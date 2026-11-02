/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parsing.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/23 16:08:55 by dpohulia          #+#    #+#             */
/*   Updated: 2026/08/06 18:20:44 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	all_numbers(char *s)
{
	int	i;

	if (!s || s[0] == '\0')
		return (print_error("numeric parameter is empty"));
	i = 0;
	while (s[i])
	{
		if (s[i] >= '0' && s[i] <= '9')
			i++;
		else
		{
			while (ft_isspace(s[i]))
				i++;
			if (s[i] != '\0')
				return (print_error("invalid numeric parameter"));
		}
	}
	return (1);
}

int	is_valid_numeric_str(char *s, int *i)
{
	while (ft_isspace(s[*i]))
		*i = *i + 1;
	if (s[*i] == '+' || s[*i] == '-')
	{
		if (s[*i] == '-')
			return (print_error("numeric parameter cannot be negative"));
		*i = *i + 1;
		if (s[*i] < '0' || s[*i] > '9')
			return (print_error("invalid numeric parameter"));
	}
	while (s[*i] == '0')
		*i = *i + 1;
	if (*i > 0 && s[*i] == '\0')
	{
		if (s[*i - 1] == '0')
		{
			*i = *i - 1;
			return (1);
		}
		else
			return (print_error("numeric parameter is empty"));
	}
	if (!all_numbers(s + *i))
		return (0);
	return (1);
}

int	safe_atoi(char *s)
{
	int			i;
	long long	res;

	i = 0;
	if (is_valid_numeric_str(s, &i))
	{
		res = 0;
		while (s[i] >= '0' && s[i] <= '9')
		{
			res = res * 10 + (s[i] - '0');
			if (res > 2147483647LL)
			{
				print_error("numeric parameter bigger than INT_MAX");
				return (-1);
			}
			i++;
		}
	}
	else
		return (-1);
	return ((int)res);
}

int	init_parameters(t_parameters *param, int *values)
{
	if (values[0] == 0)
		return (print_error("number_of_coders cannot be 0"));
	param->number_of_coders = values[0];
	param->time_to_burnout = values[1];
	param->time_to_compile = values[2];
	param->time_to_debug = values[3];
	param->time_to_refactor = values[4];
	param->number_of_compiles_required = values[5];
	param->dongle_cooldown = values[6];
	param->scheduler = values[7];
	return (1);
}

int	parse(char **argv, t_parameters	*param)
{
	int	i;
	int	values[8];

	i = 0;
	while (i < 7)
	{
		values[i] = safe_atoi(argv[i + 1]);
		if (values[i] == -1)
			return (print_error("invalid numeric parameter, abort"));
		i++;
	}
	if (strcmp(argv[i + 1], "fifo") == 0)
		values[i] = FIFO;
	else if (strcmp(argv[i + 1], "edf") == 0)
		values[i] = EDF;
	else
		return (print_error("invalid scheduler, abort"));
	if (!init_parameters(param, values))
		return (print_error("one or more invalid parameters, abort"));
	return (1);
}
