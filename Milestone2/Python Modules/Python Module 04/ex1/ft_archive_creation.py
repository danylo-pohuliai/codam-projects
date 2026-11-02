import sys

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print("=== Cyber Archives Recovery & Preservation ===")
        print(f"Accessing file '{sys.argv[1]}'")
        try:
            file = open(sys.argv[1])
        except Exception as e:
            print(f"Error opening file '{sys.argv[1]}': {e}\n")
        else:
            text = file.read()
            print(f"---\n\n{text}\n\n---")
            file.close()
            print(f"File '{sys.argv[1]}' closed.\n")
            if len(text) > 0:
                print("Transform data:\n---\n")
                new_text = text.replace("\n", "#\n")
                if not new_text.endswith("\n"):
                    new_text = new_text + "#"
                print(f"{new_text}\n\n---")
                u_input = input("Enter new file name (or empty): ")
                if u_input == "":
                    print("Not saving data.")
                else:
                    print(f"Saving data to '{u_input}'")
                    try:
                        f = open(u_input, "w")
                        f.write(new_text)
                        print(f"Data saved in file '{u_input}'.")
                        f.close()
                    except Exception as e:
                        print(f"Error saving file '{u_input}': {e}")
                        print("Data not saved.")
            else:
                print("File is empty :)\nData not saved.")
    else:
        print("Usage: ft_archive_creation.py <file>")
