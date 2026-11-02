*This project has been created as part of the 42 curriculum by dpohulia.*

# Call Me Maybe - Constrained Function Calling in LLMs

## Description
**Goal:** The primary objective of this project is to bridge the gap between natural language understanding and machine-executable commands by implementing a highly reliable function calling system using a Small Language Model (Qwen3-0.6B).

**Overview:** Small language models (like the 0.6B parameter model used here by default) are notoriously unreliable at generating structured output, often succeeding only 30% of the time. They frequently hallucinate JSON keys, mismatch data types, or fail to output parseable syntax. This project solves these issues entirely by employing **Constrained Decoding**. Instead of relying on prompt engineering and hoping for valid output, the system intercepts the LLM's generation process token-by-token. By dynamically selecting only from a pre-approved set of valid tokens at each generation step, the program mathematically guarantees that the output will be 100% structurally valid JSON that perfectly matches the predefined function schemas.

## Instructions

### Requirements
*   Python 3.10+.
*   `uv` package manager (for dependency isolation and running).
*   The `llm_sdk` provided by the curriculum placed in the root directory.
*   Only `pydantic`, `numpy`, and `json` packages are permitted; frameworks like `transformers`, `pytorch`, or `outlines` are strictly forbidden.

### Installation
Clone the repository and sync the dependencies using `uv`:
```bash
git clone <repository_url> call-me-maybe
cd call-me-maybe
uv sync
```

### Execution & CLI Flags

You can run the project using the provided `Makefile` or directly via `uv`. The application supports several command-line arguments to customize the execution environment.

```bash
uv run python -m src [OPTIONS]
```

| Flag | Description | Default Value |
| --- | --- | --- |
| `--functions_definition` | Path to the JSON file containing the available function schemas. | `data/input/functions_definition.json` |
| `--input` | Path to the JSON array of natural language prompts to process. | `data/input/function_calling_tests.json` |
| `--output` | Path where the generated function calls will be saved. | `data/output/function_calling_results.json` |
| `--model` | Selects the LLM model target. Supports predefined aliases (`qwen3`, `smol`, `smol-135`) or a direct model path. | `qwen3` |
| `--fast_forward` | Enables structural syntax injection (Fast-Forwarding) to massively speed up generation. | `False` (Disabled) |
| `--visualisation` | Enables real-time colored terminal output to monitor the token-by-token generation process. | `False` (Disabled) |

Example:
```bash
uv run python -m src --functions_definition data/input/my_best_function_definitions.json --input data/input/my_average_function_calling_tests.json --output data/output/your_poor_function_calling_results.json --model qwen2.5-1.5b --fast_forward --visualisation
```

## Algorithm Explanation

The core algorithm relies on **Constrained Decoding** combined with a rigid **Finite State Machine (FSM)**.

### 1. Stage 1 (Semantic Routing)

The LLM is prompted with function descriptions. A Trie-based prefix cache forces the model to select a valid function name token-by-token. The rule states that the function must be chosen using the LLM, not heuristics. By masking logits of invalid characters, we force the LLM to traverse a pre-calculated tree of valid function names using its own semantic reasoning, stopping exactly when a valid name is completed.

### 2. Fast-Forwarding (Syntax Injection)

When the `--fast_forward` flag is active, the system injects static JSON boilerplate (e.g., `{"name": "`, `", "parameters": {`) directly into the `input_ids` sequence without invoking the LLM.

* **Why is it powerful?** Calling `get_logits_from_input_ids` forces a forward pass through millions of parameters. Fast-forwarding skips these expensive neural network calculations for predictable syntax, saving seconds of execution time per prompt.
* **Why is it compliant?** The project rules require generating 100% valid JSON and ensuring the LLM chooses the function. Fast-forwarding does not alter the LLM's semantic decisions (like choosing the function or parameter values); it strictly enforces the structural JSON wrapper, completely eliminating the risk of syntax hallucinations.



### 3. Dynamic Masking & Termination (Preventing Hallucinations)

A major issue with small LLMs is the tendency to enter infinite generation loops or hallucinate endless text. The FSM prevents this via strict termination conditions:

