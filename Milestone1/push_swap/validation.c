/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   validation.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/20 12:46:41 by dpohulia          #+#    #+#             */
/*   Updated: 2026/04/24 17:15:40 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	validate_and_fill(char **args, t_app *app)
{
	int		i;
	long	num;

	i = 0;
	while (args[i])
		i++;
	app->a = init_ring(i);
	if (!app->a)
		print_error_allocated(args, app);
	i = 0;
	while (args[i])
	{
		if (!is_valid_string(args[i]))
			print_error_allocated(args, app);
		num = safe_atol(args[i]);
		if (num > INT_MAX || num < INT_MIN)
			print_error_allocated(args, app);
		if (check_duplicates(app->a->data, num, i))
			print_error_allocated(args, app);
		app->a->data[i] = num;
		i++;
	}
	app->a->head = 0;
	app->a->size = i;
}

int	get_strat_type(char *arg)
{
	if (!ft_strncmp(arg, "--simple", 9))
		return (STRAT_SIMPLE);
	if (!ft_strncmp(arg, "--medium", 9))
		return (STRAT_MEDIUM);
	if (!ft_strncmp(arg, "--complex", 10))
		return (STRAT_COMPLEX);
	if (!ft_strncmp(arg, "--adaptive", 11))
		return (STRAT_ADAPTIVE);
	return (-1);
}

void	single_flag(char *arg, t_app *app, int *had_strategy)
{
	int	strat;

	strat = get_strat_type(arg);
	if (strat != -1)
	{
		if (*had_strategy)
			print_error();
		app->config.strategy = strat;
		*had_strategy = 1;
	}
	else if (!ft_strncmp(arg, "--bench", 8))
	{
		if (app->config.bench_mode)
			print_error();
		app->config.bench_mode = 1;
	}
	else
		print_error();
}

int	check_flags(char **argv, t_app	*app)
{
	int	i;
	int	had_strategy;

	i = 1;
	had_strategy = 0;
	while (argv[i] && argv[i][0] == '-' && argv[i][1] == '-')
	{
		single_flag(argv[i], app, &had_strategy);
		i++;
	}
	return (i - 1);
}

void	parse_and_validate(int argc, char **argv, t_app	*app)
{
	int		offset;
	char	**args;

	if (argc == 1)
		exit(0);
	offset = check_flags(argv, app);
	if (!argv[offset + 1])
		exit(0);
	if ((argc - offset - 1) > 1)
		args = &argv[offset + 1];
	else
	{
		args = ft_split(argv[offset + 1], ' ');
		if (!args)
			print_error();
		app->data_allocated = 1;
	}
	validate_and_fill(args, app);
	if (app->data_allocated)
		free_char_array(args);
}
