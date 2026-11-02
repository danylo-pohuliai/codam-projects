*This project has been created as part of the 42 curriculum by myapaten, dpohulia.*
# push_swap
## Description
**push_swap** is an algorithmic project at 42 that challenges students to sort data on a stack, with a limited set of instructions, using the lowest possible number of actions. To succeed, various sorting algorithms must be manipulated and chosen to output the most optimized data sorting solution.
The project utilizes two stacks (Stack A and Stack B) and specific operations to manipulate them (e.g., push, swap, rotate, reverse rotate). The ultimate goal is to have all numbers sorted in ascending order in Stack A with the absolute minimum number of operations.
## Technical Choices & Collaboration
This project was developed jointly by **myapaten** and **dpohulia**. While both of us actively collaborated on all stages of development (data validation, algorithm design, and the bonus checker program), the workload was slightly distributed based on focus areas: **myapaten** focused a bit more on the core algorithm implementations, and **dpohulia** focused slightly more on robust data validation and parsing.
Instead of traditional doubly linked lists, we opted for a highly optimized **Circular Buffer (Ring Buffer)** architecture using static arrays. This allows us to achieve O(1) time complexity for all push_swap operations (ra, rra, pa, pb, etc.) simply by manipulating a head index, completely eliminating the overhead and memory fragmentation of constant malloc and free calls.
## Algorithms: Explanation and Justification
According to the subject guidelines, projects often map specific algorithms to specific data sizes. Through rigorous benchmarking and architectural changes, we mapped Chunk Sort to our medium strategy and Radix Sort to our complex strategy.
### 1. Simple Sort (Low Disorder / Small Stacks)
For small stacks or arrays with low disorder, we implemented an **Adaptive Insertion Sort**.
 * **Explanation:** The algorithm filters the stack by identifying the longest pre-existing increasing sequence. Any number that breaks this sequence is pushed to Stack B (acting as an "error" buffer). Once filtered, the algorithm iterates through Stack B, calculates the exact target position for each number in Stack A, and uses a smart rotation function (smart_rotate_a) to find the cheapest path (either ra or rra) to insert the number back.
 * **Justification:** This approach ensures pure O(N) performance on nearly sorted arrays. It avoids the O(N^2) pitfalls of traditional Bubble Sort or standard Insertion Sort by keeping the sorted frame completely intact.
### 2. Medium Sort (Chunk Sort)
 * **Explanation:** To sort medium datasets, we implemented a highly optimized Chunk Sort. The algorithm calculates a dynamic chunk size using an approximated square root formula: `sqrt(size) * 1.5`. It pushes elements to Stack B in these defined chunks, pushing smaller numbers to the bottom of B (`rb`) and larger numbers to the top. Once Stack A is empty, it finds the absolute maximum value in Stack B and calculates the shortest rotational path to push it back to Stack A.
 * **Justification:** Chunk sort effectively handles arrays with moderate disorder. By intelligently dividing the array into chunks and utilizing double operations, it drastically reduces the total operation count.
### 3. Complex Sort (Radix Sort)
 * **Explanation:** We use a classic Base-2 Radix Sort utilizing bitwise operations for large datasets. Before sorting, the array is **normalized** (coordinate compression)—meaning raw values (e.g., -5000, 42, 10) are replaced by their relative sorted indices (0, 3, 2). The algorithm then checks each bit (from 0 to 31) of the normalized numbers. If the bit is 1, it stays in Stack A (`ra`); if it is 0, it goes to Stack B (`pb`).
 * **Justification:** Radix Sort guarantees a passing grade for our complex, large arrays. Its predictable approach makes it a robust choice, as it relies strictly on bitwise operations regardless of the initial disorder.
## Instructions
### Compilation
The project includes a Makefile to compile the executable and the bonus checker.
 * To compile the main sorting program:
   ```bash
   make
   ```
 * To compile the bonus checker program:
   ```bash
   make bonus
   ```
 * To clean object files: make clean
 * To clean everything (objects and executables): make fclean
 * To recompile: make re
