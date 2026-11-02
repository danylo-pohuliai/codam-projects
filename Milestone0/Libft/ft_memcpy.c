/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcpy.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/12 13:45:30 by dpohulia          #+#    #+#             */
/*   Updated: 2026/03/17 18:09:36 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memcpy(void *dest, const void *src, size_t n)
{
	size_t				i;
	unsigned char		*d;
	const unsigned char	*s;

	if (!dest && !src)
		return (NULL);
	d = (unsigned char *)dest;
	s = (const unsigned char *)src;
	i = 0;
	while (i < n)
	{
		d[i] = s[i];
		i++;
	}
	return (dest);
}

// int		main(int argc, const char *argv[])
// {
// 	void	*mem;
// 	int		arg;

// 	if (!(mem = malloc(sizeof(*mem) * 30)) || argc == 1)
// 		return (0);
// 	memset(mem, 'j', 30);
// 	if ((arg = atoi(argv[1])) == 1)
// 	{
// 		if (mem != ft_memcpy(mem, "zyxwvutsrqponmlkjihgfedcba", 14))
// 			write(1, "dest's adress was not returned\n", 31);
// 		write(1, mem, 30);
// 	}
// 	else if (arg == 2)
// 	{
// 		if (mem != ft_memcpy(mem, "zyxwvutst", 0))
// 			write(1, "dest's adress was not returned\n", 31);
// 		write(1, mem, 30);
// 	}
// 	else if (arg == 3)
// 	{
// 		if (mem != ft_memcpy(mem, "zy\0xw\0vu\0\0tsr", 11))
// 			write(1, "dest's adress was not returned\n", 31);
// 		write(1, mem, 30);
// 	}
// 	return (0);
// }
