/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_nums.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/31 12:37:23 by dpohulia          #+#    #+#             */
/*   Updated: 2026/04/20 12:37:24 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

void	ft_print_unsigned(t_print *tab)
{
	unsigned int	n;
	int				len;
	int				zeros;
	int				spaces;

	n = va_arg(tab->args, unsigned int);
	len = ft_numlen_unsigned(n);
	if (n == 0 && tab->pnt && tab->prc == 0)
		len = 0;
	zeros = 0;
	if (tab->prc > len)
		zeros = tab->prc - len;
	spaces = tab->wdt - (len + zeros);
	if (!tab->dash && (!tab->zero || tab->pnt))
		ft_pad(tab, spaces, ' ');
	if (!tab->dash && tab->zero && !tab->pnt)
		ft_pad(tab, spaces, '0');
	ft_pad(tab, zeros, '0');
	if (len > 0)
		ft_putnbr(tab, n);
	if (tab->dash)
		ft_pad(tab, spaces, ' ');
}

static void	print_hex_part(t_print *tab, unsigned int n, int spaces, int zeros)
{
	if (!tab->dash && (!tab->zero || tab->pnt))
		ft_pad(tab, spaces, ' ');
	if (tab->hash && tab->type == 'x')
		tab->tl += write(tab->fd, "0x", 2);
	if (tab->hash && tab->type == 'X')
		tab->tl += write(tab->fd, "0X", 2);
	if (!tab->dash && tab->zero && !tab->pnt)
		ft_pad(tab, spaces, '0');
	ft_pad(tab, zeros, '0');
	if (n != 0 || !tab->pnt || tab->prc != 0)
		ft_puthex(tab, n, tab->type);
	if (tab->dash)
		ft_pad(tab, spaces, ' ');
}

void	ft_print_hex(t_print *tab)
{
	unsigned int	n;
	int				len;
	int				spaces;
	int				zeros;

	n = va_arg(tab->args, unsigned int);
	len = ft_hexlen(n);
	if (n == 0)
		tab->hash = 0;
	if (tab->pnt && tab->prc == 0 && n == 0)
		len = 0;
	zeros = 0;
	if (tab->prc > len)
		zeros = tab->prc - len;
	spaces = tab->wdt - len - zeros;
	if (tab->hash)
		spaces -= 2;
	print_hex_part(tab, n, spaces, zeros);
}

static void	print_int_part(t_print *tab, long n, int spaces, int zeros)
{
	if (!tab->dash && (!tab->zero || tab->pnt))
		ft_pad(tab, spaces, ' ');
	if (tab->sign)
		tab->tl += write(tab->fd, &tab->sign, 1);
	if (!tab->dash && tab->zero && !tab->pnt)
		ft_pad(tab, spaces, '0');
	ft_pad(tab, zeros, '0');
	if (n != 0 || !tab->pnt || tab->prc != 0)
		ft_putnbr(tab, n);
	if (tab->dash)
		ft_pad(tab, spaces, ' ');
}

void	ft_print_int(t_print *tab)
{
	long	n;
	int		len;
	int		zeros;
	int		spaces;

	n = va_arg(tab->args, int);
	if (n < 0)
	{
		tab->sign = '-';
		n = -n;
	}
	else if (tab->sign)
		tab->sign = '+';
	else if (tab->space)
		tab->sign = ' ';
	len = ft_numlen(n);
	if (n == 0 && tab->pnt && tab->prc == 0)
		len = 0;
	zeros = 0;
	if (tab->prc > len)
		zeros = tab->prc - len;
	spaces = tab->wdt - len - zeros;
	if (tab->sign)
		spaces--;
	print_int_part(tab, n, spaces, zeros);
}
