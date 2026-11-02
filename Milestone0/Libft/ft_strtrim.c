/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strtrim.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/14 12:34:24 by dpohulia          #+#    #+#             */
/*   Updated: 2026/03/20 19:44:12 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strtrim(char const *s1, char const *set)
{
	size_t	start;
	size_t	len;

	start = 0;
	while (ft_strchr(set, s1[start]))
		start++;
	len = ft_strlen(s1);
	while (ft_strchr(set, s1[len - 1]))
		len--;
	return (ft_substr(s1, start, len - start));
}

// int main(void)
// {
// 	printf("%s\n", ft_strtrim("vcvcss Danylo 12 vcvv", "vcvcss Danylo  vcvv"));
// 	return (0);
// }
