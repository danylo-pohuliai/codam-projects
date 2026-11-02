/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/14 12:34:52 by dpohulia          #+#    #+#             */
/*   Updated: 2026/03/17 15:48:03 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static	size_t	count_words(char const *s, char c)
{
	size_t	i;
	size_t	res;

	i = 0;
	res = 0;
	while (s[i])
	{
		if (s[i] != c && (s[i + 1] == c || s[i + 1] == '\0'))
			res++;
		i++;
	}
	return (res);
}

static	char	*ft_word(char const *s, char c)
{
	char	*res;
	size_t	i;

	i = 0;
	while (s[i] && s[i] != c)
		i++;
	res = malloc(i + 1);
	if (!res)
		return (NULL);
	ft_strlcpy(res, s, i + 1);
	return (res);
}

static void	*free_array(char **res, size_t n)
{
	size_t	i;

	i = 0;
	while (i < n)
	{
		free(res[i]);
		i++;
	}
	free(res);
	return (NULL);
}

char	**ft_split(char const *s, char c)
{
	char	**res;
	size_t	i;

	if (!s)
		return (NULL);
	res = malloc(sizeof(char *) * (count_words(s, c) + 1));
	if (!res)
		return (NULL);
	i = 0;
	while (*s)
	{
		while (*s == c)
			s++;
		if (*s)
		{
			res[i] = ft_word(s, c);
			if (!res[i])
				return (free_array(res, i));
			while (*s != c && *s != '\0')
				s++;
			i++;
		}
	}
	res[i] = NULL;
	return (res);
}

// int	main(void)
// {
// 	char	*str = "xxxxxxRoman 33xxxabxxxxx21";
// 	char	sep = 'o';
// 	char	**res;
// 	int		i;
// 	int		j;

// 	res = ft_split(str, sep);
// 	if (!res)
// 		return (0);
// 	i = 0;
// 	while (res[i])
// 	{
// 		j = 0;
// 		while (res[i][j])
// 		{
// 			write(1, &(res[i][j]), 1);
// 			j++;
// 		}
// 		write(1, "\n", 1);
// 		i++;
// 	}
// 	return (0);
// }
