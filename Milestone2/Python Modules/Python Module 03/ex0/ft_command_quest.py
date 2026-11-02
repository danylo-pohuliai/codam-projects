import sys

if __name__ == "__main__":
    print("=== Command Quest ===")
    print(f"Program name: {sys.argv[0]}")
    if len(sys.argv) == 1:
        print("No arguments provided!\nTotal arguments: 1")
    else:
        print(f"Arguments received: {len(sys.argv) - 1}")
        n = 1
        for arg in sys.argv[1:]:
            print(f"Argument {n}: {arg}")
            n += 1
        print(f"Total arguments: {n}")
