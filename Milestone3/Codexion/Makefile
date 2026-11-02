NAME = codexion
CC = cc
FLAGS = -Wextra -Werror -Wall -pthread #-g -fsanitize=thread
TEST_FLAGS = -include tester.h
SRCS = codexion.c parsing.c little_helpers.c init_simulation.c routines.c \
    scheduling.c free_resources.c bigger_helpers.c
TEST_SRCS = tester.c
OBJDIR = obj
OBJS = $(SRCS:%.c=$(OBJDIR)/%.o)

all: $(NAME)

$(OBJDIR):
	@mkdir -p $(OBJDIR)

$(OBJDIR)/%.o: %.c Makefile | $(OBJDIR)
	$(CC) $(FLAGS) -c $< -o $@

$(NAME): $(OBJS) Makefile
	@$(CC) $(FLAGS) $(OBJS) -o $(NAME)

test:
	@$(CC) $(FLAGS) $(TEST_FLAGS) $(SRCS) $(TEST_SRCS) -o $(NAME)
	@echo "Test executable $(NAME) created!"

clean:
	@rm -rf $(OBJDIR)

fclean: clean
	@rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re test