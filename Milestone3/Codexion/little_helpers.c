/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   little_helpers.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/25 15:32:58 by dpohulia          #+#    #+#             */
/*   Updated: 2026/08/06 18:20:46 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	ft_isspace(int c)
{
	if (c == ' ' || c == '\f' || c == '\n'
		|| c == '\r' || c == '\t' || c == '\v')
		return (1);
	return (0);
}

int	print_error(char *msg)
{
	fprintf(stderr, "[Codexion] Error: %s\n", msg);
	return (0);
}

int	check_stop(t_parameters *param)
{
	int	stop;

	pthread_mutex_lock(&param->stop_mutex);
	stop = param->stop;
	pthread_mutex_unlock(&param->stop_mutex);
	return (stop);
}

void	set_timespec(long duration_ms, struct timespec *ts)
{
	struct timeval	tv;

	gettimeofday(&tv, NULL);
	tv.tv_sec += duration_ms / 1000;
	tv.tv_usec += (duration_ms % 1000) * 1000;
	if (tv.tv_usec >= 1000000)
	{
		tv.tv_sec++;
		tv.tv_usec -= 1000000;
	}
	ts->tv_sec = tv.tv_sec;
	ts->tv_nsec = tv.tv_usec * 1000;
}

void	dequeue_request(t_dongle *dongle, t_coder *coder)
{
	dongle->is_taken = 1;
	if (dongle->queue[0].coder_id == coder->id)
		dongle->queue[0] = dongle->queue[1];
	dongle->queue_size--;
	pthread_mutex_unlock(&dongle->queue_mutex);
}
