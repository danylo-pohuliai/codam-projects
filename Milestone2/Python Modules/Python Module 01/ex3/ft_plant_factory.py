class Plant:
    def __init__(self, name: str, height: float, age: int):
        self.name = name
        self.height = height
        self.age_in_days = age
        self.progress = 0.0

    def show(self) -> None:
        print(f"{self.name}: {self.height:.1f}cm, {self.age_in_days} days old")

    def grow(self) -> None:
        if (self.name == "Rose"):
            self.height = self.height + 0.8
            self.progress = self.progress + 0.8
        elif (self.name == "Sunflower"):
            self.height = self.height + 1.2
            self.progress = self.progress + 1.2
        elif (self.name == "Cactus"):
            self.height = self.height + 1.4
            self.progress = self.progress + 1.4
        else:
            self.height = self.height + 2.1
            self.progress = self.progress + 2.1

    def age(self) -> None:
        self.age_in_days = self.age_in_days + 1


if __name__ == "__main__":
    print("=== Plant Factory Output ===")
    rose = Plant("Rose", 25.0, 30)
    oak = Plant("Oak", 200.0, 365)
    cactus = Plant("Cactus", 5.0, 90)
    sunflower = Plant("Sunflower", 80.0, 45)
    fern = Plant("Fern", 15.0, 120)

    plants = [rose, oak, cactus, sunflower, fern]
    for plant in plants:
        print("Created: ", end="")
        plant.show()
