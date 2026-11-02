from ex0 import FlameFactory, AquaFactory, CreatureFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import NormalStrategy, AggressiveStrategy, DefensiveStrategy
from ex2.strategies import BattleStrategy


def battle(opponents: list[tuple[CreatureFactory, BattleStrategy]]) -> None:
    print("*** Tournament ***")
    amount = len(opponents)
    print(f"{amount} opponents involved\n")
    for i in range(amount):
        for j in range(i + 1, amount):
            f1, s1 = opponents[i]
            f2, s2 = opponents[j]

            cr1 = f1.create_base()
            cr2 = f2.create_base()

            print("* Battle *\n" + cr1.describe() + "\n vs.")
            print(cr2.describe() + "\n now fight!")
            try:
                print(s1.act(creature=cr1))
                print(s2.act(creature=cr2) + "\n")
            except Exception as e:
                print(f"Battle error, aborting tournament: {e}\n")
                return


if __name__ == "__main__":
    print("Tournament 0 (basic)")
    print(" [ (Flameling+Normal), (Healing+Defensive) ]")
    battle([(FlameFactory(), NormalStrategy()),
            (HealingCreatureFactory(), DefensiveStrategy())])
    print("Tournament 1 (error)")
    print(" [ (Flameling+Aggressive), (Healing+Defensive) ]")
    battle([(FlameFactory(), AggressiveStrategy()),
            (HealingCreatureFactory(), DefensiveStrategy())])
    print("Tournament 2 (multiple)")
    print(" [ (Aquabub+Normal), (Healing+Defensive), (Transform+Aggressive) ]")
    battle([(AquaFactory(), NormalStrategy()),
            (HealingCreatureFactory(), DefensiveStrategy()),
            (TransformCreatureFactory(), AggressiveStrategy())])
