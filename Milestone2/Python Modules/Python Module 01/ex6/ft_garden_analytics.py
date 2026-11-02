from typing import Self


class Plant:
    def __init__(self, name: str, height: float, age: int):
        self.name = name
        if height < 0:
            print(f"{self.name}: Error, height can't be negative")
            self._height = 0.0
        else:
            self._height = height
        if age < 0:
            print(f"{self.name}: Error, age can't be negative")
            self._age_in_days = 0
        else:
            self._age_in_days = age
        self.progress = 0.0
        self._stat = self.Statistic()

    def show(self) -> None:
        print(
            f"{self.name}: {self._height:.1f}cm,"
            f" {self._age_in_days} days old"
            )
        self._stat.inc_show()

    def grow(self) -> None:
        if (self.name == "Rose"):
            self._height = self._height + 8.0
            self.progress = self.progress + 8.0
        elif (self.name == "Sunflower"):
            self._height = self._height + 30.0
            self.progress = self.progress + 30.0
        elif (self.name == "Cactus"):
            self._height = self._height + 1.4
            self.progress = self.progress + 1.4
        else:
            self._height = self._height + 2.1
            self.progress = self.progress + 2.1
        self._stat.inc_grow()

    def age(self) -> None:
        self._age_in_days = self._age_in_days + 1
        self._stat.inc_age()

    def set_height(self, value: float) -> None:
        if value < 0:
            print(f"{self.name}: Error, height can't be negative")
            print("Height update rejected")
        else:
            self._height = value
            print(f"Height updated: {round(self.get_height())}cm")

    def set_age(self, value: int) -> None:
        if value < 0:
            print(f"{self.name}: Error, age can't be negative")
            print("Age update rejected")
        else:
            self._age_in_days = value
            print(f"Age updated: {self.get_age()} days")

    def get_height(self) -> float:
        return (self._height)

    def get_age(self) -> int:
        return (self._age_in_days)

    @staticmethod
    def is_year(days: int) -> bool:
        return days > 365

    @classmethod
    def create_anonymous(cls) -> Self:
        return cls("Unknown plant", 0.0, 0)

    class Statistic:
        def __init__(
                self,
                grow_amount: int = 0,
                age_amount: int = 0,
                show_amount: int = 0
                ):
            self._grow_amount = grow_amount
            self._age_amount = age_amount
            self._show_amount = show_amount

        def inc_grow(self) -> None:
            self._grow_amount += 1

        def inc_age(self) -> None:
            self._age_amount += 1

        def inc_show(self) -> None:
            self._show_amount += 1

        def _show_stat(self) -> None:
            print(
                f"Stats: {self._grow_amount} grow, {self._age_amount}"
                f" age, {self._show_amount} show"
                )

    def get_stat(self) -> None:
        self._stat._show_stat()


class Flower(Plant):
    def __init__(self, name: str, height: float, age: int, color: str):
        super().__init__(name, height, age)
        self.color = color
        self.bloomed = False

    def bloom(self) -> None:
        self.bloomed = True

    def show(self) -> None:
        super().show()
        print(f" Color: {self.color}")
        if self.bloomed:
            print(f" {self.name} is blooming beautifully!")
        else:
            print(f" {self.name} has not bloomed yet")


class Tree(Plant):
    class Statistic(Plant.Statistic):
        def __init__(
                self,
                grow_amount: int = 0,
                age_amount: int = 0,
                show_amount: int = 0,
                shade_amount: int = 0
                ):
            super().__init__(grow_amount, age_amount, show_amount)
            self._shade_amount = shade_amount

        def inc_shade(self) -> None:
            self._shade_amount += 1

        def _show_stat(self) -> None:
            super()._show_stat()
            print(f" {self._shade_amount} shade")

    def __init__(
            self,
            name: str,
            height: float,
            age: int,
            trunk_diameter: float):
        super().__init__(name, height, age)
        self.trunk_diameter = trunk_diameter
        self._stat: Tree.Statistic = self._stat

    def produce_shade(self) -> None:
        print(
            f"Tree {self.name} now produces a shade"
            f" of {self.get_height()}cm long and {self.trunk_diameter}cm wide."
            )
        self._stat.inc_shade()

    def show(self) -> None:
        super().show()
        print(f" Trunk diameter: {self.trunk_diameter}cm")


class Seed(Flower):
    def __init__(self, name: str, height: float, age: int, color: str):
        super().__init__(name, height, age, color)
        self.seeds_amount = 0

    def bloom(self) -> None:
        super().bloom()
        self.seeds_amount = 42

    def show(self) -> None:
        super().show()
        print(f" Seeds: {self.seeds_amount}")

    def age(self) -> None:
        super().age()
        self._age_in_days += 19


def print_statistic(plant: Plant) -> None:
    print(f"[statistics for {plant.name}]")
    plant.get_stat()


if __name__ == "__main__":
    print("=== Garden statistics ===\n=== Check year-old")
    rose = Flower("Rose", 15.0, 10, "red")
    print(f"Is 30 days more than a year? -> {rose.is_year(30)}")
    print(f"Is 400 days more than a year? -> {rose.is_year(400)}")
    print("\n=== Flower")
    rose.show()
    print_statistic(rose)
    print(" [asking the rose to grow and bloom]")
    rose.bloom()
    rose.grow()
    rose.show()
    print_statistic(rose)

    print("\n=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    print_statistic(oak)
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    print_statistic(oak)
    print("\n=== Seed")
    sunflower = Seed("Sunflower", 80.0, 45, "yellow")
    sunflower.show()
    print("[make sunflower grow, age and bloom]")
    sunflower.grow()
    sunflower.age()
    sunflower.bloom()
    sunflower.show()
    print_statistic(sunflower)

    print("\n=== Anonymous")
    anon = Plant.create_anonymous()
    anon.show()
    print_statistic(anon)
