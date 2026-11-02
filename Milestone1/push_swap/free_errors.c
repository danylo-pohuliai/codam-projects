/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   free_errors.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/20 12:45:20 by dpohulia          #+#    #+#             */
/*   Updated: 2026/04/24 17:52:37 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	free_char_array(char **res)
{
	int	j;

	j = 0;
	while (res[j])
	{
		free(res[j]);
		j++;
	}
	free(res);
}

void	free_ring(t_ring *ring)
{
	if (!ring)
		return ;
	if (ring->data)
		free(ring->data);
	free(ring);
}

void	print_error(void)
{
	write(2, "Error\n", 6);
	exit(1);
}

void	print_error_allocated(char **args, t_app *app)
{
	if (app->data_allocated && args)
		free_char_array(args);
	if (app->a)
		free_ring(app->a);
	print_error();
}
