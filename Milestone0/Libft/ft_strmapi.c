/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strmapi.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/14 12:35:36 by dpohulia          #+#    #+#             */
/*   Updated: 2026/03/22 11:52:08 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

// static char	mapi_test(unsigned int index, char c)
// {
// 	char	res;

// 	res = c;
// 	if (!(index % 2))
// 		res = ft_toupper((int)c);
// 	return (res);
// }

char	*ft_strmapi(char const *s, char (*f)(unsigned int, char))
{
	char			*res;
	size_t			len;
	unsigned int	i;

	if (!s || !f)
		return (NULL);
	len = ft_strlen(s);
	res = malloc(len + 1);
	if (!res)
		return (NULL);
	i = 0;
	while (s[i])
	{
		res[i] = f(i, s[i]);
		i++;
	}
	res[i] = s[i];
	return (res);
}

// int main(void)
// {
// 	char	*str = "Hello world!!";

// 	printf("%s\n", ft_strmapi(str, mapi_test));
// 	return (0);
// }
