/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstiter.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/16 16:32:21 by dpohulia          #+#    #+#             */
/*   Updated: 2026/03/22 11:51:07 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

// static void	test_iter(void *i)
// {
// 	int	*ptr;

// 	ptr = (int *)i;
// 	*ptr = *ptr + 3;
// }

void	ft_lstiter(t_list *lst, void (*f)(void *))
{
	if (!lst || !f)
		return ;
	while (lst)
	{
		f(lst->content);
		lst = lst->next;
	}
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
// 		printf("%d\n", *(int *)temp->content);
// 		temp = temp->next;
// 	}
// 	printf("------------\n");
// 	ft_lstiter(lst, test_iter);
// 	while (lst)
// 	{
// 		printf("%d\n", *(int *)lst->content);
// 		lst = lst->next;
// 	}
// 	return (0);
// }
