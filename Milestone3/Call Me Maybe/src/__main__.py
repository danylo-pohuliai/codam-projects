import sys
import json
import time
from pathlib import Path

from .CommandLine import parse_arguments
from .ValidationModels import load_function_definitions, load_prompts
from .TokenManager import TokenManager
from .TerminalVisualizer import TerminalVisualizer
from .ConstrainedGenerator import ConstrainedGenerator


def main() -> None:
    config = parse_arguments()

    input_path = Path(config.input)
    def_path = Path(config.functions_definition)
    output_path = Path(config.output)

    if not def_path.is_file():
        raise FileNotFoundError(
            f"Functions definition file not found: {def_path}"
        )
    if not input_path.is_file():
        raise FileNotFoundError(f"Input prompts file not found: {input_path}")
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "a", encoding="utf-8"):
            pass
    except PermissionError:
        raise PermissionError(f"Do not have permission: {output_path}")
    except OSError as e:
        raise ValueError(f"Invalid output path '{output_path}': {e}")
    print(f"Reading definitions from: {def_path}")
    print(f"Reading prompts from: {input_path}")
    print(f"Writing results to: {output_path}")
    print(f"Using model target: {config.model_path}")

    prompts = load_prompts(str(input_path))
    if len(prompts) < 1:
        raise ValueError("File with prompts should contain at least 1 prompt")
    functions = load_function_definitions(str(def_path))
    if len(functions) < 1:
        raise ValueError("File with functions should contain at least 1 func")

    print("Importing and initialising model...")
    init_start = time.perf_counter()

    try:
        from llm_sdk import Small_LLM_Model
    except ImportError:
        raise ImportError(
            "Could not import 'llm_sdk'. Ensure the 'llm_sdk' directory "
            "is placed correctly in the project root."
        )

    llm = Small_LLM_Model(model_name=config.model_path)
    token_mgr = TokenManager(llm)
    visualizer = TerminalVisualizer(enabled=config.visualisation)

    generator = ConstrainedGenerator(
        model=llm,
        token_mgr=token_mgr,
        visualizer=visualizer,
        fast_forwarding=config.fast_forward,
    )

    print(f"Model ready in: {time.perf_counter() - init_start:.2f} s")

    gen_start = time.perf_counter()
    results = generator.process_all(prompts, functions)
    total_gen_time = time.perf_counter() - gen_start

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    except PermissionError:
        raise PermissionError(
            f"Do not have permission to write to: {output_path}"
        )
    except OSError as e:
        raise RuntimeError(f"Failed to save output file: {e}")

    mins = int(total_gen_time // 60)
    secs = total_gen_time % 60
    print(f"\nProcessing time: {mins} mins, {secs:.2f} secs")
    print(f"Results saved to: {output_path}")


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, ImportError, PermissionError, ValueError) as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[INFO] Process interrupted by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n[FATAL] Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
