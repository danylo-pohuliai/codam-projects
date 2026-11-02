*This project has been created as part of the 42 curriculum by dpohulia*

# Libft

## Description
The goal of this project is to code our own first C library. It involves rewriting various standard C library (`libc`) functions from scratch, as well as developing additional utility functions for string manipulation, memory allocation, and linked list management. This static library (`libft.a`) will serve as a foundational building block for future C projects within the curriculum.

The functions in this library are divided into three main parts:
### Part 1: Libc Functions
These are reimplementations of standard C library functions. They share the same prototypes and behaviors as the originals, but are prefixed with ft_.
 * Character Classification:
   * ft_isalpha - Checks for an alphabetic character.
   * ft_isdigit - Checks for a digit (0 through 9).
   * ft_isalnum - Checks for an alphanumeric character.
   * ft_isascii - Checks whether a character fits into the ASCII character set.
   * ft_isprint - Checks for any printable character.
 * String Manipulation:
   * ft_strlen - Calculates the length of a string.
   * ft_strlcpy - Size-bounded string copying.
   * ft_strlcat - Size-bounded string concatenation.
   * ft_strchr - Locates the first occurrence of a character in a string.
   * ft_strrchr - Locates the last occurrence of a character in a string.
   * ft_strncmp - Compares two strings up to a specified number of characters.
   * ft_strnstr - Locates a substring in a string.
 * Memory Manipulation:
   * ft_memset - Fills memory with a constant byte.
   * ft_bzero - Zeroes a byte string.
   * ft_memcpy - Copies memory area.
   * ft_memmove - Copies memory area (safe for overlapping areas).
   * ft_memchr - Scans memory for a character.
   * ft_memcmp - Compares memory areas.
 * Conversion & Allocation:
   * ft_toupper - Converts a character to uppercase.
   * ft_tolower - Converts a character to lowercase.
   * ft_atoi - Converts a string to an integer.
   * ft_calloc - Allocates memory for an array and zeroes it.
   * ft_strdup - Duplicates a string.
### Part 2: Additional Functions
These functions provide useful utilities that are either not included in standard libc or exist in a different form.
 * ft_substr - Extracts a substring from a string.
 * ft_strjoin - Concatenates two strings into a new one.
 * ft_strtrim - Trims specified characters from the beginning and end of a string.
 * ft_split - Splits a string into an array of strings using a delimiter character.
 * ft_itoa - Converts an integer to a string.
 * ft_strmapi - Applies a function to each character of a string, creating a new string.
 * ft_striteri - Applies a function to each character of a string, modifying it in place.
 * ft_putchar_fd - Outputs a character to a given file descriptor.
 * ft_putstr_fd - Outputs a string to a given file descriptor.
 * ft_putendl_fd - Outputs a string to a given file descriptor, followed by a newline.
 * ft_putnbr_fd - Outputs an integer to a given file descriptor.
### Part 3: Linked List Functions
A custom implementation of linked lists using the t_list structure to store generic data.
 * ft_lstnew - Creates a new list node.
 * ft_lstadd_front - Adds a node to the beginning of a list.
 * ft_lstsize - Counts the number of nodes in a list.
 * ft_lstlast - Returns the last node of a list.
 * ft_lstadd_back - Adds a node to the end of a list.
 * ft_lstdelone - Frees the memory of a specific node's content.
 * ft_lstclear - Deletes and frees a node and all its successors.
 * ft_lstiter - Applies a function to the content of all nodes in a list.
 * ft_lstmap - Applies a function to each node, creating a new list with the results.

## Instructions
To compile the library, navigate to the root of the repository and run:

```bash
make
```

This will compile the source files and generate the libft.a static library.
To use libft in your own projects:
 * Include the header in your C files:
 ```C
   #include "libft.h"
```
 * Compile your project with the library:
 ```bash
   cc your_source_file.c -L. -lft
```

## Available Makefile rules:
 * make / make all: Compiles the standard library functions.
 * make clean: Removes all .o object files.
 * make fclean: Removes object files and the libft.a library file.
 * make re: Recompiles the entire project from scratch.

 ## Resources
 * Linux Manual Pages (man): The primary resource used to understand the exact behavior, parameters, and return values of the original libc functions.
 * Peers: Invaluable discussions and brainstorming sessions with fellow students.
 * AI Usage: Generative AI was used occasionally to clarify complex Makefile syntax and to get conceptual explanations for pointer arithmetic edge cases. AI was also utilized to format, structure, and draft this README.md file to ensure clarity and adherence to the project's documentation requirements.