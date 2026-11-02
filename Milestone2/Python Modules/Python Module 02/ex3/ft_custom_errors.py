class GardenError(Exception):
    def __init__(self, *args: str):
        if args:
            super().__init__(*args)
        else:
            super().__init__("Unknown garden error")


class PlantError(GardenError):
    def __init__(self, *args: str):
        if args:
            super().__init__(*args)
        else:
            super().__init__("Unknown plant error")


class WaterError(GardenError):
    def __init__(self, *args: str):
        if args:
            super().__init__(*args)
        else:
            super().__init__("Unknown water error")


def test() -> None:
    print("Testing PlantError...\nCaught PlantError: ", end="")

    try:
        raise PlantError("The tomato plant is wilting!")
    except PlantError as error:
        print(f"{error}\n")
    print("Testing WaterError...\nCaught WaterError: ", end="")
    try:
        raise WaterError("Not enough water in the tank!")
    except WaterError as error:
        print(f"{error}\n")
    print("Testing catching all garden errors...")
    try:
        raise PlantError("The tomato plant is wilting!")
    except GardenError as error:
        print(f"Caught GardenError: {error}")
    try:
        raise WaterError("Not enough water in the tank!\n")
    except GardenError as error:
        print(f"Caught GardenError: {error}")


if __name__ == "__main__":
    print("=== Custom Garden Errors Demo ===\n")
    test()
    print("All custom error types work correctly!")
