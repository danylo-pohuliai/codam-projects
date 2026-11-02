/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/24 13:56:08 by dpohulia          #+#    #+#             */
/*   Updated: 2026/03/31 12:26:26 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H

# include <stdio.h>
# include <stdarg.h>
# include <stdlib.h>
# include <unistd.h>
# include "libft/libft.h"

typedef struct s_print
{
	va_list	args;
	int		wdt;
	int		prc;
	int		tl;
	char	type;
	char	zero;
	char	pnt;
	char	dash;
	char	sign;
	char	is_zero;
	char	space;
	char	hash;
}	t_print;

int		ft_printf(const char *str, ...);
void	ft_initialise_tab(t_print *tab);
int		ft_eval_format(t_print *tab, const char *str, int i);
void	ft_print_controller(t_print *tab);
int		ft_parse_flags(t_print *tab, const char *str, int i);
int		ft_parse_width(t_print *tab, const char *str, int i);
int		ft_parse_precision(t_print *tab, const char *str, int i);
void	ft_print_char(t_print *tab);
void	ft_print_str(t_print *tab);
void	ft_print_ptr(t_print *tab);
int		ft_is_specifier(int c);
int		ft_is_flag(int c);
void	ft_print_hex(t_print *tab);
void	ft_print_int(t_print *tab);
void	ft_print_unsigned(t_print *tab);
int		ft_numlen_unsigned(unsigned int n);
int		ft_hexlen(unsigned long n);
int		ft_numlen(long n);
void	ft_pad(t_print *tab, int count, char c);
void	ft_puthex(t_print *tab, unsigned long n, char type);
void	ft_putnbr(t_print *tab, unsigned long n);

#endif