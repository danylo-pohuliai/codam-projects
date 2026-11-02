/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/23 12:47:02 by dpohulia          #+#    #+#             */
/*   Updated: 2026/08/06 18:20:55 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

long	get_time(void)
{
	struct timeval	tv;
	long			time;

	if (gettimeofday(&tv, NULL) == -1)
		return (-1);
	time = (tv.tv_sec * 1000) + (tv.tv_usec / 1000);
	return (time);
}

long	get_sim_time(t_parameters *param)
{
	return (get_time() - param->start_time);
}

void	run_simulation(t_parameters	*param)
{
	param->start_time = get_time();
	pthread_mutex_unlock(&param->state_mutex);
	pthread_join(param->mon_thread, NULL);
	free_resources(6, param);
}

int	main(int argc, char **argv)
{
	t_parameters	param;

	if (argc != 9)
	{
		printf("Usage: ./codexion number_of_coders time_to_burnout");
		printf(" time_to_compile time_to_debug time_to_refactor ");
		printf("number_of_compiles_required dongle_cooldown scheduler\n");
		printf("Example: ./codexion 10 250 70 20 30 8 10 edf\n");
		return (1);
	}
	if (!parse(argv, &param))
		return (1);
	if (!init_simulation(&param))
		return (1);
	run_simulation(&param);
	return (0);
}
