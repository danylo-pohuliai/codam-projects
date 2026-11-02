import time
import functools
from collections.abc import Callable
from typing import Any


def spell_timer(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper() -> Any:
        print(f"Casting {func.__name__}...")
        start_time = time.time()
        result = func()
        end_time = time.time()
        print(f"Spell completed in {end_time - start_time:.3f} seconds")
        return result
    return wrapper


def power_validator(min_power: int) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if len(args) == 1:
                power = args[0]
            else:
                power = args[2]
            if not isinstance(power, (int, float)) or power < min_power:
                return "Insufficient power for this spell"
            return func(*args, **kwargs)
        return wrapper
    return decorator


def retry_spell(max_attempts: int) -> Callable[..., Callable[..., str]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    print("Spell failed, retrying... "
                          f"(attempt {attempt}/{max_attempts})")
                    time.sleep(0.1)
            return f"Spell casting failed after {max_attempts} attempts"
        return wrapper
    return decorator


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        if len(name) < 3:
            return False
        return all(c.isalpha() or c.isspace() for c in name)

    @power_validator(min_power=10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


if __name__ == "__main__":
    print("\nTesting spell timer...")

    @spell_timer
    def fireball() -> str:
        time.sleep(0.101)
        return "Result: Fireball cast!"
    print(fireball())
    print("\nTesting power validator for standart function...")

    @power_validator(min_power=15)
    def cast(power: int) -> str:
        return f"Casting spell with power {power}"
    print(cast(20))
    print(cast(3))
    print()

    @retry_spell(max_attempts=3)
    def failing_spell() -> None:
        raise ValueError

    @retry_spell(max_attempts=3)
    def not_failing_spell() -> str:
        return "Waaaaaaagh spelled !"

    print(failing_spell())
    print(not_failing_spell())

    print("\nTesting MageGuild...")
    print(MageGuild.validate_mage_name("Gandalf the Grey"))
    print(MageGuild.validate_mage_name("42"))
    guild = MageGuild()
    print(guild.cast_spell("Lightning", 15))
    print(guild.cast_spell("Spark", 5))
