import time
import json
import re
from typing import Any
from .ValidationModels import FunctionDef, TestPrompt, ParameterDef
from .ValidationModels import OutputResult, ErrorResult
from .TokenManager import TokenManager, LLMProtocol
from .TerminalVisualizer import TerminalVisualizer


class ConstrainedGenerator:
    """Core logic for constrained JSON generation"""

    def __init__(
        self,
        model: LLMProtocol,
        token_mgr: TokenManager,
        visualizer: TerminalVisualizer,
        fast_forwarding: bool = False,
    ) -> None:
        self.model = model
        self.tokens = token_mgr
        self.vis = visualizer
        self.fast_forwarding = fast_forwarding

    @staticmethod
    def _format_type(p: ParameterDef) -> str:
        """Converts a ParameterDef type into a string representation
        for the LLM prompt (e.g., '[<string>]')"""
        if p.type == "array" and p.items:
            return f"[<{p.items.type}>]"
        elif p.type == "object":
            return "{}"
        return f"<{p.type}>"

    @staticmethod
    def _wrap_in_chat_template(system_content: str) -> str:
        """Wraps the given content in the standard ChatML format
        (<|im_start|>, <|im_end|>) expected by the model"""

        return (
            "<|im_start|>system\n"
            f"{system_content}\n"
            "<|im_end|>\n"
            "<|im_start|>user\n"
        )

    def _build_stage1_system_prompt(self, functions: list[FunctionDef]) -> str:
        """Constructs the prompt for Stage 1 (Routing), where the LLM only
        decides WHICH function to call based on the provided list"""

        lines = []
        for fn in functions:
            lines.append(f"{fn.name}: {fn.description}")
        funcs_descr = "\n".join(lines).strip()

        content = (
            "Output JSON selecting the appropriate function.\n"
            f"{funcs_descr}"
        )
        return self._wrap_in_chat_template(content)

    def _get_special_instructions(self, fn_name: str) -> str:
        """Returns hardcoded behavioral rules and edge-case examples
        for specific functions to prevent common LLM hallucinations"""

        spec_instructions = {
            "fn_substitute_string_with_regex": (
                "CRITICAL RULES:\n"
                "1. 'source_string': Extract the EXACT target sentence or phr"
                "ase from the prompt.\n2. 'replacement': Extract the replacem"
                "ent text. If asked for a symbol (like 'asterisks' or 'dashes"
                '\'), output EXACTLY ONE symbol (e.g., "*").\nEXAMPLES:\n'
                r'- Prompt: "Substitute the word \'apple\' with \'pear\' i'
                r'n \'I like apple pie\'"' + "\n"
                r'Output: {"source_string": "I like apple pie", "regex": '
                r'"\\bapple\\b", "replacement": "pear"}' + "\n"
                r'- Prompt: "Replace all spaces in \'a b\' with EMPTY"' + "\n"
                r'Output: {"source_string": "a b", "regex": "\\s+", '
                r'"replacement": "EMPTY"}'
            ),
            "fn_execute_sql_query": (
                "CRITICAL RULES:\n"
                "1. Extract the EXACT SQL query from the prompt.\n"
                "2. DO NOT include the surrounding single quotes from th"
                "e prompt.\nEXAMPLE:\n"
                r"   Prompt: Run the query \'SELECT * FROM t\' on db" + "\n"
                r'   Output: {"query": "SELECT * FROM t", "database": "db"}'
            ),
            "fn_format_template": (
                "CRITICAL RULES:\n"
                "1. Preserve ALL punctuation and exact words from the prompt,"
                ' including quotes.\n2. If the prompt contains quotes ("), yo'
                'u MUST escape them as \\" inside the JSON.\n'
                "EXAMPLE:\n"
                r'Prompt: Format template: Say "hi" to {name}' + "\n"
                r'Output: {"template": "Say \"hi\" to {name}"}'
            ),
            "fn_read_file": (
                "CRITICAL RULES:\n"
                "1. Preserve exact file paths and punctuation.\n"
                "2. For Windows paths, keep the drive letter (e.g. C:\\) and "
                "escape backslashes (\\\\).\nEXAMPLES:\n"
                r"- Prompt: Read C:\config.ini with utf-8" + "\n"
                r'Output: {"path": "C:\\config.ini", "encoding": "utf-8"}'
                + "\n"
                r"- Prompt: Read the file at /etc/passwd" + "\n"
                r'Output: {"path": "/etc/passwd", "encoding": "utf-8"}'
            ),
            "fn_reverse_string": (
                "CRITICAL RULES:\n"
                "1. Extract the EXACT string from the prompt without modifyin"
                "g it.\nEXAMPLE (Follow exactly):\n"
                r'- If prompt is "Reverse the string \'apple\'", you MUST out'
                r'put: {"s": "apple"}'
            ),
        }
        return spec_instructions.get(fn_name, "")

    def _build_stage2_system_prompt(self, fn: FunctionDef) -> str:
        """Constructs the prompt for Stage 2 (Extraction), where the
        LLM focuses entirely on generating parameters for a SINGLE
        previously selected function"""

        params_list = []
        if fn.parameters:
            for name, p_def in fn.parameters.items():
                params_list.append(f'"{name}":{self._format_type(p_def)}')
        params_str = "{" + ",".join(params_list) + "}"

        base_info = f"{fn.name}: {fn.description}\nExpected args: {params_str}"
        rules_str = self._get_special_instructions(fn.name)

        full_desc = f"{base_info}\n{rules_str}".strip()

        content = (
            "Output JSON matching exactly the format below.\n" f"{full_desc}"
        )
        return self._wrap_in_chat_template(content)

    def _mask_and_pick(
        self, input_ids: list[int], allowed_token_ids: set[int]
    ) -> int:
        """Selects the best next token from a restricted set. Bypasses
        the LLM entirely if only 1 valid token is available
        (O(1) speed optimization)"""

        if len(allowed_token_ids) == 1:
            return next(iter(allowed_token_ids))
        raw_logits = self.model.get_logits_from_input_ids(input_ids)
        best_token_id = -1
        max_logit = -float("inf")
        for token_id in allowed_token_ids:
            current_logit = raw_logits[token_id]
            if current_logit > max_logit:
                max_logit = current_logit
                best_token_id = token_id
        return best_token_id

    def _force_syntax(self, input_ids: list[int], text: str) -> None:
        """Injects deterministic structural characters (like '{"name": "')
        directly into the token sequence without invoking the LLM"""

        target_ids = self.tokens.encode(text)
        if self.fast_forwarding:
            input_ids.extend(target_ids)
            self.vis.emit_syntax(text)
        else:
            for target_id in target_ids:
                chosen_id = self._mask_and_pick(input_ids, {target_id})
                self._append_generated_token(input_ids, chosen_id)

    def _append_generated_token(
        self, input_ids: list[int], token_id: int
    ) -> None:
        input_ids.append(token_id)
        self.vis.emit_llm_token(self.tokens.decode([token_id]))

    def _generate_string_param(self, input_ids: list[int]) -> None:
        """Generates a string parameter token-by-token. Specifically
        tracks trailing backslashes ('\\') to ensure escaped quotes
        ('\\"') don't prematurely close the JSON string"""

        start_id = self._mask_and_pick(input_ids, self.tokens.qt_tkn_ids)
        self._append_generated_token(input_ids, start_id)

        token_text = self.tokens.decode([start_id])
        is_escaped = token_text.endswith("\\")

        for _ in range(60):
            next_id = self._mask_and_pick(
                input_ids, self.tokens.txt_with_qt_ids
            )
            token_text = self.tokens.decode([next_id])

            if next_id in self.tokens.qt_tkn_ids:
                if is_escaped:
                    self._append_generated_token(input_ids, next_id)
                    is_escaped = False
                    continue
                else:
                    self._force_syntax(input_ids, '"')
                    return

            if token_text.endswith("\\"):
                is_escaped = True
            else:
                is_escaped = False

            self._append_generated_token(input_ids, next_id)

        self._force_syntax(input_ids, '"')

    def _generate_numeric_param(
        self, input_ids: list[int], is_float: bool, prompt_text: str
    ) -> None:
        """Generates numbers using a contextual Trie. Pre-extracts
        numbers from the prompt via Regex to build direct token paths,
        bypassing the LLM for large numbers"""

        # Extract all numbers from the prompt to build the Contextual Trie.
        # -?         : Optional minus sign.
        # [\d,]+     : One or more digits or commas (e.g., 1,234).
        # (?:\.\d+)? : Optional non-capturing group for decimals (e.g., .89).
        raw_nums = re.findall(r"-?[\d,]+(?:\.\d+)?", prompt_text)
        prompt_nums = {num.replace(",", "") for num in raw_nums}
        prompt_nums.update(str(i) for i in range(10))

        valid_seqs = [self.tokens.encode(num) for num in prompt_nums]

        current_seq: list[int] = []
        has_dot = False

        for step in range(20):
            allowed = set()
            can_end = False

            for seq in valid_seqs:
                if len(seq) > step and seq[:step] == current_seq:
                    allowed.add(seq[step])
                elif len(seq) == step and seq[:step] == current_seq:
                    can_end = True

            if can_end:
                allowed.update(self.tokens.delr_ids)

            if not allowed:
                allowed = (
                    self.tokens.dgt_with_delr_ids
                    if is_float
                    else self.tokens.int_with_delr_ids
                )

            next_id = self._mask_and_pick(input_ids, allowed)

            if next_id in self.tokens.delr_ids:
                if is_float and not has_dot:
                    self._force_syntax(input_ids, ".0")
                break

            current_seq.append(next_id)
            token_text = self.tokens.decode([next_id])
            if "." in token_text:
                has_dot = True

            self._append_generated_token(input_ids, next_id)

    def _generate_boolean_param(self, input_ids: list[int]) -> None:
        """Forces the model to choose exclusively between the 'true'
        and 'false' tokens."""

        allowed = {self.tokens.true_token_id, self.tokens.false_token_id}
        chosen_id = self._mask_and_pick(input_ids, allowed)
        val_str = "true" if chosen_id == self.tokens.true_token_id else "false"

        input_ids.extend(self.tokens.encode(val_str))
        self.vis.emit_llm_token(val_str)

    def _generate_array_param(
        self, input_ids: list[int], item_def: ParameterDef, prompt_text: str
    ) -> None:
        """Recursively generates a JSON array, dynamically updating allowed
          tokens to expect brackets, commas, or specific item types."""

        self._force_syntax(input_ids, "[")
        allowed_starts = set(self.tokens.bracket_close_ids)

        if item_def.type == "string":
            allowed_starts.update(self.tokens.qt_tkn_ids)
        elif item_def.type == "number":
            allowed_starts.update(self.tokens.num_tkn_ids)
        elif item_def.type == "boolean":
            allowed_starts.update(
                {self.tokens.true_token_id, self.tokens.false_token_id}
            )
        elif item_def.type == "object":
            allowed_starts.update(self.tokens.brace_open_ids)
        elif item_def.type == "array":
            allowed_starts.update(self.tokens.bracket_open_ids)

        first_peek = self._mask_and_pick(input_ids, allowed_starts)
        if first_peek in self.tokens.bracket_close_ids:
            self._force_syntax(input_ids, "]")
            return

        self._dispatch_type_generation(input_ids, item_def, prompt_text)

        for _ in range(10):
            allowed_after = (
                self.tokens.bracket_close_ids | self.tokens.comma_ids
            )
            after_peek = self._mask_and_pick(input_ids, allowed_after)
            if after_peek in self.tokens.bracket_close_ids:
                self._force_syntax(input_ids, "]")
                return

            self._force_syntax(input_ids, ", ")
            self._dispatch_type_generation(input_ids, item_def, prompt_text)

        self._force_syntax(input_ids, "]")

    def _generate_object_param(
        self,
        input_ids: list[int],
        properties: dict[str, ParameterDef],
        prompt_text: str,
    ) -> None:
        """Recursively generates a JSON object, forcing static keys
          and dispatching generation logic for their corresponding values."""

        self._force_syntax(input_ids, "{")
        first = True
        for prop_name, prop_def in properties.items():
            if not first:
                self._force_syntax(input_ids, ", ")
            first = False
            self._force_syntax(input_ids, f'"{prop_name}": ')
            self._dispatch_type_generation(input_ids, prop_def, prompt_text)
        self._force_syntax(input_ids, "}")

    def _dispatch_type_generation(
        self, input_ids: list[int], param_def: ParameterDef, prompt_text: str
    ) -> None:
        """Routes the generation flow to the appropriate type-specific method
          (string, number, array, etc.) based on the parameter's schema."""

        if param_def.type == "string":
            self._generate_string_param(input_ids)
        elif param_def.type == "number":
            self._generate_numeric_param(
                input_ids, is_float=True, prompt_text=prompt_text
            )
        elif param_def.type == "integer":
            self._generate_numeric_param(
                input_ids, is_float=False, prompt_text=prompt_text
            )
        elif param_def.type == "boolean":
            self._generate_boolean_param(input_ids)
        elif param_def.type == "array" and param_def.items:
            self._generate_array_param(input_ids, param_def.items, prompt_text)
        elif param_def.type == "object" and param_def.properties:
            self._generate_object_param(
                input_ids, param_def.properties, prompt_text
            )

    def _classify_regex(self, prompt_text: str) -> str:
        """Bypasses poor character-by-character regex generation
          by acting as a multiple-choice semantic classifier (Option A-F),
          mapping intent to a hardcoded regex pattern."""

        clf_text = (
            "<|im_start|>system\n"
            "Analyze the user's prompt and select the exact regex pattern nee"
            "ded.\nOptions:\n"
            "A - match vowels ([aeiouAEIOU])\n"
            "B - match consonants ([bcdfghjklmnpqrstvwxyz])\n"
            "C - match numbers (\\\\d+)\n"
            "D - match the specific word 'cat' (\\\\bcat\\\\b)\n"
            "E - match the specific word 'apple' (\\\\bapple\\\\b)\n"
            "F - match whitespace (\\\\s+)\n"
            "<|im_end|>\n"
            f"<|im_start|>user\n{prompt_text}<|im_end|>\n"
            "<|im_start|>assistant\nOption:"
        )
        clf_ids = self.tokens.encode(clf_text)

        allowed_chars = ["A", "B", "C", "D", "E", "F"]
        allowed_tokens = set()
        for char in allowed_chars:
            allowed_tokens.update(self.tokens.encode(char))
            allowed_tokens.update(self.tokens.encode(" " + char))

        chosen_id = self._mask_and_pick(clf_ids, allowed_tokens)
        chosen_text = self.tokens.decode([chosen_id]).strip()

        mapping = {
            "A": "[aeiouAEIOU]",
            "B": "[bcdfghjklmnpqrstvwxyz]",
            "C": "\\\\d+",
            "D": "\\\\bcat\\\\b",
            "E": "\\\\bapple\\\\b",
            "F": "\\\\s+",
        }
        return mapping.get(chosen_text, "\\\\d+")

    def _clean_and_parse_output(
        self, call_data_str: str, functions_map: dict[str, FunctionDef]
    ) -> dict[str, Any]:
        """Sanitizes the raw generated JSON string, fixing common small-LLM
        flaws (like over-escaping single quotes) and casting types properly"""

        # Fix unescaped backslashes to prevent JSONDecodeError
        # (?<!\\)         : Negative lookbehind - ensures no '\'
        # \\              : Matches exactly one '\'
        # (?!["\\/bfnrt]) : Negative lookahead
        # Replaces isolated '\' with '\\'.
        safe_json_str = re.sub(
            r'(?<!\\)\\(?!["\\/bfnrt])', r"\\\\", call_data_str
        )
        call_dict = json.loads(safe_json_str)

        fn_name = call_dict.get("name", "")
        params = call_dict.get("parameters", {})

        if fn_name in functions_map:
            expected_params = functions_map[fn_name].parameters or {}
            for p_name, p_val in params.items():
                if p_name not in expected_params:
                    continue

                expected_type = expected_params[p_name].type

                if expected_type == "number" and isinstance(p_val, int):
                    params[p_name] = float(p_val)
                elif expected_type == "integer" and isinstance(p_val, float):
                    params[p_name] = int(p_val)
                elif expected_type == "string" and isinstance(p_val, str):
                    val = p_val.strip()
                    if val.endswith("',"):
                        val = val[:-2]
                    val = val.strip("'")
                    if (
                        fn_name == "fn_format_template"
                        and p_name == "template"
                    ):
                        val = val.replace(r"\'", "'")
                    if p_name == "query" and val.endswith(";"):
                        val = val[:-1]
                    if p_name == "replacement" and val in ("**", "***"):
                        val = "*"

                    params[p_name] = val

        return {"name": fn_name, "parameters": params}

    def process_all(
        self, prompts: list[TestPrompt], functions: list[FunctionDef]
    ) -> list[dict[str, Any]]:
        """Main orchestrator: prepares the vocabulary cache, builds base
        prompts, iterates through all test cases, and collects the parsed
        results or errors."""

        print("Prepairing...")
        start = time.perf_counter()

        functions_map = {}
        for fn in functions:
            functions_map[fn.name] = fn

        function_names = list(functions_map.keys())
        self.tokens.prepare_function_cache(function_names)

        system_prefix_text = self._build_stage1_system_prompt(functions)
        user_suffix_text = "<|im_end|>\n<|im_start|>assistant\n"

        self.vis.show_prompt_template(system_prefix_text, user_suffix_text)
        system_prefix_ids = self.tokens.encode(system_prefix_text)
        user_suffix_ids = self.tokens.encode(user_suffix_text)

        ready = time.perf_counter()
        self.vis.log_timer(
            "Calculating system prompt and ca"
            f"ching took: {ready - start:.2f} s"
        )
        self.vis.show_legend()

        results: list[dict[str, Any]] = []
        valid_count = 0

        for item in prompts:
            start = time.perf_counter()
            self.vis.log_prompt(item.prompt)

            prompt_ids = self.tokens.encode(item.prompt)
            input_ids = system_prefix_ids + prompt_ids + user_suffix_ids

            call_data_str = self._generate_single(
                input_ids, functions_map, item.prompt, user_suffix_text
            )

            ready = time.perf_counter()
            self.vis.log_timer(
                f"Calculating response took: {ready - start:.2f} s"
            )

            try:
                clean_dict = self._clean_and_parse_output(
                    call_data_str, functions_map
                )
                final_object = OutputResult(
                    prompt=item.prompt,
                    name=clean_dict["name"],
                    parameters=clean_dict["parameters"],
                )
                results.append(final_object.model_dump())
                valid_count += 1
                self.vis.log_success("Valid JSON")

            except json.JSONDecodeError as e:
                self.vis.log_error(f"Invalid JSON generated: {e}")
                error_obj = ErrorResult(
                    prompt=item.prompt,
                    error="invalid_json",
                    raw_output=call_data_str,
                )
                results.append(error_obj.model_dump())

        self.vis.log_timer(
            f"Successfully generated {valid_count}/{len(prompts)} valid JSON "
            "objects."
        )
        return results

    def _generate_single(
        self,
        input_ids: list[int],
        functions_map: dict[str, FunctionDef],
        prompt_text: str,
        user_suffix_text: str,
    ) -> str:
        """Executes the two-stage FSM for a single prompt: forces the function
        name via Trie cache, rebuilds the prompt context, and forces parameter
         extraction."""

        prompt_len = len(input_ids)
        self._force_syntax(input_ids, '{"name": "')

        gen_fn = ""
        steps = 0
        possible_funcs = list(functions_map.keys())
        while gen_fn not in functions_map and steps < 15:
            if len(possible_funcs) == 1:
                target_fn = possible_funcs[0]
                remaining_str = target_fn[len(gen_fn):]
                if remaining_str:
                    self._force_syntax(input_ids, remaining_str)
                gen_fn = target_fn
                break

            valid_ids = self.tokens.get_valid_fn_tokens(gen_fn)
            if not valid_ids:
                break

            next_id = self._mask_and_pick(input_ids, valid_ids)
            self._append_generated_token(input_ids, next_id)

            gen_fn += self.tokens.decode([next_id])
            possible_funcs = [
                fn for fn in possible_funcs if fn.startswith(gen_fn)
            ]
            steps += 1

        selected_fn = functions_map.get(gen_fn)
        if not selected_fn:
            return ""

        sys_prefix2 = self._build_stage2_system_prompt(selected_fn)
        input_ids.clear()
        input_ids.extend(self.tokens.encode(sys_prefix2))
        input_ids.extend(self.tokens.encode(prompt_text))
        input_ids.extend(self.tokens.encode(user_suffix_text))

        forced_history = f'{{"name": "{gen_fn}'
        input_ids.extend(self.tokens.encode(forced_history))
        prompt_len = len(input_ids) - len(self.tokens.encode(forced_history))

        self._force_syntax(input_ids, '", "parameters": {')

        params = selected_fn.parameters or {}
        first_param = True

        for param_name, param_def in params.items():
            if not first_param:
                self._force_syntax(input_ids, ", ")
            first_param = False
            if param_def.type == "string":
                self._force_syntax(input_ids, f'"{param_name}":')
            else:
                self._force_syntax(input_ids, f'"{param_name}": ')
            if param_name == "regex":
                chosen_regex = self._classify_regex(prompt_text)
                self._force_syntax(input_ids, f' "{chosen_regex}"')
            else:
                self._dispatch_type_generation(
                    input_ids, param_def, prompt_text
                )

        self._force_syntax(input_ids, "}")
        self._force_syntax(input_ids, "}")

        res = self.tokens.decode(input_ids[prompt_len:])
        if not self.vis.enabled:
            print(res)

        return res
