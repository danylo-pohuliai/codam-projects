/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/12 14:51:04 by dpohulia          #+#    #+#             */
/*   Updated: 2026/03/14 16:53:36 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

size_t	ft_strlcat(char *dst, const char *src, size_t size)
{
	size_t	d_len;
	size_t	s_len;
	size_t	j;

	d_len = 0;
	while (dst[d_len] && d_len < size)
		d_len++;
	s_len = ft_strlen(src);
	if (size <= d_len)
		return (size + s_len);
	j = 0;
	while (src[j] && (d_len + j) < (size - 1))
	{
		dst[d_len + j] = src[j];
		j++;
	}
	dst[d_len + j] = '\0';
	return (d_len + s_len);
}
