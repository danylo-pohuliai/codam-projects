/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   routines.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/27 10:55:43 by dpohulia          #+#    #+#             */
/*   Updated: 2026/08/06 18:20:40 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	take_dongles_without_deadlock(t_coder	*coder)
{
	if (coder->id % 2)
	{
		request_dongle(coder->left_dongle, coder, coder->param);
		print_routine(coder, "has taken a dongle\n", 19);
		request_dongle(coder->right_dongle, coder, coder->param);
		print_routine(coder, "has taken a dongle\n", 19);
	}
	else
	{
		request_dongle(coder->right_dongle, coder, coder->param);
		print_routine(coder, "has taken a dongle\n", 19);
		request_dongle(coder->left_dongle, coder, coder->param);
		print_routine(coder, "has taken a dongle\n", 19);
	}
	return ;
}

void	coder_routine(t_coder *coder, int comp_req)
{
	while ((!check_stop(coder->param)) && (coder->compiles_done < comp_req))
	{
		take_dongles_without_deadlock(coder);
		pthread_mutex_lock(&coder->state_mutex);
		coder->last_compile = get_sim_time(coder->param);
		coder->compiles_done++;
		pthread_mutex_unlock(&coder->state_mutex);
		print_routine(coder, "is compiling\n", 13);
		_sleep(coder->param->time_to_compile, coder);
		release_dongle(coder->left_dongle, coder->param);
		release_dongle(coder->right_dongle, coder->param);
		print_routine(coder, "is debugging\n", 13);
		_sleep(coder->param->time_to_debug, coder);
		print_routine(coder, "is refactoring\n", 15);
		_sleep(coder->param->time_to_refactor, coder);
	}
	if ((!check_stop(coder->param)) && (coder->compiles_done == comp_req))
	{
		pthread_mutex_lock(&coder->param->state_mutex);
		coder->param->finished_coders++;
		pthread_mutex_unlock(&coder->param->state_mutex);
	}
}

void	*routine(void *arg)
{
	t_coder	*coder;
	int		compiles_required;

	coder = (t_coder *)arg;
	pthread_mutex_lock(&coder->param->state_mutex);
	pthread_mutex_unlock(&coder->param->state_mutex);
	pthread_mutex_lock(&coder->param->state_mutex);
	compiles_required = coder->param->number_of_compiles_required;
	pthread_mutex_unlock(&coder->param->state_mutex);
	pthread_mutex_lock(&coder->state_mutex);
	coder->last_compile = get_sim_time(coder->param);
	pthread_mutex_unlock(&coder->state_mutex);
	if (coder->param->number_of_coders == 1 && compiles_required != 0)
	{
		request_dongle(coder->left_dongle, coder, coder->param);
		print_routine(coder, "has taken a dongle\n", 19);
		_sleep(coder->param->time_to_burnout + 10, coder);
		return (NULL);
	}
	coder_routine(coder, compiles_required);
	return (NULL);
}

int	check_coder_burnout(t_parameters *param)
{
	int		i;
	long	time;

	i = 0;
	while (i < param->number_of_coders)
	{
		pthread_mutex_lock(&param->coders[i].state_mutex);
		time = get_sim_time(param) - param->coders[i].last_compile;
		if (param->coders[i].compiles_done != param->number_of_compiles_required
			&& time > (long)param->time_to_burnout)
		{
			pthread_mutex_unlock(&param->coders[i].state_mutex);
			stop_simulation(param, param->coders[i].id);
			return (0);
		}
		pthread_mutex_unlock(&param->coders[i].state_mutex);
		i++;
	}
	return (1);
}

void	*monitor(void *arg)
{
	t_parameters	*param;
	int				finished_coders;

	param = (t_parameters *)arg;
	pthread_mutex_lock(&param->state_mutex);
	pthread_mutex_unlock(&param->state_mutex);
	while (!check_stop(param))
	{
		pthread_mutex_lock(&param->state_mutex);
		finished_coders = param->finished_coders;
		pthread_mutex_unlock(&param->state_mutex);
		if (param->number_of_coders == finished_coders)
		{
			stop_simulation(param, 0);
			return (NULL);
		}
		if (!check_coder_burnout(param))
			return (NULL);
		usleep(1000);
	}
	return (NULL);
}
