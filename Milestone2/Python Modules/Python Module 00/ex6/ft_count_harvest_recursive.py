def ft_count_harvest_recursive() -> None:
    days = int(input("Days until harvest: "))
    if (days > 0):
        helper(days)
    print("Harvest time!")


def helper(days: int) -> None:
    if (days > 1):
        helper(days - 1)
    print(f"Day {days}")
