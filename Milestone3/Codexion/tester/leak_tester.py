import subprocess
import os
import re
import sys

RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
RESET  = "\033[0m"

print(f"{YELLOW}Building test executable via 'make test'...{RESET}")
try:
    subprocess.run(["make", "test"], check=True)
except subprocess.CalledProcessError:
    print(f"{RED}[FAIL] Failed to compile test executable. Check your Makefile and tester.c/h{RESET}")
    sys.exit(1)

def run_fault_injection_tests(env_var_name, run_cmd):
    print(f"\n--- Testing: {env_var_name} ---")

    for i in range(1, 20000):
        env = os.environ.copy()
        env[env_var_name] = str(i)

        try:
            result = subprocess.run(run_cmd, env=env, capture_output=True, text=True, timeout=5)
        except subprocess.TimeoutExpired:
            print(f"{GREEN}[DONE] Simulation started safely. All {env_var_name} scenarios checked (total {i-1} limits reached).{RESET}")
            break

        print(result.stderr, end="")
        stdOut = []
        if result.stdout:
            stdOut = result.stdout.split("\n")
            print("[STDOUT]: ", end="")
            for line in stdOut[0:4]:
                print(line)
            print("...")
            for line in stdOut[-4:]:
                print(line)
        else:
            print(f"[STDOUT]: {result.stdout}")

        if "[INJECTOR] Blocked" in result.stderr:
            if result.returncode in [0, 1]:
                match = re.search(r"\[INJECTOR_STATS\] Mallocs: (\d+)/(\d+), Mutexes: (\d+)/(\d+), Conds: (\d+)/(\d+), Threads: (\d+)/(\d+)", result.stderr)

                if match:
                    free_mem, alloc_mem, dest_m, cre_m, dest_c, cre_c, join_t, cre_t = map(int, match.groups())

                    if free_mem >= alloc_mem and dest_m == cre_m and dest_c == cre_c and join_t == cre_t:
                        print(f"{GREEN}[OK] PERFECT CLEANUP (Exit {result.returncode}) on {env_var_name} #{i} (Mallocs: {alloc_mem}, Mutexes: {cre_m}, Conds: {cre_c}, Threads: {cre_t}){RESET}")
                    else:
                        print(f"{RED}[FAIL] RESOURCE LEAK DETECTED on {env_var_name} #{i}!{RESET}")
                        if free_mem != alloc_mem:
                            print(f"{RED}   -> Memory Leak: Allocated {alloc_mem}, but Freed only {free_mem}{RESET}")
                        if dest_m != cre_m:
                            print(f"{RED}   -> Mutex Leak: Created {cre_m}, but Destroyed only {dest_m}{RESET}")
                        if dest_c != cre_c:
                            print(f"{RED}   -> Cond Leak: Created {cre_c}, but Destroyed only {dest_c}{RESET}")
                        if join_t != cre_t:
                            print(f"{RED}   -> Thread Leak: Created {cre_t}, but Joined/Detached only {join_t}{RESET}")
                else:
                    print(f"{YELLOW}[WARN] Missing Injector Stats! Did the program crash hard? (Exit {result.returncode}){RESET}")
            else:
                print(f"{RED}[FAIL] CRASH (Exit Code {result.returncode}) on failure {env_var_name} #{i}!{RESET}")
                print(result.stderr.strip())
        else:
            print(f"{GREEN}[DONE] All {env_var_name} scenarios checked (total {i-1} limits reached).{RESET}")
            break

