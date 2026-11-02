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


if __name__ == "__main__":
    print("=== Garden Security System ===")
    rose = Plant("Rose", 15.0, 10)
    print("Plant created: ", end="")
    rose.show()
    print("")
    rose.set_height(25.0)
    rose.set_age(30)
    print("")
    rose.set_height(-25)
    rose.set_age(-30)
    print("")
    print("Current state: ", end="")
    rose.show()
