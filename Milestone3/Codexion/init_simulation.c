/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init_simulation.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/27 10:55:35 by dpohulia          #+#    #+#             */
/*   Updated: 2026/08/06 18:20:48 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	init_dongles(t_parameters	*param)
{
	int	i;

	i = 0;
	while (i < param->number_of_coders)
	{
		param->dongles[i].is_taken = 0;
		param->dongles[i].available_at = 0;
		param->dongles[i].queue_size = 0;
		if (pthread_mutex_init(&param->dongles[i].queue_mutex, NULL))
			return (destroy_mut_cond(param, i, 0, 0));
		i++;
	}
	i = 0;
	while (i < param->number_of_coders)
	{
		if (pthread_cond_init(&param->dongles[i].cond, NULL))
			return (destroy_mut_cond(param, param->number_of_coders, i, 0));
		i++;
	}
	return (1);
}

int	init_coders(t_parameters *param)
{
	int	i;
	int	coders_am;

	i = 0;
	coders_am = param->number_of_coders;
	while (i < coders_am)
	{
		param->coders[i].id = i + 1;
		param->coders[i].compiles_done = 0;
		param->coders[i].param = param;
		param->coders[i].last_compile = 0;
		param->coders[i].left_dongle = &param->dongles[i];
		param->coders[i].right_dongle = &param->dongles[(i + 1) % coders_am];
		if (pthread_mutex_init(&param->coders[i].state_mutex, NULL))
			return (destroy_mut_cond(param, coders_am, coders_am, i));
		i++;
	}
	return (1);
}

int	init_param_mut_cond(t_parameters *param)
{
	if (pthread_mutex_init(&param->stop_mutex, NULL))
		return (free_resources(1, param));
	if (pthread_mutex_init(&param->print_mutex, NULL))
		return (free_resources(2, param));
	if (pthread_mutex_init(&param->state_mutex, NULL))
		return (free_resources(3, param));
	if (pthread_cond_init(&param->stop_cond, NULL))
		return (free_resources(4, param));
	return (1);
}

int	create_threads(t_parameters	*param, t_coder	*coder)
{
	int		i;

	if (pthread_create(&param->mon_thread, NULL, monitor, (void *)param))
	{
		pthread_mutex_unlock(&param->state_mutex);
		return (print_error("failed to create monitor thread"));
	}
	i = 0;
	while (i < param->number_of_coders)
	{
		coder = &param->coders[i];
		if (pthread_create(&coder->thread, NULL, routine, (void *)coder))
		{
			pthread_mutex_lock(&param->stop_mutex);
			param->stop = 1;
			pthread_mutex_unlock(&param->stop_mutex);
			pthread_mutex_unlock(&param->state_mutex);
			pthread_join(param->mon_thread, NULL);
			join_threads(param, i);
			return (0);
		}
		usleep(1000);
		i++;
	}
	return (1);
}

int	init_simulation(t_parameters	*param)
{
	t_coder	*coder;

	coder = NULL;
	param->finished_coders = 0;
	param->stop = 0;
	param->coders = malloc(sizeof(t_coder) * param->number_of_coders);
	if (!param->coders)
		return (print_error("first malloc failed"));
	param->dongles = malloc(sizeof(t_dongle) * param->number_of_coders);
	if (!param->dongles)
	{
		free(param->coders);
		return (print_error("second malloc failed"));
	}
	if (!init_dongles(param))
		return (free_resources(0, param));
	if (!init_coders(param))
		return (free_resources(0, param));
	if (!init_param_mut_cond(param))
		return (print_error("general mutexes/conditions init failed"));
	pthread_mutex_lock(&param->state_mutex);
	if (!create_threads(param, coder))
		return (free_resources(5, param));
	return (1);
}
