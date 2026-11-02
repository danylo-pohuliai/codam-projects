# Milestone 1 — Variadic Functions, Buffered I/O & Algorithmic Optimization

> ⚠️ **Note for 42/Codam Students:** This repository is for portfolio demonstration only. Please solve the problems independently.

## Overview

**Milestone 1** expands upon low-level C programming by introducing system calls (`read`, `write`), persistent state management across function calls, variadic functions, and algorithmic complexity optimization.

## Projects in this Milestone

| Project | Language | Key Engineering Concepts |
| :--- | :--- | :--- |
| **[ft_printf](./ft_printf)** | `C` | Variadic arguments (`va_list`, `va_start`, `va_arg`, `va_end`), format specifier parsing, buffered output. |
| **[get_next_line](./get_next_line)** | `C` | File descriptors, static variables, dynamic buffer management, zero-leak EOF/error handling. |
| **[push_swap](./push_swap)** | `C` | Data structures (stacks/linked lists), sorting algorithms, operation count minimization, complexity analysis. |

---

### Project Summaries

* **[ft_printf](./ft_printf):** A custom re-implementation of `<stdio.h>`'s `printf`, supporting `%c`, `%s`, `%p`, `%d`, `%i`, `%u`, `%x`, `%X`, and `%%` conversions using modular dispatch logic and `[Libft]`.
* **[get_next_line](./get_next_line):** A function that reads and returns a single line from any valid file descriptor (`stdin`, files, or network sockets) with configurable `BUFFER_SIZE` at compile time.
* **[push_swap](./push_swap):** An algorithmic challenge that calculates the shortest sequence of stack instructions (`sa`, `pb`, `ra`, `rra`, etc.) required to sort a random set of integers using two stacks.