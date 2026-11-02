/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/14 12:35:16 by dpohulia          #+#    #+#             */
/*   Updated: 2026/03/17 18:30:32 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_itoa(int n)
{
	char	buf[12];
	long	number;
	size_t	i;

	number = n;
	if (number < 0)
		number = -number;
	i = 11;
	buf[i] = '\0';
	if (number == 0)
		buf[--i] = '0';
	while (number > 0)
	{
		i--;
		buf[i] = (number % 10) + '0';
		number = number / 10;
	}
	if (n < 0)
	{
		i--;
		buf[i] = '-';
	}
	return (ft_strdup(&buf[i]));
}
// void	ft_print_result(char const *s)
// {
// 	int		len;

// 	len = 0;
// 	while (s[len])
// 		len++;
// 	write(1, s, len);
// }

// int		main(int argc, const char *argv[])
// {
// 	int		arg;

// 	if (argc == 1)
// 		return (0);
// 	else if ((arg = atoi(argv[1])) == 1)
// 	{
// 		char *res = ft_itoa(0);
// 		ft_print_result(res);
// 		free(res);
// 	}
// 	else if (arg == 2)
// 	{
// 		char *res = ft_itoa(9);
// 		ft_print_result(res);
// 		free(res);
// 	}
// 	else if (arg == 3)
// 	{
// 		char *res = ft_itoa(-9);
// 		ft_print_result(res);
// 		free(res);
// 	}
// 	else if (arg == 4)
// 	{
// 		char *res = ft_itoa(10);
// 		ft_print_result(res);
// 		free(res);
// 	}
// 	else if (arg == 5)
// 	{
// 		char *res = ft_itoa(-10);
// 		ft_print_result(res);
// 		free(res);
// 	}
// 	else if (arg == 6)
// 	{
// 		char *res = ft_itoa(8124);
// 		ft_print_result(res);
// 		free(res);
// 	}
// 	else if (arg == 7)
// 	{
// 		char *res = ft_itoa(-9874);
// 		ft_print_result(res);
// 		free(res);
// 	}
// 	else if (arg == 8)
// 	{
// 		char *res = ft_itoa(543000);
// 		ft_print_result(res);
// 		free(res);
// 	}
// 	else if (arg == 9)
// 	{
// 		char *res = ft_itoa(-2147483648LL);
// 		ft_print_result(res);
// 		free(res);
// 	}
// 	else if (arg == 10)
// 	{
// 		char *res = ft_itoa(2147483647);
// 		ft_print_result(res);
// 		free(res);
// 	}
// 	return (0);
// }
