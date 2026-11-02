/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   op_push.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/20 12:48:18 by dpohulia          #+#    #+#             */
/*   Updated: 2026/04/24 15:25:59 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	push(t_ring	*from, t_ring *to)
{
	int	temp;

	temp = from->data[from->head];
	from->head = (from->head + 1) % from->capacity;
	from->size--;
	to->head = (to->head - 1 + to->capacity) % to->capacity;
	to->data[to->head] = temp;
	to->size++;
}

void	do_pa(t_app *app)
{
	if (app->b->size == 0)
		return ;
	push(app->b, app->a);
	app->ops.pa++;
	app->ops.total++;
	if (!app->config.checker)
		write(1, "pa\n", 3);
}

void	do_pb(t_app *app)
{
	if (app->a->size == 0)
		return ;
	push(app->a, app->b);
	app->ops.pb++;
	app->ops.total++;
	if (!app->config.checker)
		write(1, "pb\n", 3);
}
