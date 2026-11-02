def garden_operations(operation_number: int) -> None:
    if operation_number == 0:
        operation_number = int('abc')
    elif operation_number == 1:
        operation_number = 10 / 0
    elif operation_number == 2:
        open("/non/existent/file")
    elif operation_number == 3:
        operation_number = operation_number + "str"


def test_error_types() -> None:
    for n in range(0, 5):
        try:
            print(f"Testing operation {n}...")
            garden_operations(n)
        except ValueError as error:
            print(f"Caught ValueError: {error}")
        except ZeroDivisionError as error:
            print(f"Caught ZeroDivisionError: {error}")
        except FileNotFoundError as error:
            print(f"Caught FileNotFoundError: {error}")
        except TypeError as error:
            print(f"Caught TypeError: {error}")
        else:
            print("Operation completed successfully")
    print("")


if __name__ == "__main__":
    print("=== Garden Error Types Demo ===")
    test_error_types()
    print("All error types tested successfully!")
