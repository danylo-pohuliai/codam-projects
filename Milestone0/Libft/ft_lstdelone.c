/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstdelone.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/16 16:31:30 by dpohulia          #+#    #+#             */
/*   Updated: 2026/03/18 14:43:45 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_lstdelone(t_list *lst, void (*del)(void*))
{
	if (!lst || !del)
		return ;
	del(lst->content);
	free(lst);
}

// int main(void)
// {
// 	char *cont1 = ft_strdup("jfjsa");
// 	char *cont2 = ft_strdup("pizza");
// 	char *cont3 = ft_strdup("4216");
// 	t_list *lst;
// 	t_list *temp;

// 	lst = ft_lstnew(cont1);
// 	ft_lstadd_front(&lst, ft_lstnew(cont2));
// 	ft_lstadd_front(&lst, ft_lstnew(cont3));
// 	temp = lst;
// 	while (temp)
// 	{
// 		printf("%s\n", (char *)temp->content);
// 		temp = temp->next;
// 	}
// 	ft_lstdelone(ft_lstlast(lst), &free);
// 	printf("\n\n");
// 	while (lst)
// 	{
// 		printf("%s\n", (char *)lst->content);
// 		lst = lst->next;
// 	}
// }
