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


def water_plant(plant_name: str) -> None:
    if (plant_name == plant_name.capitalize()):
        print(f"Watering {plant_name}: [OK]")
    else:
        raise PlantError(f"Invalid plant name to water: '{plant_name}'")


def test_watering_system(plants: list[str]) -> None:
    print("Opening watering system")
    try:
        for plant in plants:
            water_plant(plant)
    except PlantError as error:
        print(f"Caught PlantError: {error}")
        print(".. ending tests and returning to main")
    finally:
        print("Closing watering system\n")


if __name__ == "__main__":
    print("=== Garden Watering System ===\n\nTesting valid plants...")
    test_watering_system(["Tomato", "Lettuce", "Carrots"])
    print("Testing invalid plants...")
    test_watering_system(["Tomato", "lettuce", "carrots"])
    print("Cleanup always happens, even with errors!")