* **Type Bounds:** When generating a number, the allowed token set is strictly limited to digits and a single decimal point.
* **Hard Limits:** Iterative structures like arrays or strings are constrained by forced loop limits (e.g., `for _ in range(60):` for strings). If the LLM refuses to generate a closing quote (`"`), the system forces the closure, guaranteeing the JSON does not break and the process terminates gracefully.
* **Deterministic Bypass:** If only one token is structurally valid at a given step (e.g., the rest of a predefined word), the LLM evaluation is bypassed (`len(allowed) == 1` optimization).

## Design Decisions

* **Custom BPE Tokenizer (Bonus):** To optimize performance and avoid direct use of `encode` and `decode` in the main code, a custom Byte-Pair Encoding algorithm was implemented from scratch using token IDs as merge ranks.


* **Contextual Numeric Trie:** To drastically speed up number generation, the algorithm pre-extracts numeric values from the prompt using Regex. It builds an allowed token sequence, allowing the model to auto-complete large numbers (e.g., `1234567.89`) in 0 milliseconds without invoking the model's logits.
* **Shift-Left Security:** Architectural constraints and schema validations are handled via strict `Pydantic` validation models.



## Performance Analysis

* **Accuracy:** Achieves 100% valid JSON formatting and strict schema compliance across all edge cases (nested arrays, booleans, floats, strings with quotes).
* **Speed:** Highly optimized. By using `set` lookups `O(1)` for prefix caching and bypassing the LLM forward pass when deterministic choices exist, the system processes complex prompts rapidly. Cache preparation time was reduced from ~14 seconds to <0.05 seconds.

## Challenges Faced

* **Token Boundary & Quote Anxiety:** The small model struggled with merged tokens (e.g., `"/`) and refused to escape quotes properly due to training biases. *Solution:* Implemented true BPE encoding to maintain token semantics and handled Python vs. JSON apostrophe escaping at the post-processing sanitization layer.
* **Regex Generation Degradation:** The 0.6B model failed at generating raw regex syntax character-by-character. *Solution:* Shifted regex logic to a "Stage 3" semantic classifier, mapping prompt intents to single token choices (A-F), mapping them to hardcoded regex strings later.
* **Big O Bottleneck in Caching:** Iterating `startswith` over a 150,000-token vocabulary took ~14s. *Solution:* Pre-calculated all valid function name substrings and used Python Hash Sets (`set()`), dropping complexity to `O(1)` and generation time to milliseconds.
* **Hallucinations & Infinite Loops:** The model frequently forgot to close arrays or strings. *Solution:* Implemented strict sequence termination within the FSM (e.g., peeking for bracket close IDs `]` and forcing syntax closures when hard loop constraints are met).

## Testing Strategy

* **Manual Edge-Case Testing:** Curated a diverse set of manual test cases to evaluate boundary conditions. This included testing empty JSON inputs, malformed structures, missing keys, and various overlapping data types to ensure the system handles errors gracefully without crashing.


* **Static Type Checking:** Extensively utilized `mypy` with flags like `--warn-return-any`, `--ignore-missing-imports`, and `--check-untyped-defs` to enforce rigorous type safety across all components, preventing runtime crashes before they happen.


* **Linting:** Used `flake8` to ensure clean, PEP8-compliant code structure.

## Example Usage

To process a custom batch of prompts with Fast-Forwarding and Visualization enabled:

```bash
uv run python -m src --input data/input/my_custom_prompts.json --fast_forward --visualisation
```

**Output format generated:**

```json
[
  {
    "prompt": "Calculate compound interest on 1234567.89 at 0.0375 rate for 23 years",
    "name": "fn_calculate_compound_interest",
    "parameters": {
      "principal": 1234567.89,
      "rate": 0.0375,
      "years": 23
    }
  }
]
```

## Resources

* [HuggingFace NLP Course: Byte-Pair Encoding](https://huggingface.co/learn/nlp-course/chapter6/5)
* **AI Usage:** AI (Google Gemini) was utilized as a thought partner to brainstorm algorithmic optimizations. Specifically, it assisted in moving from an `O(N*M)` string comparison approach to an `O(1)` HashSet approach for the vocabulary cache, implementing the true BPE fallback logic without a `merges.txt` file, and provided comprehensive theoretical explanations regarding tokenization mechanics, token boundary issues, and techniques to prevent autoregressive hallucinations.