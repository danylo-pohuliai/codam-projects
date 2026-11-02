import functools
import operator
from collections.abc import Callable
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0
    operations: dict[str, Callable[[int, int], int]] = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": max,
        "min": min
    }
    if operation not in operations.keys():
        raise ValueError(f"Unknown operation: {operation}")
    return int(functools.reduce(operations[operation], spells))


def partial_enchanter(
        base_enchantment: Callable[..., str]) -> dict[str, Callable[..., str]]:
    return {
        "flame": functools.partial(base_enchantment, 50, "Fire"),
        "frost": functools.partial(base_enchantment, 50, "Ice"),
        "terra": functools.partial(base_enchantment, 50, "Earth")
    }


@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    @functools.singledispatch
    def cast(spell: Any) -> str:
        return "Unknown spell type"

    @cast.register(int)
    def _(spell: int) -> str:
        return f"Damage spell: {spell} damage"

    @cast.register(str)
    def _(spell: str) -> str:
        return f"Enchantment: {spell}"

    @cast.register(list)
    def _(spell: list[Any]) -> str:
        return f"Multi-cast: {len(spell)} spells"
    return cast


if __name__ == "__main__":
    spells_list = [20, 30, 10, 40]

    print("\nTesting spell reducer...")
    print(f"Sum: {spell_reducer(spells_list, 'add')}")
    print(f"Product: {spell_reducer(spells_list, 'multiply')}")
    print(f"Max: {spell_reducer(spells_list, 'max')}\n")

    print("Testing partial enchanter...")

    def base_enchantment(power: int, element: str, target: str) -> str:
        return f"Enchanted {target} with {element}, the power is {power}"
    items = partial_enchanter(base_enchantment)
    for item in items.keys():
        print(f"{item}: {items[item]("Sword")}")

    print("\nTesting memoized fibonacci...")
    print(f"Fib(0): {memoized_fibonacci(0)}")
    print(f"Fib(1): {memoized_fibonacci(1)}")
    print(f"Fib(10): {memoized_fibonacci(10)}")
    print(f"Fib(15): {memoized_fibonacci(15)}\n")

    print("Testing spell dispatcher...")
    dispatch = spell_dispatcher()
    print(dispatch(42))
    print(dispatch("fireball"))
    print(dispatch(["fireball", "freeze", "heal"]))
    print(dispatch(3.14))
