/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstmap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/16 16:32:48 by dpohulia          #+#    #+#             */
/*   Updated: 2026/03/22 11:51:15 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

// static void	*test_iter(void *i)
// {
// 	int	*ptr;
// 	int	*new_ptr;

// 	new_ptr = malloc(sizeof(int));
// 	ptr = (int *)i;
// 	*new_ptr = *ptr + 3;
// 	return (new_ptr);
// }

// static void	test_del(void *c)
// {
// 	return ;
// }

t_list	*ft_lstmap(t_list *lst, void *(*f)(void *), void (*del)(void *))
{
	t_list	*res;
	t_list	*new_node;
	void	*new_content;

	if (!lst || !f || !del)
		return (NULL);
	res = NULL;
	while (lst)
	{
		new_content = f(lst->content);
		new_node = ft_lstnew(new_content);
		if (!new_node)
		{
			del(new_content);
			ft_lstclear(&res, del);
			return (NULL);
		}
		ft_lstadd_back(&res, new_node);
		lst = lst->next;
	}
	return (res);
}

// int main(void)
// {
// 	t_list *lst;
// 	t_list *temp;
// 	int i = 0;
// 	int i1 = 1;
// 	int i2 = 2;
// 	int i3 = 3;

// 	lst = ft_lstnew(&i);
// 	ft_lstadd_back(&lst, ft_lstnew(&i1));
// 	ft_lstadd_back(&lst, ft_lstnew(&i2));
// 	ft_lstadd_back(&lst, ft_lstnew(&i3));

// 	temp = lst;
// 	while (temp)
// 	{
// 		printf("%p %d\n", temp->content, *(int *)temp->content);
// 		temp = temp->next;
// 	}
// 	printf("------------\n");
// 	temp = ft_lstmap(lst, test_iter, test_del);
// 	while (temp)
// 	{
// 		printf("%p %d\n", temp->content, *(int *)temp->content);
// 		temp = temp->next;
// 	}
// 	printf("------------\n");
// 	temp = lst;
// 	while (temp)
// 	{
// 		printf("%p %d\n", temp->content, *(int *)temp->content);
// 		temp = temp->next;
// 	}
// 	return (0);
// }
