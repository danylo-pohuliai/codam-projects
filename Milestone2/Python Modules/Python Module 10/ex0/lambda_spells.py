from typing import Any


def artifact_sorter(artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(artifacts, key=lambda x: x["power"], reverse=True)


def power_filter(
        mages: list[dict[str, Any]],
        min_power: int) -> list[dict[str, Any]]:
    return list(filter(lambda x: x["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda x: "* " + x + " *", spells))


def mage_stats(mages: list[dict[str, Any]]) -> dict[str, Any]:
    max_power = max(mages, key=lambda x: x["power"])["power"]
    min_power = min(mages, key=lambda x: x["power"])["power"]
    avg_power = round(sum(map(lambda x: x["power"], mages)) / len(mages), 2)
    return {
        'max_power': max_power,
        'min_power': min_power,
        'avg_power': avg_power
        }


if __name__ == "__main__":
    artifacts = [
        {'name': 'Earth Shield', 'power': 92, 'type': 'accessory'},
        {'name': 'Shadow Blade', 'power': 94, 'type': 'relic'},
        {'name': 'Storm Crown', 'power': 119, 'type': 'weapon'},
        {'name': 'Crystal Orb', 'power': 95, 'type': 'armor'},
        ]
    mages = [
        {'name': 'River', 'power': 85, 'element': 'earth'},
        {'name': 'Jordan', 'power': 60, 'element': 'ice'},
        {'name': 'Rowan', 'power': 79, 'element': 'light'},
        {'name': 'Luna', 'power': 97, 'element': 'shadow'},
        {'name': 'Sage', 'power': 57, 'element': 'light'}
        ]
    spells = ['freeze', 'darkness', 'shield', 'earthquake']
    print("\nTesting artifact sorter...")
    list(map(lambda x: print(f"{x}"), artifact_sorter(artifacts)))
    print("\nTesting power filter...")
    list(map(lambda x: print(f"{x}"), power_filter(mages, 75)))
    print("\nTesting spell transformer...")
    list(map(lambda x: print(f"{x}"), spell_transformer(spells)))
    print("\nTesting mage stats...")
    print(mage_stats(mages))
