*This project has been created as part of the 42 curriculum by dpohulia*


# Description

**Codexion** is a multi-threaded scheduling and resource management simulation developed as part of the 42/Codam curriculum. The primary goal of this project is to implement a concurrent system where multiple threads (coders) compete for shared, limited resources (USB dongles) without encountering deadlocks, data races, or resource starvation.
In this simulation, coders sit in a circular co-working hub and alternate between three states: compiling, debugging, and refactoring. Crucially, the dongles are not placed in a shared central pool. Instead, exactly one dongle lies between each adjacent pair of coders. A coder can **only** request and acquire the specific dongles placed immediately to their left and right — nowhere else.

To solve the concurrency challenges of this setup, the project relies on three core concepts:
*   **Threads:** Each coder (and the observer/monitor) runs as a separate POSIX thread (`pthread`), allowing them to operate concurrently in real-time.
*   **Mutexes (Mutual Exclusion):** Locks used to protect shared resources (like the dongles, print logs, and coder states) so that only one thread can access them at a time, preventing data corruption.
*   **Condition Variables:** Primitives that allow threads to pause execution and sleep until a specific event occurs (e.g., a dongle becoming available), ensuring the simulation does not waste CPU cycles.

To compile, a coder must acquire both of these adjacent dongles simultaneously. The core challenge lies in the implementation of fair arbitration policies — **FIFO** (First In, First Out) and **EDF** (Earliest Deadline First) — to manage localized dongle requests from neighboring coders during their mandatory "cooldown" periods. A dedicated monitor thread continuously checks the state of all coders to ensure that the simulation stops immediately and precisely (within 10ms) if any coder "burns out" due to a lack of compilation time.

# Instructions

### Compilation

To compile the project, simply run the following command at the root of the repository. It will generate the `codexion` executable:

```bash
make
```

### Execution

Run the program with the following mandatory arguments:

```bash
./codexion number_of_coders time_to_burnout time_to_compile time_to_debug time_to_refactor number_of_compiles_required dongle_cooldown scheduler
```

**Parameters overview:**

* `number_of_coders`: The number of coders (and the number of dongles on the table).
* `time_to_burnout`: Time in milliseconds. If a coder doesn't start compiling within this time since their last compile (or the start of the simulation), they burn out.
* `time_to_compile`: Time in milliseconds a coder spends compiling (requires holding 2 dongles).
* `time_to_debug`: Time in milliseconds a coder spends debugging.
* `time_to_refactor`: Time in milliseconds a coder spends refactoring.
* `number_of_compiles_required`: If all coders reach this number of compilations, the simulation ends successfully.
* `dongle_cooldown`: Time in milliseconds a dongle remains unavailable after being released by a coder.
* `scheduler`: The arbitration policy for the dongles. Must be either `fifo` or `edf`.

**Example:**

```bash
./codexion 5 300 30 25 20 4 40 edf
```

### Testing

An automated testing suite has been developed to verify edge cases, starvation prevention, and memory safety. To access the testing environment, switch to the dedicated `dev` branch and execute commands in this order:

```bash
git switch dev
mv dev/tests.sh dev/tester.h dev/tester.c dev/leak_tester.py .
git switch master
bash tests.sh
make fclean
make test
python3 leak_tester.py
```

Concurrency & Race Condition Testing
Extensive testing was performed using both Valgrind and Clang/GCC's Thread Sanitizer to ensure strict thread safety and synchronization.

Using Valgrind (DRD & Helgrind):

```bash
valgrind --tool=helgrind ./codexion 5 400 70 20 30 3 100 edf
valgrind --tool=helgrind ./codexion 5 800 200 200 200 10 10 edf
valgrind --tool=drd ./codexion 2 400 70 20 30 8 10 edf
```

Using Thread Sanitizer:
You can also compile the project with the Thread Sanitizer flag to detect data races at runtime:

```bash
cc -g -fsanitize=thread -Wextra -Werror -Wall -pthread *.c -o codexion
```

Translate fsanitize from addr to human language:
```bash
addr2line -e ./codexion 0x4bc844
```

```
⚠️ WARNING: Never run an executable compiled with -fsanitize=thread using Valgrind. These tools intercept memory and thread events differently; combining them will cause severe conflicts, crashes, or unreadable garbage output.
```

### Note on Helgrind False Positives and Condition Variables

When running the project under Valgrind's **Helgrind** tool, you may encounter recurring error blocks that look like this:

```text
==78250== Thread #19: pthread_cond_{signal,broadcast}: dubious: associated lock is not held by any thread
==78250==    at 0x48513D6: ??? (in /usr/libexec/valgrind/vgpreload_helgrind-amd64-linux.so)
==78250==    by 0x491202E: __pthread_cond_wait_common (pthread_cond_wait.c:516)
==78250==    by 0x491202E: pthread_cond_timedwait@@GLIBC_2.3.2 (pthread_cond_wait.c:652)
...
==78250==    by 0x403243: _sleep (in /codexion/codexion)
```
This is a well-known false positive in Helgrind. Here is a detailed explanation of why it happens and why our implementation is actually safe:

How pthread_cond_timedwait works internally:
According to the POSIX standard, when a thread calls pthread_cond_timedwait (or pthread_cond_wait), it must do so while holding the associated mutex. Internally, the OS atomically unlocks the mutex and puts the thread to sleep. When the thread is signaled to wake up (or the timeout expires), it automatically re-acquires the mutex before returning control to your program.

