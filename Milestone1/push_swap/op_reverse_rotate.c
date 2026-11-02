/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   op_reverse_rotate.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/20 12:48:07 by dpohulia          #+#    #+#             */
/*   Updated: 2026/04/24 15:26:15 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	reverse_rotate(t_ring *ring)
{
	int	temp;
	int	last_pos;
	int	new_head;

	last_pos = (ring->head + ring->size - 1) % ring->capacity;
	temp = ring->data[last_pos];
	new_head = (ring->head - 1 + ring->capacity) % ring->capacity;
	ring->data[new_head] = temp;
	ring->head = new_head;
}

void	do_rra(t_app *app)
{
	if (app->a->size < 2)
		return ;
	reverse_rotate(app->a);
	app->ops.rra++;
	app->ops.total++;
	if (!app->config.checker)
		write(1, "rra\n", 4);
}

void	do_rrb(t_app *app)
{
	if (app->b->size < 2)
		return ;
	reverse_rotate(app->b);
	app->ops.rrb++;
	app->ops.total++;
	if (!app->config.checker)
		write(1, "rrb\n", 4);
}

void	do_rrr(t_app *app)
{
	if (app->a->size < 2 || app->b->size < 2)
		return ;
	reverse_rotate(app->a);
	reverse_rotate(app->b);
	app->ops.rrr++;
	app->ops.total++;
	if (!app->config.checker)
		write(1, "rrr\n", 4);
}
