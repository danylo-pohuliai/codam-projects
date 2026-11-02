class TerminalVisualizer:
    """Handles all UI formatting, ANSI colors, and console output"""

    COLORS = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "syntax": "\033[96m",
        "llm": "\033[92m",
        "timer": "\033[93m",
        "prompt": "\033[95m",
        "success": "\033[92m",
        "error": "\033[91m",
    }

    def __init__(self, enabled: bool = False):
        self.enabled = enabled

    def _print(self, text: str, color_key: str) -> None:
        if not self.enabled:
            return
        prefix = self.COLORS.get(color_key, "")
        print(f"{prefix}{text}{self.COLORS['reset']}", end="", flush=True)

    def emit_syntax(self, text: str) -> None:
        self._print(text, "syntax")

    def emit_llm_token(self, text: str) -> None:
        self._print(text, "llm")

    def log_timer(self, msg: str) -> None:
        if self.enabled:
            print(f"\n{self.COLORS['timer']}{msg}{self.COLORS['reset']}\n")

    def log_prompt(self, msg: str) -> None:
        if self.enabled:
            print(
                f"{self.COLORS['prompt']}Sending "
                f"prompt:{self.COLORS['reset']} {msg}"
            )

    def show_legend(self) -> None:
        if self.enabled:
            print(
                f"\n{self.COLORS['bold']}=== LEGEND ==={self.COLORS['reset']}"
            )
            print(
                f"{self.COLORS['syntax']}CYAN: Fast-Forwarding "
                f"(Forced Schema){self.COLORS['reset']}"
            )
            print(
                f"{self.COLORS['llm']}GREEN: Constrained Decoding"
                f" (LLM Choices){self.COLORS['reset']}"
            )
            print(
                f"{self.COLORS['bold']}=============={self.COLORS['reset']}\n"
            )

    def show_prompt_template(
        self, system_prefix: str, suffix_text: str
    ) -> None:
        if self.enabled:
            print(
                f"\n{self.COLORS['bold']}=== FULL PROMPT "
                f"TEMPLATE ==={self.COLORS['reset']}"
            )

            full_template = (
                f"{system_prefix}"
                f"{self.COLORS['prompt']}{{user pro"
                f"mpt here}}{self.COLORS['reset']}\n"
                f"{suffix_text}"
            )

            print(full_template.strip())
            print(
                f"\n{self.COLORS['bold']}==============="
                f"============={self.COLORS['reset']}\n"
            )

    def log_success(self, msg: str) -> None:
        if self.enabled:
            print(f"{self.COLORS['success']}✔ {msg}{self.COLORS['reset']}\n")

    def log_error(self, msg: str) -> None:
        if self.enabled:
            print(f"{self.COLORS['error']}✖ {msg}{self.COLORS['reset']}\n")
