# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/04/28 15:30:44 by dpohulia          #+#    #+#              #
#    Updated: 2026/04/28 15:31:34 by dpohulia         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = push_swap
CHECKER = checker
CC = cc
CFLAGS = -Wall -Wextra -Werror
RM = rm -f
LIBFT_DIR = ./libft
LIBFT = $(LIBFT_DIR)/libft.a
INCLUDES = -I. -I$(LIBFT_DIR)
SHARED_SRCS = op_push.c op_reverse_rotate.c op_rotate.c op_swap.c free_errors.c helpers.c validation.c
SHARED_OBJS = $(SHARED_SRCS:.c=.o)
PS_SRCS = push_swap.c sort_simple.c sort_complex.c sort_medium.c hardcode.c
PS_OBJS = $(PS_SRCS:.c=.o)
CH_SRCS = checker.c
CH_OBJS = $(CH_SRCS:.c=.o)

all: $(NAME)

$(LIBFT):
	make -C $(LIBFT_DIR)

$(NAME): $(LIBFT) $(SHARED_OBJS) $(PS_OBJS)
	$(CC) $(CFLAGS) $(SHARED_OBJS) $(PS_OBJS) -L$(LIBFT_DIR) -lft -o $(NAME)

$(CHECKER): $(LIBFT) $(SHARED_OBJS) $(CH_OBJS)
	$(CC) $(CFLAGS) $(SHARED_OBJS) $(CH_OBJS) -L$(LIBFT_DIR) -lft -o $(CHECKER)

bonus: $(CHECKER)

%.o: %.c
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

clean:
	make -C $(LIBFT_DIR) clean
	$(RM) -f $(SHARED_OBJS) $(PS_OBJS) $(CH_OBJS)

fclean: clean
	make -C $(LIBFT_DIR) fclean
	$(RM) -f $(NAME) $(CHECKER)

re: fclean all

.PHONY: all clean fclean re bonus