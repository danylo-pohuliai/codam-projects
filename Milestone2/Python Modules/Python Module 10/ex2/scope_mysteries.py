from collections.abc import Callable
from typing import Any


def mage_counter() -> Callable[[], int]:
    call_amount = 0

    def func() -> int:
        nonlocal call_amount
        call_amount += 1
        return call_amount
    return func


def spell_accumulator(initial_power: int) -> Callable[[int], int]:
    power = initial_power

    def func(power_to_add: int) -> int:
        nonlocal power
        power += power_to_add
        return power
    return func


def enchantment_factory(enchantment_type: str) -> Callable[[str], str]:

    def func(item_name: str) -> str:
        return enchantment_type + " " + item_name
    return func


def memory_vault() -> dict[str, Callable[..., Any]]:
    vault: dict[str, Any] = {}

    def store(key: str, value: Any) -> None:
        vault[key] = value

    def recall(key: str) -> Any:
        return vault.get(key, "Memory not found")
    return {'store': store, 'recall': recall}


if __name__ == "__main__":
    print("\nTesting mage counter...")
    counter_a = mage_counter()
    counter_b = mage_counter()
    print(f"counter_a call 1: {counter_a()}")
    print(f"counter_a call 2: {counter_a()}")
    print(f"counter_b call 1: {counter_b()}")

    print("\nTesting spell accumulator...")
    acc = spell_accumulator(100)
    print(f"Base 100, add 20: {acc(20)}")
    print(f"Base 100, add 30: {acc(30)}")

    print("\nTesting enchantment factory...")
    flaming = enchantment_factory("Flaming")
    frozen = enchantment_factory("Frozen")
    print(flaming("Sword"))
    print(frozen("Shield"))

    print("\nTesting memory vault...")
    vault1 = memory_vault()
    store = vault1['store']
    recall = vault1['recall']
    print("Store 'secret' = 42")
    store('secret', 42)
    print(f"Recall 'secret': {recall('secret')}")
    print(f"Recall 'unknown': {recall('unknown')}")
