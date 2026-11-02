/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_chars.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/31 12:36:07 by dpohulia          #+#    #+#             */
/*   Updated: 2026/03/31 12:40:16 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

void	ft_print_char(t_print *tab)
{
	char	c;

	c = va_arg(tab->args, int);
	if (!tab->dash)
		ft_pad(tab, tab->wdt - 1, ' ');
	tab->tl += write(1, &c, 1);
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
	tab->tl += write(1, s, len);
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
		tab->tl += write(1, "(nil)", 5);
		if (tab->dash)
			ft_pad(tab, tab->wdt - 5, ' ');
		return ;
	}
	len = ft_hexlen(n) + 2;
	if (!tab->dash)
		ft_pad(tab, tab->wdt - len, ' ');
	tab->tl += write(1, "0x", 2);
	ft_puthex(tab, n, 'x');
	if (tab->dash)
		ft_pad(tab, tab->wdt - len, ' ');
}
