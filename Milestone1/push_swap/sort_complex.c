/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_complex.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/28 15:30:18 by dpohulia          #+#    #+#             */
/*   Updated: 2026/04/28 15:30:24 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	get_smallest(t_ring *ring, int *is_norm)
{
	int	smallest_val;
	int	smallest_idx;
	int	j;

	smallest_val = INT_MAX;
	smallest_idx = 0;
	j = 0;
	while (j < ring->size)
	{
		if (!is_norm[j] && get_val(ring, j) <= smallest_val)
		{
			smallest_val = get_val(ring, j);
			smallest_idx = j;
		}
		j++;
	}
	return (smallest_idx);
}

void	normalize(t_ring *ring)
{
	int	*is_norm;
	int	smallest_idx;
	int	i;

	is_norm = ft_calloc(ring->size, sizeof(int));
	if (!is_norm)
		return ;
	i = 0;
	while (i < ring->size)
	{
		smallest_idx = get_smallest(ring, is_norm);
		ring->data[(ring->head + smallest_idx) % ring->capacity] = i;
		is_norm[smallest_idx] = 1;
		i++;
	}
	free(is_norm);
}

void	sort_complex(t_app *app)
{
	int	bit;
	int	i;
	int	n;

	normalize(app->a);
	bit = 1;
	i = 0;
	while (i++ < 32)
	{
		n = app->a->size;
		while (n-- > 0)
		{
			if (get_val(app->a, 0) & bit)
				do_ra(app);
			else
				do_pb(app);
		}
		while (app->b->size > 0)
			do_pa(app);
		if (is_sorted(app->a))
			break ;
		bit <<= 1;
	}
}
