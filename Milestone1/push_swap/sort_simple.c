/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_simple.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/20 12:47:03 by dpohulia          #+#    #+#             */
/*   Updated: 2026/04/20 12:47:17 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	get_min_pos(t_ring *a)
{
	int	i;
	int	min_pos;
	int	min_val;
	int	curr;

	i = 0;
	min_pos = 0;
	min_val = a->data[a->head];
	while (i < a->size)
	{
		curr = a->data[(a->head + i) % a->capacity];
		if (curr < min_val)
		{
			min_val = curr;
			min_pos = i;
		}
		i++;
	}
	return (min_pos);
}

int	get_max_val(t_ring *a)
{
	int	i;
	int	max_val;

	i = 0;
	max_val = a->data[a->head];
	while (i < a->size)
	{
		if (a->data[(a->head + i) % a->capacity] > max_val)
			max_val = a->data[(a->head + i) % a->capacity];
		i++;
	}
	return (max_val);
}

int	get_target_pos(t_ring *a, int num)
{
	int	i;
	int	prev;
	int	curr;
	int	m_pos;

	m_pos = get_min_pos(a);
	if (num < a->data[(a->head + m_pos) % a->capacity] || num > get_max_val(a))
		return (m_pos);
	i = 0;
	while (i < a->size)
	{
		if (i == 0)
			prev = a->data[(a->head + a->size - 1) % a->capacity];
		else
			prev = a->data[(a->head + i - 1) % a->capacity];
		curr = a->data[(a->head + i) % a->capacity];
		if (prev < num && curr > num)
			return (i);
		i++;
	}
	return (0);
}

void	smart_rotate_a(t_app *app, int target_pos)
{
	int	size;

	size = app->a->size;
	if (target_pos <= size / 2)
	{
		while (target_pos > 0)
		{
			do_ra(app);
			target_pos--;
		}
	}
	else
	{
		while (target_pos < size)
		{
			do_rra(app);
			target_pos++;
		}
	}
}

void	sort_simple(t_app *app)
{
	int	i;
	int	size;
	int	max_so_far;

	i = 0;
	size = app->a->size;
	max_so_far = app->a->data[app->a->head];
	while (i++ < size)
	{
		if (app->a->data[app->a->head] >= max_so_far)
		{
			max_so_far = app->a->data[app->a->head];
			do_ra(app);
		}
		else
			do_pb(app);
	}
	while (app->b->size > 0)
	{
		smart_rotate_a(app, get_target_pos(app->a, app->b->data[app->b->head]));
		do_pa(app);
	}
	smart_rotate_a(app, get_min_pos(app->a));
}
