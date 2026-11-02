# Milestone 2 — Linux System Administration, Algorithms & Python Engineering

> ⚠️ **Note for 42/Codam Students:** This repository is for portfolio demonstration only. Please solve the problems independently.

## Overview

**Milestone 2** broadens the engineering scope beyond pure C into **Linux OS architecture and security**, **procedural maze generation & pathfinding**, and a comprehensive **11-module Python software engineering track**.

## 📦 Projects in this Milestone

| Project | Tech Stack | Key Engineering Concepts |
| :--- | :--- | :--- |
| **[A-Maze-ing](./A-Maze-ing)** | `Python 3.10+`, `mypy --strict`, `flake8`, `whl` | Procedural maze generation (Recursive Backtracker), BFS shortest-path solver, bitmask hex encoding, ANSI animation, reusable `.whl` package (`mazegen`). |
| **[Born2beroot](./Born2beroot)** | `Debian Linux`, `Bash`, `LVM`, `UFW` | Server virtualization, encrypted LVM partitions, SSH/PAM hardening, `sudo` security policies, automated `cron` telemetry. |
| **[Python Modules (00–10)](./Python%20Modules)** | `Python`, `Pydantic`, `venv`, `pip` | OOP, Functional Programming, closures, lambdas, comprehensions, decorators, generators, data validation, and package architecture (`alchemy`). |

---

### Project Summaries

- **[A-Maze-ing](./A-Maze-ing):** A strictly typed (`mypy --strict`) maze generator and solver built in Python 3 and packaged as an installable wheel (`mazegen-1.0.0-py3-none-any.whl`). Generates reproducible **perfect** and **imperfect** mazes (preserving an embedded `"42"` walled pattern and preventing $3\times3$ open rooms) using a **Recursive Backtracker** (randomized DFS), computes optimal routes via **Breadth-First Search (BFS)**, serializes walls using 4-bit hexadecimal encoding (`N/E/S/W`), and renders an interactive ANSI terminal UI with step-by-step path animations.
- **[Born2beroot](./Born2beroot):** Deploying and hardening a minimal Debian Linux server from scratch without a GUI. Includes strict password/PAM policies, encrypted LVM partitions, AppArmor, UFW firewall rules, SSH key/port hardening, and a system health monitoring daemon written in Bash.
- **[Python Modules (`00` – `10`)](./Python%20Modules):** An intensive 11-module progression covering core and advanced Python engineering: data structures, list/dict comprehensions, Object-Oriented Programming (inheritance, encapsulation, polymorphism), Functional Programming (lambda functions, closures, higher-order functions, decorators, generators), strict data validation with **Pydantic**, virtual environments, import mechanics, custom package distribution, and Pythonic idioms.
