/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/24 13:57:50 by dpohulia          #+#    #+#             */
/*   Updated: 2026/03/31 12:35:05 by dpohulia         ###   ########.fr       */
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
	else if (tab->type == '%')
		tab->tl += write(1, "%", 1);
}

int	ft_printf(const char *str, ...)
{
	t_print	tab;
	int		i;

	ft_initialise_tab(&tab);
	tab.tl = 0;
	va_start(tab.args, str);
	i = 0;
	while (str[i])
	{
		if (str[i] == '%')
			i = ft_eval_format(&tab, str, i + 1);
		else
			tab.tl += write(1, &str[i], 1);
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

// 	res = ft_printf("0 roma [%22s], age: [%+d] (skuf), %p\n", str, 49999, str);
// 	ft_printf("%d\n", res);
// 	res = printf("0 roma [%22s], age: [%+d] (skuf), %p\n", str, 49999, str);
// 	printf("%d\n\n", res);

// 	res = ft_printf("1 %-5s %#x %#X %#.x %#.0x\n", "skuf", 4219, 4219, 0, 0);
// 	ft_printf("%d\n", res);
// 	res = printf("1 %-5s %#x %#X %#.x %#.0x\n", "skuf", 4219, 4219, 0, 0);
// 	printf("%d\n\n", res);

// 	res = ft_printf("2 [%0.4d] [%010d] [%010.5d]\n", 46469, 42, 42);
// 	ft_printf("%d\n", res);
// 	res = printf("2 [%0.4d] [%010d] [%010.5d]\n", 46469, 42, 42);
// 	printf("%d\n\n", res);

// 	res = ft_printf("3 [%+015.5d] [% 10.5i]\n", 42, 42);
// 	ft_printf("%d\n", res);
// 	res = printf("3 [%+015.5d] [% 10.5i]\n", 42, 42);
// 	printf("%d\n\n", res);

// 	res = ft_printf("4 [%.3s], [%.6s], [%10s], [%-10.2s]\n", nl, nl, nl, nl);
// 	ft_printf("%d\n", res);
// 	res = printf("4 [%.3s], [%.6s], [%10s], [%-10.2s]\n", nl, nl, nl, nl);
// 	printf("%d\n\n", res);

// 	res = ft_printf("5 [%p], [%15p], [%-15p]\n", nl, nl, nl);
// 	ft_printf("%d\n", res);
// 	res = printf("5 [%p], [%15p], [%-15p]\n", nl, nl, nl);
// 	printf("%d\n\n", res);

// 	res = ft_printf("6 void: [%.0d], [%.x], [%#.x], [%05.0d]\n", 0, 0, 0, 0);
// 	ft_printf("%d\n", res);
// 	res = printf("6 void: [%.0d], [%.x], [%#.x], [%05.0d]\n", 0, 0, 0, 0);
// 	printf("%d\n\n", res);

// 	res = ft_printf("7 %d %i\n", -2147483648, 2147483647);
// 	ft_printf("%d\n", res);
// 	res = printf("7 %d %i\n", -2147483648, 2147483647);
// 	printf("%d\n\n", res);

// 	res = ft_printf("8 %u %x %X\n", 4294967295u, 4294967295u, 4294967295u);
// 	ft_printf("%d\n", res);
// 	res = printf("8 %u %x %X\n", 4294967295u, 4294967295u, 4294967295u);
// 	printf("%d\n\n", res);

// 	res = ft_printf("9 %% %-5%% %05%%, char: %c [%-5c] [%5c]\n", 'c', 'c', 'c');
// 	ft_printf("%d\n", res);
// 	res = printf("9 %% %-5%% %05%%, char: %c [%-5c] [%5c]\n", 'c', 'c', 'c');
// 	printf("%d\n\n", res);

// 	res = ft_printf("10 [%-15.10d] [%+010d] [% d] [%#015x]\n", -42, 42, 42, 42);
// 	ft_printf("%d\n", res);
// 	res = printf("10 [%-15.10d] [%+010d] [% d] [%#015x]\n", -42, 42, 42, 42);
// 	printf("%d\n\n", res);

// 	return (0);
// }
