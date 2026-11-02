import random

achievements = [
    'Crafting Genius', 'World Savior', 'Master Explorer', 'Collector Supreme',
    'Untouchable', 'Boss Slayer', 'Strategist', 'Speed Runner',
    'Survivor', 'Treasure Hunter', 'First Steps', 'Sharp Mind',
    'Unstoppable', 'Hidden Path Finder'
]


def gen_player_achievements() -> set[str]:
    num_achievements = random.randint(6, 12)
    chosen = random.sample(achievements, num_achievements)
    return set(chosen)


if __name__ == "__main__":
    print("=== Achievement Tracker System ===\n")
    players = ["Alice", "Bob", "Charlie", "Dylan"]
    p_sets = {}

    for p in players:
        p_sets[p] = gen_player_achievements()
        print(f"Player {p}: {p_sets[p]}")

    all_distinct: set[str] = set()
    for s in p_sets.values():
        all_distinct = all_distinct.union(s)
    print(f"All distinct achievements: {all_distinct}")

    common = set(p_sets[players[0]])
    for s in p_sets.values():
        common = common.intersection(s)
    print(f"\nCommon achievements: {common}\n")

    for p in players:
        unique_to_player = set(p_sets[p])
        for other_p in players:
            if p != other_p:
                unique_to_player = unique_to_player.difference(p_sets[other_p])
        print(f"Only {p} has: {unique_to_player}")
    print("")
    master_set = set(achievements)
    for p in players:
        missing = master_set.difference(p_sets[p])
        print(f"{p} is missing: {missing}")
