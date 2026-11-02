# Codam Coding College (42 Network) — Core Curriculum Projects

Welcome to my monorepo containing projects completed as part of the **Core Curriculum at [Codam Coding College](https://www.codam.nl/) (42 Network)** in Amsterdam.

This repository hosts a collection of projects focusing on low-level systems programming in **C**, algorithmic optimization, **Linux** system administration, **POSIX multithreading**, and **Python** software engineering.

---

> ### ⚠️ Academic Integrity Notice for 42 / Codam Students
> **This repository is published strictly for portfolio and archival purposes.**
> If you are currently a student at Codam or any 42 Network campus, **do not copy or submit any code from this repository**. The 42 pedagogy relies on peer-to-peer learning, struggling through problems yourself, and being able to defend every single line of your code during evaluations. Blindly copying code will rob you of the learning experience and lead to a `-42` cheat flag.

---

## Engineering Standards Across All C Projects

Every C project in this repository is built under strict systems engineering constraints:
* **Zero External Libraries:** Standard C library functions (`libc`) are forbidden unless explicitly permitted; core utilities and data structures are implemented from scratch.
* **Strict Compilation:** All code compiles cleanly with `-Wall -Wextra -Werror`.
* **Memory Safety:** Zero memory leaks, invalid reads/writes, or dangling pointers (rigorously verified with **Valgrind** and **GDB**).
* **Strict Coding Standard (The Norm):** Enforced limits on function length (max 25 lines), variables per function, and modular file organization.

---

## Engineering Standards Across All Python Projects

Every Python project in this repository adheres to modern software engineering best practices:
- **Type Safety:** Strict static type hinting is enforced across all modules (verified with `mypy`).
- **Clean Code & Formatting:** Adherence to PEP 8 standards, utilizing tools like `flake8`, `black`, or `isort` for consistent readability.
- **Robust Architecture:** Focus on Object-Oriented Programming (OOP) principles, modular design, and separation of concerns.
- **Data Validation:** Comprehensive validation using libraries like `pydantic` to ensure data integrity at runtime.

---

## Repository Architecture

Each project directory contains its own detailed `README.md` with build instructions, architecture notes, and usage examples as required by the Codam curriculum.

<pre>
.
├── Milestone0/
│   └── Libft/                  # Custom C standard library implementation
├── Milestone1/
│   ├── ft_printf/              # Variadic printf implementation in C
│   ├── get_next_line/          # Buffered file descriptor I/O reader
│   └── push_swap/              # Stack sorting algorithm optimizer
├── Milestone2/
│   ├── A-Maze-ing/             # Algorithmic maze generation & solving
│   ├── Born2beroot/            # Hardened Debian Linux server & LVM setup
│   └── Python Modules/         # Modules 00–10: OOP, FP, Packaging & Data
└── Milestone3/
    ├── Call Me Maybe/          # Constrained LLM decoding & tool-calling SDK
    └── Codexion/               # POSIX threads (pthreads) & mutex concurrency
</pre>

---

## Milestones Overview

### [Milestone 0 — Foundations of Low-Level C](./Milestone0)
* **[Libft](./Milestone0/Libft):** Re-implementation of essential standard C library (`libc`) functions, dynamic memory management, string manipulation, and singly linked list data structures.

### [Milestone 1 — I/O Buffering, Variadic Functions & Algorithms](./Milestone1)
* **[ft_printf](./Milestone1/ft_printf):** Custom implementation of the standard `printf` function using variadic arguments (`stdarg.h`) and modular format parsing.
* **[get_next_line](./Milestone1/get_next_line):** Buffered line-by-line reader supporting multiple simultaneous file descriptors via static memory persistence.
* **[push_swap](./Milestone1/push_swap):** Sorting algorithm sorting data across two stacks using a minimal set of assembly-like stack operations with optimized time/operation complexity.

### [Milestone 2 — System Administration, Algorithms & Python Track](./Milestone2)
* **[A-Maze-ing](./Milestone2/A-Maze-ing):** Procedural maze generation, graph traversal, and pathfinding architecture.
* **[Born2beroot](./Milestone2/Born2beroot):** Linux system administration project covering Debian server hardening, encrypted LVM partitioning, SSH/UFW security policies, and automated Bash telemetry scripts.
* **[Python Modules (00–10)](./Milestone2/Python%20Modules):** Intensive 11-module track covering Python internals, Object-Oriented Programming, functional paradigms, custom package architecture (`alchemy`), and data structures.

### [Milestone 3 — Concurrency, Multithreading & AI Systems](./Milestone3)
* **[Codexion](./Milestone3/Codexion):** Multithreaded resource-contention simulation in C using POSIX threads (`pthreads`), mutex synchronization, deadlock avoidance, and precision microsecond timing (includes a custom automated `tester`).
* **[Call Me Maybe](./Milestone3/Call%20Me%20Maybe):** Deterministic function-calling and constrained token generation pipeline for Large Language Models using `llm_sdk`.

---
