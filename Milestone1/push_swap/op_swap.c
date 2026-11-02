/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   op_swap.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/20 12:47:51 by dpohulia          #+#    #+#             */
/*   Updated: 2026/04/24 15:26:50 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	swap(t_ring *ring)
{
	int		temp;
	int		first;
	int		second;

	first = ring->head;
	second = (ring->head + 1) % ring->capacity;
	temp = ring->data[first];
	ring->data[first] = ring->data[second];
	ring->data[second] = temp;
}

void	do_sa(t_app *app)
{
	if (app->a->size < 2)
		return ;
	swap(app->a);
	app->ops.sa++;
	app->ops.total++;
	if (!app->config.checker)
		write(1, "sa\n", 3);
}

void	do_sb(t_app *app)
{
	if (app->b->size < 2)
		return ;
	swap(app->b);
	app->ops.sb++;
	app->ops.total++;
	if (!app->config.checker)
		write(1, "sb\n", 3);
}

void	do_ss(t_app *app)
{
	if (app->a->size < 2 || app->b->size < 2)
		return ;
	swap(app->a);
	swap(app->b);
	app->ops.ss++;
	app->ops.total++;
	if (!app->config.checker)
		write(1, "ss\n", 3);
}
