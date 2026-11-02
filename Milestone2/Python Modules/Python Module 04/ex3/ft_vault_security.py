def secure_archive(
                    filename: str,
                    action: str = "read",
                    content: str = ""
                    ) -> tuple[bool, str]:
    try:
        if action == "read":
            with open(filename, "r") as f:
                data = f.read()
            return (True, data)

        elif action == "write":
            with open(filename, "w") as f:
                f.write(content)
            return (True, "Content successfully written to file")

        else:
            return (False, "Invalid action. Use 'read' or 'write'.")
    except Exception as e:
        return (False, str(e))


if __name__ == "__main__":
    print("=== Cyber Archives Security ===\n")
    print("Using 'secure_archive' to read from a nonexistent file:")
    print(f"{secure_archive("/not/existing/file", "read")}\n")
    print("Using 'secure_archive' to read from an inaccessible file:")
    print(f"{secure_archive("/etc/master.passwd", "read")}\n")
    print("Using 'secure_archive' to read from a regular file:")
    result = secure_archive("ancient_fragment.txt", "read")
    print(f"{result}\n")
    print("Using 'secure_archive' to write previous content to a new file:")
    if result[0]:
        print(secure_archive("new_fragment.txt", "write", result[1]))
    else:
        print(f"{result[1]}")
