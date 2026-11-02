/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_chars.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/31 12:36:07 by dpohulia          #+#    #+#             */
/*   Updated: 2026/04/20 12:37:17 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

void	ft_print_char(t_print *tab)
{
	char	c;

	c = va_arg(tab->args, int);
	if (!tab->dash)
		ft_pad(tab, tab->wdt - 1, ' ');
	tab->tl += write(tab->fd, &c, 1);
	if (tab->dash)
		ft_pad(tab, tab->wdt - 1, ' ');
}

void	ft_print_str(t_print *tab)
{
	char	*s;
	int		len;

	s = va_arg(tab->args, char *);
	if (!s)
	{
		if (tab->pnt && tab->prc < 6)
			s = "";
		else
			s = "(null)";
	}
	len = ft_strlen(s);
	if (tab->pnt && tab->prc < len)
		len = tab->prc;
	if (!tab->dash)
		ft_pad(tab, tab->wdt - len, ' ');
	tab->tl += write(tab->fd, s, len);
	if (tab->dash)
		ft_pad(tab, tab->wdt - len, ' ');
}

void	ft_print_ptr(t_print *tab)
{
	unsigned long	n;
	int				len;

	n = (unsigned long)va_arg(tab->args, void *);
	if (!n)
	{
		if (!tab->dash)
			ft_pad(tab, tab->wdt - 5, ' ');
		tab->tl += write(tab->fd, "(nil)", 5);
		if (tab->dash)
			ft_pad(tab, tab->wdt - 5, ' ');
		return ;
	}
	len = ft_hexlen(n) + 2;
	if (!tab->dash)
		ft_pad(tab, tab->wdt - len, ' ');
	tab->tl += write(tab->fd, "0x", 2);
	ft_puthex(tab, n, 'x');
	if (tab->dash)
		ft_pad(tab, tab->wdt - len, ' ');
}

void	pad_float_part(t_print *tab, long int_p, double frac_p, int spaces)
{
	if (!tab->dash && !tab->zero)
		ft_pad(tab, spaces, ' ');
	if (tab->sign)
		tab->tl += write(tab->fd, &tab->sign, 1);
	if (!tab->dash && tab->zero)
		ft_pad(tab, spaces, '0');
	print_float_parts(tab, int_p, frac_p, tab->prc);
	if (tab->dash)
		ft_pad(tab, spaces, ' ');
}

void	ft_print_float(t_print *tab)
{
	double	n;
	long	int_part;
	double	frac_part;
	int		len;
	int		spaces;

	n = va_arg(tab->args, double);
	if (!tab->pnt)
		tab->prc = 6;
	n = handle_float_sign(tab, n);
	n += 0.5 / ft_pow10(tab->prc);
	int_part = (long)n;
	frac_part = n - (double)int_part;
	len = ft_numlen(int_part) + tab->prc + (tab->prc > 0 || tab->hash);
	spaces = tab->wdt - len - (tab->sign != 0);
	if (spaces < 0)
		spaces = 0;
	pad_float_part(tab, int_part, frac_part, spaces);
}
