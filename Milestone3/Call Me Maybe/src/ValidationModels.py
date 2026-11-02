import json
from typing import Optional, Literal, Any
from pydantic import BaseModel, Field, model_validator, ValidationError


class TestPrompt(BaseModel):
    prompt: str = Field(..., max_length=200, description="User prompt text")


class ParameterDef(BaseModel):
    type: Literal["string", "number", "integer", "boolean", "array", "object"]
    description: Optional[str] = Field(None, max_length=200)
    properties: Optional[dict[str, "ParameterDef"]] = None
    items: Optional["ParameterDef"] = None


class ReturnDef(BaseModel):
    type: Literal["string", "number", "integer", "boolean", "array", "object"]
    description: Optional[str] = Field(None, max_length=200)
    properties: Optional[dict[str, ParameterDef]] = None
    items: Optional[ParameterDef] = None


class FunctionDef(BaseModel):
    name: str = Field(..., max_length=64, pattern=r"^[a-zA-Z0-9_]+$")
    description: str = Field(..., max_length=500)
    parameters: Optional[dict[str, ParameterDef]] = Field(default_factory=dict)
    returns: Optional[ReturnDef] = None

    @model_validator(mode="after")
    def validate_nesting_depth(self) -> "FunctionDef":
        MAX_DEPTH = 4

        def get_depth(param: ParameterDef) -> int:
            child_depths = [0]
            if param.properties:
                child_depths.extend(
                    get_depth(p) for p in param.properties.values()
                )
            if param.items:
                child_depths.append(get_depth(param.items))
            return 1 + max(child_depths)

        if self.parameters is None:
            self.parameters = {}
        for p_name, p_def in self.parameters.items():
            depth = get_depth(p_def)
            if depth > MAX_DEPTH:
                raise ValueError(
                    f"Parameter '{p_name}' exceeds maximum nesting depth of "
                    f"{MAX_DEPTH} (current: {depth})."
                )

        return self


class OutputResult(BaseModel):
    prompt: str = Field(..., description="The original user prompt")
    name: str = Field(..., description="The generated function name")
    parameters: dict[str, Any] = Field(
        default_factory=dict, description="The extracted parameters"
    )


class ErrorResult(BaseModel):
    prompt: str
    error: str
    raw_output: str


ParameterDef.model_rebuild()


def load_function_definitions(filepath: str) -> list[FunctionDef]:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        validated_data = [FunctionDef(**item) for item in raw_data]
        return validated_data
    except FileNotFoundError:
        raise RuntimeError(f"File not found: {filepath}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON in {filepath}: {e}")
    except ValidationError as e:
        raise RuntimeError(f"JSON schema mismatch in {filepath}: {e}")


def load_prompts(filepath: str) -> list[TestPrompt]:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        return [TestPrompt(**item) for item in raw_data]
    except FileNotFoundError:
        raise RuntimeError(f"File not found: {filepath}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON in {filepath}: {e}")
    except ValidationError as e:
        raise RuntimeError(f"JSON schema mismatch in {filepath}: {e}")
