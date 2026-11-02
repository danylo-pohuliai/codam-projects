from collections.abc import Callable


def heal(target: str, power: int) -> str:
    return f"Heal restores {target} for {power} HP"


def fireball(target: str, power: int) -> str:
    return f"Fireball damages {target} for {power} HP"


def freeze(target: str, power: int) -> str:
    return f"Freeze encases {target} in ice, slowing them by {power}%"


def curse(target: str, power: int) -> str:
    return f"Curse drains {target}'s vitality by {power} points"


def spell_combiner(
        spell1: Callable[[str, int], str],
        spell2: Callable[[str, int], str]
        ) -> Callable[[str, int], tuple[str, str]]:
    def new_spell(target: str, power: int) -> tuple[str, str]:
        res1 = spell1(target, power)
        res2 = spell2(target, power)
        return (res1, res2)
    return new_spell


def power_amplifier(
        base_spell: Callable[[str, int], str],
        multiplier: int) -> Callable[[str, int], str]:
    def func(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)
    return func


def conditional_caster(
        condition: Callable[[str, int], bool],
        spell: Callable[[str, int], str]) -> Callable[[str, int], str]:
    def new_spell(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        else:
            return "Spell fizzled"
    return new_spell


def spell_sequence(
        spells: list[Callable[[str, int], str]]
        ) -> Callable[[str, int], list[str]]:
    def cast_all(target: str, power: int) -> list[str]:
        res = []
        for spell in spells:
            res.append(spell(target, power))
        return res
    return cast_all


if __name__ == "__main__":
    test_values = [9, 17, 12]
    test_targets = ['Dragon', 'Goblin', 'Wizard', 'Knight']

    print("Testing spell combiner...")
    fire_and_ice = spell_combiner(fireball, freeze)
    print(fire_and_ice(test_targets[0], test_values[1]))

    print("\nTesting power amplifier...")
    mega_heal = power_amplifier(heal, 3)
    print(f"Original: {heal(test_targets[2], test_values[0])}")
    print(f"Amplified: {mega_heal(test_targets[2], test_values[0])}")

    print("\nTesting conditional caster...")

    def is_goblin(target: str, power: int) -> bool:
        return target == 'Goblin'
    anti_goblin_curse = conditional_caster(is_goblin, curse)
    print(f"Targeting Goblin: "
          f"{anti_goblin_curse(test_targets[1], test_values[2])}")
    print(f"Targeting Knight: "
          f"{anti_goblin_curse(test_targets[3], test_values[2])}")

    print("\nTesting spell sequence...")
    ultimate_combo = spell_sequence([curse, fireball, freeze, heal])
    combo_results = ultimate_combo(test_targets[3], test_values[2])
    for result in combo_results:
        print(result)
