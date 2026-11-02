/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_utils.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/31 14:04:26 by dpohulia          #+#    #+#             */
/*   Updated: 2026/04/20 12:38:04 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

int	create_node(int fd, char *content, t_my_list **head)
{
	t_my_list	*new;
	t_my_list	*temp;

	new = malloc(sizeof(t_my_list));
	if (!new)
		return (0);
	new->remainings = ft_strdup(content);
	if (!new->remainings)
	{
		free(new);
		return (0);
	}
	new->fd = fd;
	new->next = NULL;
	if (!*head)
		*head = new;
	else
	{
		temp = *head;
		while (temp->next)
			temp = temp->next;
		temp->next = new;
	}
	return (1);
}
