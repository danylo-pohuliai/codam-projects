# Milestone 3 — Multithreaded Concurrency, Space-Time Pathfinding & Constrained LLM Decoding

> ⚠️ **Note for 42/Codam Students:** This repository is for portfolio demonstration only. Please solve the problems independently.

## Overview

**Milestone 3** focuses on advanced systems engineering, multi-agent algorithmic optimization, and modern AI tooling: **POSIX multithreaded synchronization & fault-injection testing in C**, **multi-drone space-time routing (`Space-Time A*`)**, and **constrained decoding for Large Language Model function calling**.

## 📦 Projects in this Milestone

| Project | Tech Stack | Key Engineering Concepts |
| :--- | :--- | :--- |
| **[Codexion](./Codexion)** | `C`, `pthreads`, `Python`, `Bash` | Multithreading (`FIFO` & `EDF` scheduling), mutexes/condvars, custom fault-injection & resource-leak testing framework (`tester/`). |
| **[Call Me Maybe](./Call%20Me%20Maybe)** | `Python`, `LLM SDK`, `BPE Tokenization` | Constrained decoding, structured JSON/function calling for LLMs, token mask filtering, deterministic schema enforcement. |
| **[Fly-in](./Fly-in)** | `Python`, `Pygame`, `mypy` | Multi-agent pathfinding (**Space-Time A\***), dynamic capacity reservation tables, dead-end graph pruning, real-time visualization. |

---

### Project Summaries

- **[Codexion](./Codexion):** A high-concurrency C simulation modeling up to 300+ threads competing for shared resources under microsecond timing constraints using **FIFO** and **Earliest Deadline First (EDF)** scheduling. Engineered with a custom **Fault-Injection & Regression Testing Suite (`tester/`)**:
  - **Deterministic Fault Injector (`tester.c`, `leak_tester.py`):** Wraps `malloc`/`free`, `pthread_mutex_init`/`destroy`, `pthread_cond_init`/`destroy`, and `pthread_create`/`join` using preprocessor hooks, GCC `constructor`/`destructor` attributes, and atomic counters (`__sync_add_and_fetch`). Iteratively injects failures at the $N$-th allocation or OS primitive call (`FAIL_MALLOC_AT`, `FAIL_MUTEX_AT`, `FAIL_COND_AT`, `FAIL_THREAD_AT`) to verify 100% graceful rollback and zero resource leaks.
  - **Automated Bash Test Harness:** Runs 50+ edge-case scenarios covering CLI parsing, integer overflows, deadlock timeouts, silent exits, and exact action/burnout telemetry under both `fifo` and `edf` policies.
- **[Call Me Maybe](./Call%20Me%20Maybe):** An AI systems engineering project focused on reliable **LLM Function Calling**. Implements constrained decoding over Byte-Pair Encoding (BPE) vocabularies so a language model is mathematically guaranteed to output valid, schema-compliant tool calls (`src/` & `llm_sdk/`).
- **[Fly-in](./Fly-in):** A multi-drone fleet routing and scheduling simulator built with a custom object-oriented graph engine and **Pygame** visualization. Features a **Space-Time A\* (`Pathfinder`)** algorithm that pre-prunes dead-end zones, computes exact backward Dijkstra heuristics, and maintains turn-by-turn zone (`max_drones`) and connection (`max_link_capacity`) reservation tables to route multiple drones across normal, priority, and restricted zones in the minimum number of turns without collisions.

*(Each project directory contains its own detailed `README.md`.)*