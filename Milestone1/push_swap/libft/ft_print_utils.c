/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_utils.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/31 12:38:14 by dpohulia          #+#    #+#             */
/*   Updated: 2026/04/20 12:37:27 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

void	ft_puthex(t_print *tab, unsigned long n, char type)
{
	char	*alphabet;

	if (type == 'X')
		alphabet = "0123456789ABCDEF";
	else
		alphabet = "0123456789abcdef";
	if (n > 15)
	{
		ft_puthex(tab, n / 16, type);
	}
	tab->tl += write(tab->fd, &alphabet[n % 16], 1);
}

void	ft_putnbr(t_print *tab, unsigned long n)
{
	char	c;

	if (n > 9)
		ft_putnbr(tab, n / 10);
	c = (n % 10) + '0';
	tab->tl += write(tab->fd, &c, 1);
}

void	ft_pad(t_print *tab, int count, char c)
{
	while (count-- > 0)
		tab->tl += write(tab->fd, &c, 1);
}

double	handle_float_sign(t_print *tab, double n)
{
	if (n < 0)
	{
		tab->sign = '-';
		return (-n);
	}
	if (tab->sign)
		tab->sign = '+';
	else if (tab->space)
		tab->sign = ' ';
	return (n);
}
