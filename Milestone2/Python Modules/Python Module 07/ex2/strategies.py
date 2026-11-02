from abc import ABC, abstractmethod
from ex0.creatures import Creature
from ex1.capabilities import HealCapability, TransformCapability
from typing import Any


class BattleStrategy(ABC):
    @abstractmethod
    def act(self, creature: Any) -> str: ...

    @abstractmethod
    def is_valid(self, creature: Any) -> bool: ...


class NormalStrategy(BattleStrategy):
    def act(self, creature: Any) -> str:
        if self.is_valid(creature):
            return str(creature.attack())
        else:
            raise Exception("This creature is invalid for NormalStrategy")

    def is_valid(self, creature: Any) -> bool:
        if isinstance(creature, Creature):
            return True
        else:
            return False


class AggressiveStrategy(BattleStrategy):
    def act(self, creature: Any) -> str:
        if self.is_valid(creature):
            return str(creature.transform() + "\n"
                       + creature.attack() + "\n"
                       + creature.revert())
        else:
            raise Exception("This creature is invalid for AggressiveStrategy")

    def is_valid(self, creature: Any) -> bool:
        if isinstance(creature, Creature) \
           and isinstance(creature, TransformCapability):
            return True
        else:
            return False


class DefensiveStrategy(BattleStrategy):
    def act(self, creature: Any) -> str:
        if self.is_valid(creature):
            return str(creature.attack() + "\n" + creature.heal())
        else:
            raise Exception("This creature is invalid for DefensiveStrategy")

    def is_valid(self, creature: Any) -> bool:
        if isinstance(creature, Creature) \
           and isinstance(creature, HealCapability):
            return True
        else:
            return False
