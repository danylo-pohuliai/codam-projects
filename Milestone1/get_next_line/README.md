*This project has been created as part of the 42 curriculum by dpohulia.*

# Get Next Line

## Description
The **get_next_line** project aims to create a highly efficient function in C that reads a single line from a file descriptor (`fd`). 

The goal of this project is to introduce the concept of static variables and deepen the understanding of dynamic memory allocation and file manipulation. Whether reading from a file, standard input, or a network socket, `get_next_line` provides a reliable way to process text line by line, regardless of the size of the chunks being read at a time (`BUFFER_SIZE`). This specific implementation includes the **Bonus** features, allowing it to manage multiple file descriptors simultaneously without losing their individual reading threads.

## Instructions

### Compilation
The function is not intended to be a standalone program, but rather a library component to be integrated into other C projects. 

To compile your code with `get_next_line`, you must define the `BUFFER_SIZE` macro during compilation. This dictates how many bytes `read()` will fetch at a time.

```bash
gcc -Wall -Wextra -Werror -D BUFFER_SIZE=42 main.c get_next_line.c get_next_line_utils.c
```

### Usage
Include the header in your C file:
```c
#include "get_next_line.h"
```

Call the function in a loop to read a file line by line until the end of the file is reached:
```c
int main(void)
{
    int fd = open("text.txt", O_RDONLY);
    char *line;

    while ((line = get_next_line(fd)) != NULL)
    {
        printf("%s", line);
        free(line);
    }
    close(fd);
    return (0);
}
```

## Algorithm and Technical Choices

To successfully read a line, the algorithm must handle cases where a single `read()` call returns multiple lines, a partial line, or a mix of both. 

**Core Algorithm:**
1. **Check for Remainings:** Before calling `read()`, the function checks if there is any leftover text (remainings) from the previous call associated with the current `fd`.
2. **Buffer Processing:** If a newline (`\n`) is found in the remainings, it immediately splits the text. The line is returned, and the new remainder is saved.
3. **Reading:** If no newline is found, the function loops `read()`, appending the new data to the string until a `\n` or the End of File (EOF) is encountered.
4. **Clean Exit:** All memory allocated during the string manipulation is strictly tracked to prevent memory leaks, especially in edge cases where `malloc` fails during dynamic concatenation.

**Justification for Linked Lists (Multiple FDs):**
To manage multiple file descriptors, this project implements a **Linked List** architecture (`t_my_list`) as the static variable, rather than a traditional static array of pointers (e.g., `static char *remainings[OPEN_MAX]`). 
* **Dynamic Footprint:** A static array forcefully reserves memory for thousands of potential FDs, even if only one is used. A linked list allocates memory *only* for actively open files.
* **Scalability:** It scales infinitely without relying on system-specific limits like `OPEN_MAX` or `FOPEN_MAX`.
* **Resource Management:** Once a file is completely read or closed, the specific node is securely unlinked and freed (`free(temp)`), returning the memory to the system and preventing ghost data.

## Resources
* **System Manuals:** `man 3 read`, `man 3 malloc`, `man 3 free`.
* **Peers :)**.
* **AI Usage:** AI was used to debug complex memory leaks triggered by `NULL_CHECK` edge cases, to explain the underlying causes of segmentation faults when dealing with invalid file descriptors, and to provide structural advice on refactoring the `read_file` and `check_buf` functions to strictly comply with the 42 Norm (25-line limit per function) without sacrificing algorithmic efficiency.