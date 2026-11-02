/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_helpers.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/31 12:36:36 by dpohulia          #+#    #+#             */
/*   Updated: 2026/03/31 12:36:45 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_numlen_unsigned(unsigned int n)
{
	int		res;

	res = 0;
	if (n == 0)
		return (1);
	while (n > 0)
	{
		n /= 10;
		res++;
	}
	return (res);
}

int	ft_hexlen(unsigned long n)
{
	int	res;

	res = 0;
	if (n == 0)
		return (1);
	while (n > 0)
	{
		n /= 16;
		res++;
	}
	return (res);
}

int	ft_numlen(long n)
{
	int		res;

	res = 0;
	if (n == 0)
		return (1);
	if (n < 0)
	{
		n = -n;
		res++;
	}
	while (n > 0)
	{
		n /= 10;
		res++;
	}
	return (res);
}
