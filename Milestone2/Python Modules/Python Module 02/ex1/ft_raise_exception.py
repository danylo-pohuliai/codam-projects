def input_temperature(temp_str: str) -> int:
    temperature = int(temp_str)
    if temperature > 40:
        raise Exception(f"{temperature}°C is too hot for plants (max 40°C)")
    if temperature < 0:
        raise Exception(f"{temperature}°C is too cold for plants (min 0°C)")
    return temperature


def test_temperature() -> None:
    try:
        print("Input data is '25'")
        input_temperature("25")
    except Exception as error:
        print(error)
    else:
        print("Temperature is now 25°C\n")

    try:
        print("Input data is 'abc'")
        input_temperature("abc")
    except Exception as error:
        print(f"Caught input_temperature error: {error}\n")
    else:
        print("Temperature is now abc°C :)\n")

    try:
        print("Input data is '100'")
        input_temperature("100")
    except Exception as error:
        print(f"Caught input_temperature error: {error}\n")
    else:
        print("Temperature is now 100°C :)\n")

    try:
        print("Input data is '-50'")
        input_temperature("-50")
    except Exception as error:
        print(f"Caught input_temperature error: {error}\n")
    else:
        print("Temperature is now -50°C :)\n")


if __name__ == "__main__":
    print("=== Garden Temperature Checker ===\n")
    test_temperature()
    print("All tests completed - program didn't crash!")