### Execution
Run push_swap with a list of integers (can be passed as separate arguments or as a single formatted string):
```bash
./push_swap 4 67 3 87 23
./push_swap "4 67 3 87 23"
```
#### Custom Flags & Adaptive Strategy
The program supports custom flags to force specific sorting behaviors or display benchmarking metrics:
 * --bench: Outputs detailed metrics (total operations, disorder percentage, algorithm used, and exact counts per operation type) to stderr.
 * --simple, --medium, --complex: Forces the program to use a specific sorting algorithm.
 * **Adaptive Default:** If no specific algorithm flag is provided, the program calculates the **disorder** ratio of the input array (the number of inversions compared to total possible pairs) and adaptively selects the most efficient strategy:
   * Disorder < 20% (0.2f): Uses STRAT_SIMPLE
   * Disorder < 50% (0.5f): Uses STRAT_MEDIUM
   * Disorder \ge 50%: Uses STRAT_COMPLEX
#### Advanced Testing & Benchmarking
You can use bash command chaining to generate random numbers, run the sort, save benchmarks, and verify the output simultaneously. For example:
```bash
shuf -i 0-9999 -n 100 > args.txt ; ./push_swap --bench --simple $(cat args.txt) 2> bench.txt | ./checker $(cat args.txt)
```
**What this does:**
 1. shuf -i 0-9999 -n 100 > args.txt: Generates an array of 100 unique random numbers between 0 and 9999 and saves them into args.txt.
 2. ./push_swap ... 2> bench.txt: Runs the sorting algorithm using the generated numbers, forcing the --simple strategy and --bench mode. The standard operations output (pa, ra, etc.) is piped forward, while the benchmark statistics (stderr) are cleanly redirected into bench.txt.
 3. | ./checker_linux ...: Pipes the sequence of sorting operations into the checker, which validates if the instructions successfully sort the given initial sequence.
#### The Bonus Checker Architecture
To verify the sorting operations manually, pipe the output of push_swap into the checker program:
```bash
./push_swap 4 67 3 87 23 | ./checker 4 67 3 87 23
```
Architecturally, the checker and push_swap binaries are designed to be highly modular. They share the exact same core engine (SHARED_SRCS inside the Makefile, including operations, memory management, and data validation), ensuring 100% logic consistency. The heavy sorting algorithms are isolated strictly to the push_swap compilation.
The checker program operates by utilizing a continuous read-eval loop:
 1. It reads standard input (stdin / file descriptor 0) line-by-line using get_next_line.
 2. It compares each read line against known instructions (e.g., sa\n, pb\n) and applies the corresponding shared function (do_sa, do_pb).
 3. If an invalid or unknown command is detected, it triggers a custom error handler that immediately outputs Error, frees all allocated memory (both stacks and the command string), and safely exits.
 4. Once the input stream ends, it verifies the final state. If Stack A is perfectly sorted **and** Stack B is completely empty (app->b->size == 0), it outputs OK. If either condition is unmet, it outputs KO.
## Resources
### References
 * **Coordinate Compression (Normalization):** Standard competitive programming technique used to handle negative values and large gaps between numbers in Radix Sort.
 * **Radix Sort:** General bitwise sorting methodologies.
 * **Circular Buffer (Ring Buffer):** Data structure theory for overriding linear arrays.
### AI Usage
Artificial Intelligence (LLMs) was utilized strictly as an educational and debugging tool, specifically to understand the mathematical mechanics of the **Circular Buffer**.
 * **Conceptual Understanding:** AI was used to explain the modular arithmetic required to read logical indices from physical memory (data[(head + i) % capacity]).
 * **Logic Verification:** AI helped debug our initial implementations of the operations (push, swap, rotate, reverse_rotate). Specifically, it explained why simple head adjustments cause "holes" or duplicate numbers when an array is not at full capacity, and helped us formulate the correct logic to physically move the elements to the "tail" index ((head + size) % capacity) before shifting the pointers.