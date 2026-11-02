import json
from functools import lru_cache
from typing import Protocol, Any


class LLMProtocol(Protocol):
    def get_path_to_vocab_file(self) -> str: ...
    def get_path_to_merges_file(self) -> str: ...
    def encode(self, text: str) -> Any: ...
    def decode(self, ids: list[int]) -> str: ...

    def get_logits_from_input_ids(self, input_ids: list[int]) -> list[float]:
        pass


class TokenManager:
    """Manages vocabulary, token filtering, and prefix caching."""

    def __init__(self, model: LLMProtocol) -> None:
        self.model = model
        self._fn_cache: dict[str, set[int]] = {}

        with open(
            self.model.get_path_to_vocab_file(), "r", encoding="utf-8"
        ) as f:
            self.vocab = json.load(f)

        self.id_to_token = {}
        for token, token_id in self.vocab.items():
            self.id_to_token[token_id] = token

        self.bpe_ranks: dict[tuple[str, str], int] = {}
        self._load_bpe_merges()

        self.qt_tkn_ids: set[int] = set()
        self.txt_tkn_ids: set[int] = set()
        self.num_tkn_ids: set[int] = set()
        self.int_tkn_ids: set[int] = set()
        self.delr_ids: set[int] = set()
        self.bracket_close_ids: set[int] = set()
        self.bracket_open_ids: set[int] = set()
        self.brace_open_ids: set[int] = set()
        self.comma_ids: set[int] = set()

        self._init_token_filters()

        self.txt_with_qt_ids = self.txt_tkn_ids | self.qt_tkn_ids
        self.dgt_with_delr_ids = self.num_tkn_ids | self.delr_ids
        self.int_with_delr_ids = self.int_tkn_ids | self.delr_ids
        self.true_token_id = self.encode("true")[0]
        self.false_token_id = self.encode("false")[0]

    def _load_bpe_merges(self) -> None:
        """Reads merges.txt and builds the bpe_ranks dictionary."""
        try:
            with open(
                self.model.get_path_to_merges_file(), "r", encoding="utf-8"
            ) as f:
                bpe_data = f.read().split("\n")

            start_idx = 1 if bpe_data and bpe_data[0].startswith("#") else 0

            for i, line in enumerate(bpe_data[start_idx:]):
                parts = line.strip().split()
                if len(parts) == 2:
                    self.bpe_ranks[(parts[0], parts[1])] = i
        except Exception as e:
            print(f"[Warning] Could not load merges.txt: {e}")

    def _init_token_filters(self) -> None:
        """
        Parses the raw vocabulary once at startup to group tokens by type.
        Creates fast lookup sets for digits, strings, and JSON delimiters,
        used during parameter generation to restrict LLM choices.
        """
        valid_num_chars = set("0123456789.-")
        valid_int_chars = set("0123456789-")
        delimiters = set(",}\n ]")

        for raw_token, token_id in self.vocab.items():
            clean_token = raw_token.replace("Ġ", "").strip()

            if clean_token.startswith('"'):
                self.qt_tkn_ids.add(token_id)
            elif clean_token == '\\"':
                self.txt_tkn_ids.add(token_id)
            elif '"' not in raw_token and "\n" not in raw_token:
                self.txt_tkn_ids.add(token_id)

            if clean_token == "]":
                self.bracket_close_ids.add(token_id)
            elif clean_token == "[":
                self.bracket_open_ids.add(token_id)
            elif clean_token == "{":
                self.brace_open_ids.add(token_id)
            elif clean_token == ",":
                self.comma_ids.add(token_id)

            if clean_token:
                token_chars = set(clean_token)
                if token_chars <= valid_num_chars:
                    self.num_tkn_ids.add(token_id)
                    if token_chars <= valid_int_chars:
                        self.int_tkn_ids.add(token_id)

            if set(raw_token.replace("Ġ", " ")) & delimiters:
                self.delr_ids.add(token_id)

    def prepare_function_cache(self, function_names: list[str]) -> None:
        """
        Builds a prefix cache (Trie) for all valid function names.

        This O(1) lookup table allows the generator to instantly know which
        vocabulary tokens can legally follow the currently generated string.
        It prevents the LLM from hallucinating invalid function names.
        """
        self._fn_cache.clear()

        valid_prefixes = {""}
        valid_substrings = set()

        for name in function_names:
            for i in range(len(name) + 1):
                valid_prefixes.add(name[:i])
                for j in range(i + 1, len(name) + 1):
                    valid_substrings.add(name[i:j])

        for raw_token, token_id in self.vocab.items():
            clean_token = raw_token.replace("Ġ", " ").replace("Ċ", "\n")
            if not clean_token:
                continue
            if clean_token not in valid_substrings:
                continue

            for prefix in valid_prefixes:
                candidate = prefix + clean_token

                if candidate in valid_prefixes:
                    if prefix not in self._fn_cache:
                        self._fn_cache[prefix] = set()
                    self._fn_cache[prefix].add(token_id)

    def get_valid_fn_tokens(self, accumulated: str) -> set[int]:
        return self._fn_cache.get(accumulated, set())

    @lru_cache(maxsize=256)
    def _encode_to_tuple(self, text: str) -> tuple[int, ...]:
        """Performs true Byte-Pair Encoding using ranks from merges.txt."""
        prepared = text.replace(" ", "Ġ").replace("\n", "Ċ")
        tokens = [c for c in prepared]

        while len(tokens) > 1:
            best_rank = float("inf")
            best_pair_idx = -1

            for i in range(len(tokens) - 1):
                pair = (tokens[i], tokens[i + 1])
                rank = self.bpe_ranks.get(pair)
                if rank is not None and rank < best_rank:
                    best_rank = rank
                    best_pair_idx = i

            if best_pair_idx == -1:
                break

            best_pair = (tokens[best_pair_idx], tokens[best_pair_idx + 1])
            merged_token = best_pair[0] + best_pair[1]

            new_tokens = []
            i = 0
            while i < len(tokens):
                if (
                    i < len(tokens) - 1
                    and (tokens[i], tokens[i + 1]) == best_pair
                ):
                    new_tokens.append(merged_token)
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1
            tokens = new_tokens

        return tuple(self.vocab.get(t, 0) for t in tokens)

    def encode(self, text: str) -> list[int]:
        """
        Public encoder method.
        Creates a fresh mutable list from the cached tuple.
        """
        return list(self._encode_to_tuple(text))

    def decode(self, token_ids: list[int]) -> str:
        text = "".join(self.id_to_token.get(tid, "") for tid in token_ids)
        return text.replace("Ġ", " ").replace("Ċ", "\n")
