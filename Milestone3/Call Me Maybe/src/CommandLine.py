import argparse
from pydantic import BaseModel, Field

MODEL_ALIASES: dict[str, str] = {
    "qwen3": "Qwen/Qwen3-0.6B",
    "qwen2.5-0.5b": "Qwen/Qwen2.5-0.5B-Instruct",
    "qwen2.5-1.5b": "Qwen/Qwen2.5-1.5B-Instruct",
    "qwen1.5-0.5b": "Qwen/Qwen1.5-0.5B-Chat",
    "smol": "HuggingFaceTB/SmolLM2-360M-Instruct",
    "smol-135": "HuggingFaceTB/SmolLM2-135M-Instruct",
}


class AppConfig(BaseModel):
    functions_definition: str = Field(min_length=1)
    input: str = Field(min_length=1)
    output: str = Field(min_length=1)
    model_path: str = Field(min_length=1)
    fast_forward: bool
    visualisation: bool


def parse_arguments() -> AppConfig:
    """Parses CLI arguments and resolves model aliases."""
    parser = argparse.ArgumentParser(
        description="Constrained decoding function caller"
    )

    parser.add_argument(
        "--functions_definition",
        type=str,
        default="data/input/functions_definition.json",
        help="Path to the JSON file containing function schemas.",
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/input/function_calling_tests.json",
        help="Path to the input JSON file containing test prompts.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/output/function_calling_results.json",
        help="Path where the generated JSON results will be saved.",
    )

    alias_keys = list(MODEL_ALIASES.keys())
    parser.add_argument(
        "--model",
        type=str,
        default="qwen3",
        choices=alias_keys,
        help=f"Target model alias. Available options: {', '.join(alias_keys)}",
    )
    parser.add_argument(
        "--fast_forward",
        action="store_true",
        help="Enable fast-forwarding to skip LLM for static syntax.",
    )
    parser.add_argument(
        "--visualisation",
        action="store_true",
        help="Enable real-time colored terminal token visualization.",
    )

    args = parser.parse_args()
    model_path = MODEL_ALIASES[args.model.lower()]

    return AppConfig(
        functions_definition=args.functions_definition,
        input=args.input,
        output=args.output,
        model_path=model_path,
        fast_forward=args.fast_forward,
        visualisation=args.visualisation,
    )
