/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_medium.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/28 15:30:31 by dpohulia          #+#    #+#             */
/*   Updated: 2026/04/28 15:30:32 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	ft_sqrt_approx(int number)
{
	int	i;

	if (number <= 0)
		return (0);
	i = 1;
	while (i * i <= number)
		i++;
	return (i - 1);
}

static void	push_to_b(t_app *app, int chunk)
{
	int	pushed;
	int	curr;

	pushed = 0;
	while (app->a->size > 0)
	{
		curr = get_val(app->a, 0);
		if (curr <= pushed)
		{
			do_pb(app);
			do_rb(app);
			pushed++;
		}
		else if (curr <= pushed + chunk)
		{
			do_pb(app);
			pushed++;
		}
		else
			do_ra(app);
	}
}

void	find_max_pos_val(t_app *app, int *max_pos, int *max_val)
{
	int	i;

	i = 1;
	while (i < app->b->size)
	{
		if (get_val(app->b, i) > *max_val)
		{
			*max_val = get_val(app->b, i);
			*max_pos = i;
		}
		i++;
	}
}

static void	push_back_to_a(t_app *app)
{
	int	max_pos;
	int	max_val;

	while (app->b->size > 0)
	{
		max_pos = 0;
		max_val = get_val(app->b, 0);
		find_max_pos_val(app, &max_pos, &max_val);
		if (max_pos <= app->b->size / 2)
			while (max_pos-- > 0)
				do_rb(app);
		else
		{
			max_pos = app->b->size - max_pos;
			while (max_pos-- > 0)
				do_rrb(app);
		}
		do_pa(app);
	}
}

void	sort_medium(t_app *app)
{
	int	chunk;

	normalize(app->a);
	chunk = ft_sqrt_approx(app->a->size) * 1.5;
	if (chunk <= 0)
		chunk = 1;
	push_to_b(app, chunk);
	push_back_to_a(app);
}
