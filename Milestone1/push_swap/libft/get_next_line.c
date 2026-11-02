/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/31 14:04:30 by dpohulia          #+#    #+#             */
/*   Updated: 2026/04/20 12:38:06 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

char	*ft_join(char *dest, char *src, size_t n)
{
	size_t	dest_len;
	char	*res;

	if (!dest)
	{
		res = malloc(n + 1);
		if (!res)
			return (NULL);
		ft_memcpy(res, src, n);
		res[n] = '\0';
		return (res);
	}
	dest_len = ft_strlen(dest);
	res = malloc(dest_len + n + 1);
	if (!res)
	{
		free (dest);
		return (NULL);
	}
	ft_memcpy(res, dest, dest_len);
	free(dest);
	ft_memcpy(res + dest_len, src, n);
	res[dest_len + n] = '\0';
	return (res);
}

int	check_buf(int fd, char *buf, char **res, t_my_list **head)
{
	size_t	i;

	i = 0;
	while (buf[i])
	{
		if (buf[i] == '\n')
		{
			*res = ft_join(*res, buf, i + 1);
			if (!*res)
				return (1);
			if (buf[i + 1] && !create_node(fd, buf + i + 1, head))
			{
				free(*res);
				*res = NULL;
			}
			return (1);
		}
		i++;
	}
	*res = ft_join(*res, buf, i);
	if (!*res)
		return (1);
	return (0);
}

char	*look_for_remainings(int fd, t_my_list **head)
{
	char		*res;
	t_my_list	*temp;
	t_my_list	*prev;

	temp = *head;
	prev = NULL;
	while (temp)
	{
		if (temp->fd == fd)
		{
			res = temp->remainings;
			if (!prev)
				*head = temp->next;
			else
				prev->next = temp->next;
			free(temp);
			return (res);
		}
		prev = temp;
		temp = temp->next;
	}
	return (NULL);
}

char	*read_file(int fd, char *res, t_my_list **head)
{
	char	*buf;
	ssize_t	bytes_read;

	buf = malloc((size_t)BUFFER_SIZE + 1);
	if (!buf)
	{
		free(res);
		return (NULL);
	}
	bytes_read = read(fd, buf, BUFFER_SIZE);
	while (bytes_read > 0)
	{
		buf[bytes_read] = '\0';
		if (check_buf(fd, buf, &res, head))
			break ;
		bytes_read = read(fd, buf, BUFFER_SIZE);
	}
	if (bytes_read == -1)
	{
		free(res);
		res = NULL;
	}
	free(buf);
	return (res);
}

char	*get_next_line(int fd)
{
	static t_my_list	*head = NULL;
	char				*res;
	char				*rem;

	if (fd < 0 || BUFFER_SIZE <= 0)
		return (NULL);
	res = NULL;
	rem = look_for_remainings(fd, &head);
	if (rem)
	{
		if (check_buf(fd, rem, &res, &head))
		{
			free(rem);
			return (res);
		}
		free(rem);
	}
	return (read_file(fd, res, &head));
}

// int	main(void)
// {
// 	int	fd;
// 	int fd1;

// 	fd = open("text.txt", O_RDONLY);
// 	fd1 = open("text1.txt", O_RDONLY);
// 	printf("%s", get_next_line(fd));
// 	printf("---------------\n");
// 	printf("%s", get_next_line(fd));
// 	printf("---------------\n");
// 	printf("%s", get_next_line(fd1));
// 	printf("---------------\n");
// 	printf("%s", get_next_line(fd));
// 	printf("---------------\n");
// 	printf("%s", get_next_line(fd1));
// 	printf("---------------\n");
// 	printf("%s", get_next_line(fd));
// 	printf("%s", get_next_line(fd));
// 	printf("---------------\n");
// 	printf("%s", get_next_line(fd));
// 	printf("---------------\n");
// 	printf("%s", get_next_line(fd1));
// 	close(fd);
// 	return (0);
// }
