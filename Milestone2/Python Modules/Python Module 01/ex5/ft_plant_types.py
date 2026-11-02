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

    def show(self) -> None:
        print(
            f"{self.name}: {self._height:.1f}cm,"
            f" {self._age_in_days} days old"
            )

    def grow(self) -> None:
        if (self.name == "Rose"):
            self._height = self._height + 0.8
            self.progress = self.progress + 0.8
        elif (self.name == "Sunflower"):
            self._height = self._height + 1.2
            self.progress = self.progress + 1.2
        elif (self.name == "Cactus"):
            self._height = self._height + 1.4
            self.progress = self.progress + 1.4
        else:
            self._height = self._height + 2.1
            self.progress = self.progress + 2.1

    def age(self) -> None:
        self._age_in_days = self._age_in_days + 1

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
    def __init__(
            self,
            name: str,
            height: float,
            age: int,
            trunk_diameter: float):
        super().__init__(name, height, age)
        self.trunk_diameter = trunk_diameter

    def produce_shade(self) -> None:
        print(
            f"Tree {self.name} now produces a shade"
            f" of {self.get_height()}cm long and {self.trunk_diameter}cm wide."
            )

    def show(self) -> None:
        super().show()
        print(f" Trunk diameter: {self.trunk_diameter}cm")


class Vegetable(Plant):
    def __init__(
            self,
            name: str,
            height: float,
            age: int,
            harvest_season: str,
            nutritional_value: int
            ):
        super().__init__(name, height, age)
        self.harvest_season = harvest_season
        self.nutritional_value = nutritional_value

    def grow(self) -> None:
        super().grow()
        self.nutritional_value += 1

    def show(self) -> None:
        super().show()
        print(f" Harvest season: {self.harvest_season}")
        print(f" Nutritional value: {self.nutritional_value}")


if __name__ == "__main__":
    print("=== Garden Plant Types ===\n=== Flower")
    rose = Flower("Rose", 15.0, 10, "red")
    rose.show()
    print("[asking the rose to bloom]")
    rose.bloom()
    rose.show()
    print("\n=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    print("\n=== Vegetable")
    tomato = Vegetable("Tomato", 5.0, 10, "April", 0)
    tomato.show()
    print("[make tomato grow and age for 20 days]")
    for n in range(20):
        tomato.age()
        tomato.grow()
    tomato.show()
