/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bigger_helpers.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/29 17:42:00 by dpohulia          #+#    #+#             */
/*   Updated: 2026/08/06 18:20:57 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	append_number(char *buffer, int index, long number)
{
	char	temp[20];
	int		i;

	i = 0;
	if (number == 0)
		temp[i++] = '0';
	while (number > 0)
	{
		temp[i++] = (number % 10) + '0';
		number /= 10;
	}
	while (i > 0)
		buffer[index++] = temp[--i];
	return (index);
}

void	print_routine(t_coder *coder, char *action, int action_len)
{
	char	buffer[64];
	int		i;
	int		j;
	long	current_time;

	pthread_mutex_lock(&coder->param->print_mutex);
	if (action[0] != 'b' && check_stop(coder->param))
	{
		pthread_mutex_unlock(&coder->param->print_mutex);
		return ;
	}
	current_time = get_sim_time(coder->param);
	i = 0;
	i = append_number(buffer, i, current_time);
	buffer[i++] = ' ';
	i = append_number(buffer, i, coder->id);
	buffer[i++] = ' ';
	j = 0;
	while (j < action_len)
		buffer[i++] = action[j++];
	write(1, buffer, i);
	pthread_mutex_unlock(&coder->param->print_mutex);
}

void	_sleep(long duration_ms, t_coder *coder)
{
	struct timespec	ts;
	pthread_mutex_t	*stop_m;

	if (duration_ms <= 0)
		return ;
	set_timespec(duration_ms, &ts);
	stop_m = &coder->param->stop_mutex;
	pthread_mutex_lock(stop_m);
	while (coder->param->stop == 0)
	{
		if (pthread_cond_timedwait(&coder->param->stop_cond, stop_m, &ts) != 0)
			break ;
	}
	pthread_mutex_unlock(stop_m);
}

void	stop_simulation(t_parameters *param, int dead_coder)
{
	int	i;

	if (!check_stop(param))
	{
		pthread_mutex_lock(&param->stop_mutex);
		param->stop = 1;
		pthread_cond_broadcast(&param->stop_cond);
		pthread_mutex_unlock(&param->stop_mutex);
		i = 0;
		while (i < param->number_of_coders)
		{
			pthread_mutex_lock(&param->dongles[i].queue_mutex);
			pthread_cond_broadcast(&param->dongles[i].cond);
			pthread_mutex_unlock(&param->dongles[i].queue_mutex);
			i++;
		}
		if (dead_coder)
			print_routine(&param->coders[dead_coder - 1], "burned out\n", 11);
		return ;
	}
}

void	release_dongle(t_dongle *dongle, t_parameters *param)
{
	pthread_mutex_lock(&dongle->queue_mutex);
	dongle->is_taken = 0;
	dongle->available_at = get_sim_time(param) + param->dongle_cooldown;
	pthread_cond_signal(&dongle->cond);
	pthread_mutex_unlock(&dongle->queue_mutex);
}
