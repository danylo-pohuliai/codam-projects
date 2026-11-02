import sys

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print("=== Cyber Archives Recovery ===")
        print(f"Accessing file '{sys.argv[1]}'")
        try:
            file = open(sys.argv[1])
        except Exception as e:
            print(f"Error opening file '{sys.argv[1]}': {e}\n")
        else:
            text = file.read()
            print(f"---\n\n{text}\n\n---")
            file.close()
            print(f"File '{sys.argv[1]}' closed.")
    else:
        print("Usage: ft_ancient_text.py <file>")
