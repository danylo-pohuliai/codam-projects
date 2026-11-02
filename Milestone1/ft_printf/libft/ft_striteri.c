/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_striteri.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/14 12:35:57 by dpohulia          #+#    #+#             */
/*   Updated: 2026/03/22 11:51:53 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

// static char	iteri_test(unsigned int index, char *c)
// {
// 	if (!(index % 2))
// 		*c = ft_toupper((int)*c);
// 	return (*c);
// }

void	ft_striteri(char *s, void (*f)(unsigned int, char*))
{
	unsigned int	i;

	if (!s || !f)
		return ;
	i = 0;
	while (s[i])
	{
		f(i, s + i);
		i++;
	}
}

// int main(void)
// {
// 	char	str[] = "Hello world!!";

// 	ft_striteri(str, iteri_test);
// 	printf("%s\n", str);
// 	return (0);
// }
