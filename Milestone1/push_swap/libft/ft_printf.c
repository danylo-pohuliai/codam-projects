/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/24 13:57:50 by dpohulia          #+#    #+#             */
/*   Updated: 2026/04/20 12:37:32 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

void	ft_initialise_tab(t_print *tab)
{
	tab->wdt = 0;
	tab->prc = 0;
	tab->type = 0;
	tab->zero = 0;
	tab->pnt = 0;
	tab->dash = 0;
	tab->sign = 0;
	tab->space = 0;
	tab->hash = 0;
}

int	ft_eval_format(t_print *tab, const char *str, int i)
{
	ft_initialise_tab(tab);
	while (str[i] && !ft_is_specifier(str[i]))
	{
		if (ft_is_flag(str[i]))
			i = ft_parse_flags(tab, str, i);
		else if (ft_isdigit(str[i]))
			i = ft_parse_width(tab, str, i);
		else if (str[i] == '.')
			i = ft_parse_precision(tab, str, i);
		else
			i++;
	}
	tab->type = str[i];
	if (str[i])
	{
		ft_print_controller(tab);
		return (i);
	}
	return (i - 1);
}

void	ft_print_controller(t_print *tab)
{
	if (tab->type == 'c')
		ft_print_char(tab);
	else if (tab->type == 's')
		ft_print_str(tab);
	else if (tab->type == 'd' || tab->type == 'i')
		ft_print_int(tab);
	else if (tab->type == 'u')
		ft_print_unsigned(tab);
	else if (tab->type == 'x' || tab->type == 'X')
		ft_print_hex(tab);
	else if (tab->type == 'p')
		ft_print_ptr(tab);
	else if (tab->type == 'f')
		ft_print_float(tab);
	else if (tab->type == '%')
		tab->tl += write(tab->fd, "%", 1);
}

int	ft_printf(int fd, const char *str, ...)
{
	t_print	tab;
	int		i;

	ft_initialise_tab(&tab);
	tab.tl = 0;
	tab.fd = fd;
	va_start(tab.args, str);
	i = 0;
	while (str[i])
	{
		if (str[i] == '%')
			i = ft_eval_format(&tab, str, i + 1);
		else
			tab.tl += write(tab.fd, &str[i], 1);
		i++;
	}
	va_end(tab.args);
	return (tab.tl);
}

// int main(void)
// {
// 	int		res;
// 	char	*str = "pivchanskiy";
// 	char	*nl = NULL;

// 	res = ft_printf(1, "0 %f%%\n", 22.624567f);
// 	ft_printf(1, "%d\n", res);
// 	res = printf("0 %f%%\n", 22.624567f);
// 	printf("%d\n\n", res);
// 	return (0);
// }
