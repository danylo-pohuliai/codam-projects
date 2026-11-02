/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/20 12:47:36 by dpohulia          #+#    #+#             */
/*   Updated: 2026/04/24 18:03:27 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include "libft/libft.h"

typedef enum e_strategy
{
	STRAT_ADAPTIVE,
	STRAT_SIMPLE,
	STRAT_MEDIUM,
	STRAT_COMPLEX
}	t_strategy;

typedef struct s_config
{
	t_strategy	strategy;
	int			bench_mode;
	int			checker;
	float		disorder;
}	t_config;

typedef struct s_operations
{
	int	sa;
	int	sb;
	int	ss;
	int	pa;
	int	pb;
	int	ra;
	int	rb;
	int	rr;
	int	rra;
	int	rrb;
	int	rrr;
	int	total;
}	t_operations;

typedef struct s_ring
{
	int	*data;
	int	head;
	int	size;
	int	capacity;
}	t_ring;

typedef struct s_app
{
	t_ring			*a;
	t_ring			*b;
	t_config		config;
	t_operations	ops;
	int				data_allocated;
}	t_app;

void	free_char_array(char **res);
void	free_ring(t_ring *ring);
void	print_error(void);
void	print_error_allocated(char **args, t_app *app);

int		is_sorted(t_ring *ring);
long	safe_atol(char *nptr);
t_ring	*init_ring(int capacity);
int		check_duplicates(int *arr, int num, int n);
int		is_valid_string(char *str);

void	validate_and_fill(char **args, t_app *app);
int		get_strat_type(char *arg);
void	single_flag(char *arg, t_app *app, int *had_strategy);
int		check_flags(char **argv, t_app	*app);
void	parse_and_validate(int argc, char **argv, t_app	*app);

void	do_sa(t_app *app);
void	do_sb(t_app *app);
void	do_ss(t_app *app);
void	do_ra(t_app *app);
void	do_rb(t_app *app);
void	do_rr(t_app *app);
void	do_rra(t_app *app);
void	do_rrb(t_app *app);
void	do_rrr(t_app *app);
void	do_pa(t_app *app);
void	do_pb(t_app *app);

void	sort_simple(t_app *app);
void	sort_medium(t_app *app);
void	sort_complex(t_app *app);
void	normalize(t_ring *ring);

void	hard_3(t_app *app);
void	hard_4(t_app *app);
void	hard_5(t_app *app);
void	print_benchmark(t_app *app);
int		get_val(t_ring *ring, int i);

#endif