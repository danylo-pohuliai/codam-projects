def input_temperature(temp_str: str) -> int:
    temperature = int(temp_str)
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


if __name__ == "__main__":
    print("=== Garden Temperature ===\n")
    test_temperature()
    print("All tests completed - program didn't crash!")