def run_happy_path_test(run_cmd):
    print(f"\n{YELLOW}--- Testing: HAPPY PATH (No Injected Failures) ---{RESET}")

    env = os.environ.copy()

    for fail_var in ["FAIL_MALLOC_AT", "FAIL_MUTEX_AT", "FAIL_COND_AT", "FAIL_THREAD_AT"]:
        if fail_var in env:
            del env[fail_var]

    try:
        result = subprocess.run(run_cmd, env=env, capture_output=True, text=True, timeout=15)
    except subprocess.TimeoutExpired:
        print(f"{RED}[FAIL] Happy Path timed out! Did the simulation hang or is it waiting endlessly?{RESET}")
        return

    print(result.stderr, end="")
    stdOut = []
    if result.stdout:
        stdOut = result.stdout.split("\n")
        print("[STDOUT]: ", end="")
        for line in stdOut[0:4]:
            print(line)
        print("...")
        for line in stdOut[-4:]:
            if line.strip():
                print(line)
    else:
        print(f"[STDOUT]: {result.stdout}")

    if result.returncode != 0:
        print(f"{RED}[FAIL] Program exited with non-zero code {result.returncode} on Happy Path!{RESET}")
        return

    match = re.search(r"\[INJECTOR_STATS\] Mallocs: (\d+)/(\d+), Mutexes: (\d+)/(\d+), Conds: (\d+)/(\d+), Threads: (\d+)/(\d+)", result.stderr)

    if match:
        free_mem, alloc_mem, dest_m, cre_m, dest_c, cre_c, join_t, cre_t = map(int, match.groups())

        if free_mem >= alloc_mem and dest_m == cre_m and dest_c == cre_c and join_t == cre_t:
            print(f"{GREEN}[OK] PERFECT CLEANUP on Happy Path! (Mallocs: {alloc_mem}, Mutexes: {cre_m}, Conds: {cre_c}, Threads: {cre_t}){RESET}")
        else:
            print(f"{RED}[FAIL] RESOURCE LEAK DETECTED on Happy Path!{RESET}")
            if free_mem != alloc_mem:
                print(f"{RED}   -> Memory Leak: Allocated {alloc_mem}, but Freed only {free_mem}{RESET}")
            if dest_m != cre_m:
                print(f"{RED}   -> Mutex Leak: Created {cre_m}, but Destroyed only {dest_m}{RESET}")
            if dest_c != cre_c:
                print(f"{RED}   -> Cond Leak: Created {cre_c}, but Destroyed only {dest_c}{RESET}")
            if join_t != cre_t:
                print(f"{RED}   -> Thread Leak: Created {cre_t}, but Joined/Detached only {join_t}{RESET}")
    else:
        print(f"{YELLOW}[WARN] Missing Injector Stats! Did the program crash hard or skip destructor?{RESET}")

print("\n\n\nTESTING WITH SMALL AMOUNT OF CODERS\n\n\n")

run_cmd = [ "./codexion", "3", "400", "30", "30", "30", "1", "30", "fifo"]
run_happy_path_test(run_cmd)
run_fault_injection_tests("FAIL_MALLOC_AT", run_cmd)
run_fault_injection_tests("FAIL_MUTEX_AT", run_cmd)
run_fault_injection_tests("FAIL_COND_AT", run_cmd)
run_fault_injection_tests("FAIL_THREAD_AT", run_cmd)

print("\n\n\nTESTING WITH AVERAGE AMOUNT OF CODERS\n\n\n")
run_cmd = [ "./codexion", "40", "400", "30", "30", "30", "1", "30", "fifo"]
run_happy_path_test(run_cmd)
run_fault_injection_tests("FAIL_MALLOC_AT", run_cmd)
run_fault_injection_tests("FAIL_MUTEX_AT", run_cmd)
run_fault_injection_tests("FAIL_COND_AT", run_cmd)
run_fault_injection_tests("FAIL_THREAD_AT", run_cmd)
print("\n\n\nTESTING WITH HUGE AMOUNT OF CODERS\n\n\n")
run_cmd = [ "./codexion", "300", "400", "30", "30", "30", "1", "30", "fifo"]
run_happy_path_test(run_cmd)
run_fault_injection_tests("FAIL_MALLOC_AT", run_cmd)
run_fault_injection_tests("FAIL_MUTEX_AT", run_cmd)
run_fault_injection_tests("FAIL_COND_AT", run_cmd)
run_fault_injection_tests("FAIL_THREAD_AT", run_cmd)