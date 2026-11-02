/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   op_rotate.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/20 12:48:00 by dpohulia          #+#    #+#             */
/*   Updated: 2026/04/24 18:24:26 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	rotate(t_ring *ring)
{
	int	temp;
	int	tail_pos;

	temp = ring->data[ring->head];
	tail_pos = (ring->head + ring->size) % ring->capacity;
	ring->data[tail_pos] = temp;
	ring->head = (ring->head + 1) % ring->capacity;
}

void	do_ra(t_app *app)
{
	if (app->a->size < 2)
		return ;
	rotate(app->a);
	app->ops.ra++;
	app->ops.total++;
	if (!app->config.checker)
		write(1, "ra\n", 3);
}

void	do_rb(t_app *app)
{
	if (app->b->size < 2)
		return ;
	rotate(app->b);
	app->ops.rb++;
	app->ops.total++;
	if (!app->config.checker)
		write(1, "rb\n", 3);
}

void	do_rr(t_app *app)
{
	if (app->a->size < 2 || app->b->size < 2)
		return ;
	rotate(app->a);
	rotate(app->b);
	app->ops.rr++;
	app->ops.total++;
	if (!app->config.checker)
		write(1, "rr\n", 3);
}
