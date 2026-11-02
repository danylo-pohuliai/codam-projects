from ex0 import FlameFactory, AquaFactory, CreatureFactory


def verify(factory: CreatureFactory) -> None:
    print("Testing factory")
    if isinstance(factory, CreatureFactory):
        creature = factory.create_base()
        print(creature.describe() + "\n" + creature.attack())
        creature = factory.create_evolved()
        print(creature.describe() + "\n" + creature.attack())
        print()


def fight(fl_fact: FlameFactory, aq_fact: AquaFactory) -> None:
    flameling = fl_fact.create_base()
    aquabub = aq_fact.create_base()
    print(f"Testing battle\n{flameling.describe()}\n vs.")
    print(aquabub.describe() + "\n fight!")
    print(flameling.attack() + "\n" + aquabub.attack())


if __name__ == "__main__":
    fl_fact = FlameFactory()
    aq_fact = AquaFactory()
    verify(fl_fact)
    verify(aq_fact)
    fight(fl_fact, aq_fact)
