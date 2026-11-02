/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_parser.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/31 12:35:23 by dpohulia          #+#    #+#             */
/*   Updated: 2026/04/20 12:37:13 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_parse_flags(t_print *tab, const char *str, int i)
{
	while (str[i] && ft_is_flag(str[i]))
	{
		if (str[i] == '-')
			tab->dash = 1;
		if (str[i] == '0')
			tab->zero = 1;
		if (str[i] == '+')
			tab->sign = 1;
		if (str[i] == ' ')
			tab->space = 1;
		if (str[i] == '#')
			tab->hash = 1;
		i++;
	}
	return (i);
}

int	ft_parse_width(t_print *tab, const char *str, int i)
{
	int	val;

	val = 0;
	if (str[i] == '*')
	{
		tab->wdt = va_arg(tab->args, int);
		if (tab->wdt < 0)
		{
			tab->dash = 1;
			tab->wdt *= -1;
		}
		i++;
	}
	else
	{
		while (ft_isdigit(str[i]))
		{
			val = (val * 10) + (str[i] - '0');
			i++;
		}
		tab->wdt = val;
	}
	return (i);
}

int	ft_parse_precision(t_print *tab, const char *str, int i)
{
	int	val;

	i++;
	tab->pnt = 1;
	val = 0;
	if (str[i] == '*')
	{
		tab->prc = va_arg(tab->args, int);
		i++;
	}
	else
	{
		while (ft_isdigit(str[i]))
		{
			val = (val * 10) + (str[i] - '0');
			i++;
		}
		tab->prc = val;
	}
	return (i);
}

int	ft_is_specifier(int c)
{
	return (c == 'c' || c == 's' || c == 'p' || c == 'd' || c == 'i'
		|| c == 'u' || c == 'x' || c == 'X' || c == 'f' || c == '%');
}

int	ft_is_flag(int c)
{
	return (c == '-' || c == '0' || c == '#' || c == ' ' || c == '+');
}
