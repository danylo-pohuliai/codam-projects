/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   hardcode.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/28 15:31:14 by dpohulia          #+#    #+#             */
/*   Updated: 2026/04/28 15:40:57 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	hard_3(t_app *app)
{
	int	v0;
	int	v1;
	int	v2;

	v0 = get_val(app->a, 0);
	v1 = get_val(app->a, 1);
	v2 = get_val(app->a, 2);
	if (v0 > v1 && v1 < v2 && v0 < v2)
		do_sa(app);
	else if (v0 > v1 && v1 > v2)
	{
		do_sa(app);
		do_rra(app);
	}
	else if (v0 > v1 && v1 < v2 && v0 > v2)
		do_ra(app);
	else if (v0 < v1 && v1 > v2 && v0 < v2)
	{
		do_sa(app);
		do_ra(app);
	}
	else if (v0 < v1 && v1 > v2 && v0 > v2)
		do_rra(app);
}

void	hard_4(t_app *app)
{
	int	min_val;
	int	i;
	int	curr;

	min_val = get_val(app->a, 0);
	i = 0;
	while (i < app->a->size)
	{
		curr = get_val(app->a, i);
		if (curr < min_val)
			min_val = curr;
		i++;
	}
	while (get_val(app->a, 0) != min_val)
		do_ra(app);
	do_pb(app);
	hard_3(app);
	do_pa(app);
}

void	hard_5(t_app *app)
{
	normalize(app->a);
	while (get_val(app->a, 0) != 0 && get_val(app->a, 0) != 1)
		do_ra(app);
	do_pb(app);
	while (get_val(app->a, 0) != 0 && get_val(app->a, 0) != 1)
		do_ra(app);
	do_pb(app);
	hard_3(app);
	if (get_val(app->b, 0) < get_val(app->b, 1))
		do_sb(app);
	do_pa(app);
	do_pa(app);
}

void	print_benchmark(t_app *app)
{
	ft_printf(2, "[bench] disorder:  %.2f%%\n", app->config.disorder * 100.0f);
	ft_printf(2, "[bench] strategy:  ");
	if (app->config.strategy == STRAT_SIMPLE)
		ft_printf(2, "Simple / O(n^2)\n");
	else if (app->config.strategy == STRAT_MEDIUM)
		ft_printf(2, "Medium / O(n*sqrt(n))\n");
	else if (app->config.strategy == STRAT_COMPLEX)
		ft_printf(2, "Complex / O(n log n)\n");
	else
		ft_printf(2, "None\n");
	ft_printf(2, "[bench] total_ops:  %d\n", app->ops.total);
	ft_printf(2, "[bench] sa: %5d  sb: ", app->ops.sa);
	ft_printf(2, "%5d  ss: %5d  ", app->ops.sb, app->ops.ss);
	ft_printf(2, "pa: %5d  pb: %5d\n", app->ops.pa, app->ops.pb);
	ft_printf(2, "[bench] ra: %5d  rb: ", app->ops.ra);
	ft_printf(2, "%5d  rr: %5d  ", app->ops.rb, app->ops.rr);
	ft_printf(2, "rra: %4d  rrb: ", app->ops.rra);
	ft_printf(2, "%4d  rrr: %4d\n", app->ops.rrb, app->ops.rrr);
}

int	get_val(t_ring *ring, int i)
{
	return (ring->data[(ring->head + i) % ring->capacity]);
}