The Helgrind Bug:
Helgrind tracks lock ownership by wrapping standard pthread functions. However, its tracking mechanism struggles to accurately follow the internal atomic release/re-acquire cycle that happens deep inside glibc during a condition wait.
When the monitor thread broadcasts a signal to stop the simulation, or a thread wakes up from a timeout, Helgrind sometimes observes the internal state before the mutex is fully re-acquired by the waking thread. It assumes the condition variable was operated on without a lock and throws the dubious: associated lock is not held by any thread error.

Why DRD is better for this project:
Valgrind's DRD (Data Race Detector) tool uses a different, more sophisticated algorithm for tracking thread states and synchronization events. It correctly understands the atomicity of POSIX condition variables and can trace the state through the kernel without dropping the lock context.

Because our architecture relies heavily on precise sleeping queues via pthread_cond_timedwait for handling dongle cooldowns and usleep replacements, DRD is the strictly preferred tool. If DRD reports 0 errors, the synchronization logic is fundamentally sound, despite Helgrind's complaints.

---

# Blocking cases handled

To ensure a robust simulation, several critical concurrency issues (blocking cases) were addressed in the architecture:

*   **Data Races & State Inconsistency:** Every read and write operation on shared variables (such as a coder's last compile time, the simulation stop flag, or a dongle's queue state) is strictly protected by mutexes. This guarantees that the monitor always reads accurate timestamps and no two coders can modify a dongle's state simultaneously.
*   **Starvation Prevention:** A strict arbitration algorithm (FIFO or EDF) evaluates competing requests for the same dongle. In EDF mode, the dongle is granted to the coder whose burnout deadline is closest, successfully preventing starvation even under heavy load.
*   **Dongle Cooldown Handling:** When a dongle is released, it enters a mandatory cooldown period. Instead of busy-waiting, coders requesting a cooling dongle calculate the remaining time and sleep precisely until the cooldown expires using `pthread_cond_timedwait`, waking up exactly when the dongle becomes valid for arbitration.
*   **Precise Burnout Detection & Global Shutdown (The "Poison Pill"):** When a coder dies, the simulation must stop instantly without leaving other threads stuck waiting for dongles. To handle this, a "Poison Pill" strategy is used: the monitor sets a global stop flag and broadcasts a signal to all condition variables across the entire simulation. This forces all blocked threads to wake up, evaluate the stop flag, and cleanly exit their routines.
*   **Log Serialization:** A dedicated `print_mutex` is used to prevent terminal output from interleaving. Furthermore, the print routine checks the simulation's global stop flag *after* acquiring the lock, guaranteeing that absolutely no actions are logged after a "burned out" message is printed.

# Thread synchronization mechanisms

This project strictly avoids **busy-waiting** (spinning in infinite `while` loops that consume 100% CPU). Instead, it relies on POSIX synchronization primitives to manage flow efficiently:

*   **`pthread_mutex_t` (Atomicity):**
    Mutexes are the backbone of data integrity in this project. They ensure that operations on shared memory are atomic. A strict design principle applied throughout the codebase is **keeping critical sections as short as possible**. Mutexes are locked right before accessing shared data and unlocked immediately after, significantly reducing thread contention and minimizing the risk of bottlenecks.
*   **`pthread_cond_t` (Efficient Waiting):**
    Condition variables are used to manage waiting queues natively. When a coder attempts to take a dongle that is currently held by their neighbor, they call `pthread_cond_wait`. This safely puts the thread to sleep, yielding the CPU to the OS. Once the neighbor releases the dongle, they call `pthread_cond_signal` to wake the waiting coder up.
*   **`pthread_cond_timedwait` (Precision Sleeping):**
    Standard functions like `usleep` can be imprecise and do not interact well with mutexes. `pthread_cond_timedwait` is utilized for internal sleeping mechanisms (like waiting during debugging/refactoring phases or dongle cooldowns). It atomically unlocks the associated mutex, sleeps for the required time, and locks the mutex again upon waking — or wakes up prematurely if a broadcast signal (like a simulation stop) is received.
---

# Resources

### Documentation

* [POSIX Threads (pthreads) manual](https://man7.org/linux/man-pages/man7/pthreads.7.html) (specifically `pthread_create`, `pthread_mutex`, and `pthread_cond` families).
* Standard C library documentation (`gettimeofday`, `usleep`).

### AI Usage

Artificial Intelligence was utilized during the development of this project for the following tasks:

* **Theory & Concurrency:** Explaining complex concurrency theory, race conditions, and synchronization paradigms.
* **Algorithm Guidance:** Providing conceptual guidance on properly implementing the FIFO and EDF (Earliest Deadline First) scheduling algorithms within a threaded environment.
* **Testing & QA:** Assisting in the development of the automated testing suite and proposing complex edge-case scenarios to ensure robust liveness and precise burnout detection.

### Acknowledgements

A special thanks to my peer **svpanfil** for the valuable collaboration on this project. We discussed the core logic and various test cases together. She also provided the excellent idea to enhance the custom tester by adding features to track and count the exact number of compilations per coder to verify fairness and policy correctness.

---