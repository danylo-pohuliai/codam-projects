/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   helpers.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/20 12:45:44 by dpohulia          #+#    #+#             */
/*   Updated: 2026/04/24 15:59:15 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	is_sorted(t_ring *ring)
{
	int	i;
	int	current;
	int	next;

	if (ring->size <= 1)
		return (1);
	i = 0;
	while (i < ring->size - 1)
	{
		current = ring->data[(ring->head + i) % ring->capacity];
		next = ring->data[(ring->head + i + 1) % ring->capacity];
		if (current > next)
			return (0);
		i++;
	}
	return (1);
}

long	safe_atol(char *nptr)
{
	int		i;
	int		sign;
	long	res;

	i = 0;
	res = 0;
	sign = 1;
	while (ft_isspace(nptr[i]))
		i++;
	if (nptr[i] == '-' || nptr[i] == '+')
	{
		if (nptr[i] == '-')
			sign = -1;
		i++;
	}
	while (nptr[i] >= '0' && nptr[i] <= '9')
	{
		res = res * 10 + (nptr[i] - '0');
		if ((sign == 1 && res > 2147483647L)
			|| (sign == -1 && res > 2147483648L))
			break ;
		i++;
	}
	return (res * sign);
}

t_ring	*init_ring(int capacity)
{
	t_ring	*ring;

	if (capacity == 0)
		return (NULL);
	ring = malloc(sizeof(t_ring));
	if (!ring)
		return (NULL);
	ring->data = malloc(sizeof(int) * capacity);
	if (!ring->data)
	{
		free(ring);
		return (NULL);
	}
	ring->capacity = capacity;
	ring->size = 0;
	ring->head = 0;
	return (ring);
}

int	check_duplicates(int *arr, int num, int n)
{
	int	i;

	i = 0;
	while (i < n)
	{
		if (arr[i] == num)
			return (1);
		i++;
	}
	return (0);
}

int	is_valid_string(char *str)
{
	if (!str)
		return (0);
	while (ft_isspace(*str))
		str++;
	if (*str == '-' || *str == '+')
		str++;
	if (!ft_isdigit(*str))
		return (0);
	while (*str && ft_isdigit(*str))
		str++;
	while (*str)
	{
		if (!ft_isspace(*str))
			return (0);
		str++;
	}
	return (1);
}
