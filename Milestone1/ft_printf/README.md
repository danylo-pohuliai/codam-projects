*This project has been created as part of the 42 curriculum by dpohulia.*

# ft_printf

## Description
The **ft_printf** project is a custom implementation of the standard C library `printf` function. The goal of this project is to recreate the formatting and output capabilities of `printf` while learning about variadic arguments in C (`stdarg.h`) and building a robust, modular parsing architecture.

This implementation goes beyond the mandatory requirements and includes the full **Bonus Part**, handling complex combinations of formatting flags, minimum field widths, and precision logic. It successfully mimics the behavior of the original `printf` even in the most obscure edge cases.

### Handled Specifiers:
*   `%c` - Single character
*   `%s` - String of characters
*   `%p` - Pointer address (in hexadecimal)
*   `%d` / `%i` - Signed decimal integer
*   `%u` - Unsigned decimal integer
*   `%x` / `%X` - Unsigned hexadecimal integer (lowercase/uppercase)
*   `%%` - A literal '%' character

### Bonus Flags Handled:
*   `-` (Left-justify within the given field width)
*   `0` (Left-pads the number with zeroes instead of spaces)
*   `.` (Precision: minimum number of digits for integers, maximum string length for strings)
*   `#` (Alternate form: adds `0x` or `0X` for hex, forces decimal point for floats if applicable)
*   `' '` (Space: leaves a blank space before a positive number)
*   `+` (Forces a plus sign `+` before positive numbers)
*   *Field minimum width* (as a number or passed as `*` via arguments)

---

## Algorithm and Data Structure
To handle the immense complexity of flag combinations and adhere to the strict **42 Norminette** (maximum 25 lines per function, maximum 4 arguments per function), the project uses a centralized state-tracking data structure and a dispatch-based algorithm.

### Data Structure: `t_print`
Instead of passing dozens of variables between parsing and printing functions, a single struct is passed by reference:
```c
typedef struct s_print
{
    va_list args;   // Variadic arguments list
    int     wdt;    // Field width
    int     prc;    // Precision
    int     zero;   // '0' flag
    int     pnt;    // '.' (precision) flag
    int     dash;   // '-' (left justify) flag
    int     tl;     // Total length (return value)
    int     sign;   // '+' or ' ' (space) flag
    int     hash;   // '#' flag
    int     type;   // The specifier type (e.g., 'd', 'x')
} t_print;
```
Justification: This structure acts as the "brain" of the operation. It allows for modularity; the parsing functions only need to update this struct, and the printing functions only need to read it to know exactly how to format the output. It completely eliminates the need for ternary operators and excessive function arguments.
Algorithm
 * Linear Scan: The main function scans the format string character by character. Normal characters are printed immediately, and the total length tab->tl is incremented.
 * Parsing Phase: Upon encountering a %, the ft_eval_format function is called. It iterates through the subsequent characters, parsing flags, width, and precision using dedicated helper functions (ft_parse_flags, ft_parse_width, ft_parse_precision), updating the t_print struct accordingly.
 * Dispatch Phase: Once the specifier (e.g., d, x) is found, ft_print_controller routes the execution to the appropriate printing function.
 * Formatting & Execution: The specific printing function (e.g., ft_print_int) calculates the required padding (spaces and zeros) based on conflicts and priorities (e.g., - overrides 0, . overrides 0 for numbers). It then uses helper functions to execute the write system calls in the exact required order (Left Spaces -> Sign/Prefix -> Zeros -> Number -> Right Spaces).

### Instructions
Compilation
The project includes a Makefile that compiles the library. To compile the libftprintf.a static library along with the libft dependencies, simply run:
make

Available commands:
 * make clean: Removes all .o object files.
 * make fclean: Removes object files and the libftprintf.a library.
 * make re: Performs a full recompilation (fclean followed by all).


### Resources
 * man 3 printf: The ultimate reference for the standard behavior, edge cases, and flag precedence.
 * stdarg.h documentation: For understanding how to iterate through variadic arguments using va_start, va_arg, va_copy, and va_end.
 * AI Usage Acknowledgment: Artificial Intelligence (LLM) was utilized during the development of this project for educational and architectural purposes. Specifically, AI was used to:
   * Explain the complex architecture required for the bonus part, particularly how to structure the code to resolve precedence conflicts between formatting flags (e.g., understanding why the . precision flag cancels out the 0 padding flag for numeric types).
   * Provide guidance on refactoring code to strictly adhere to the 42 Norminette (e.g., logically splitting mathematical padding calculations from the write execution to stay under the 25-line limit).