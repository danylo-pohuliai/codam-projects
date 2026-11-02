/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   checker.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/24 15:11:52 by dpohulia          #+#    #+#             */
/*   Updated: 2026/04/24 18:15:00 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	apply_command(t_app *app, char *command)
{
	if (!ft_strncmp(command, "sa\n", 3))
		do_sa(app);
	else if (!ft_strncmp(command, "sb\n", 3))
		do_sb(app);
	else if (!ft_strncmp(command, "ss\n", 3))
		do_ss(app);
	else if (!ft_strncmp(command, "pa\n", 3))
		do_pa(app);
	else if (!ft_strncmp(command, "pb\n", 3))
		do_pb(app);
	else if (!ft_strncmp(command, "ra\n", 3))
		do_ra(app);
	else if (!ft_strncmp(command, "rb\n", 3))
		do_rb(app);
	else if (!ft_strncmp(command, "rr\n", 3))
		do_rr(app);
	else if (!ft_strncmp(command, "rra\n", 4))
		do_rra(app);
	else if (!ft_strncmp(command, "rrb\n", 4))
		do_rrb(app);
	else if (!ft_strncmp(command, "rrr\n", 4))
		do_rrr(app);
	else
		print_error_allocated(NULL, app);
}

void	apply_commands(t_app *app)
{
	char	*command;

	command = get_next_line(0);
	while (command)
	{
		apply_command(app, command);
		free(command);
		command = get_next_line(0);
	}
	if (is_sorted(app->a) && app->b->size == 0)
		write(1, "OK\n", 3);
	else
		write(1, "KO\n", 3);
}

int	main(int argc, char **argv)
{
	t_app	app;

	ft_bzero(&app, sizeof(t_app));
	app.config.checker = 1;
	parse_and_validate(argc, argv, &app);
	app.b = init_ring(app.a->capacity);
	apply_commands(&app);
	free_ring(app.a);
	free_ring(app.b);
	return (0);
}
