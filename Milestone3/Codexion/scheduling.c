/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   scheduling.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/29 10:59:17 by dpohulia          #+#    #+#             */
/*   Updated: 2026/08/06 18:20:38 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	enqueue_request(t_dongle *dongle, t_coder *coder, t_parameters *param)
{
	int	size;

	pthread_mutex_lock(&dongle->queue_mutex);
	size = dongle->queue_size;
	dongle->queue[size].coder_id = coder->id;
	dongle->queue[size].arrival_time = get_sim_time(param);
	dongle->queue[size].deadline = coder->last_compile + param->time_to_burnout;
	dongle->queue_size++;
}

int	evaluate_fifo(t_dongle *d, int targ_idx, int comp_idx)
{
	if (d->queue[targ_idx].arrival_time < d->queue[comp_idx].arrival_time)
		return (1);
	if (d->queue[targ_idx].arrival_time == d->queue[comp_idx].arrival_time)
	{
		if (d->queue[targ_idx].coder_id < d->queue[comp_idx].coder_id)
			return (1);
	}
	return (0);
}

int	evaluate_edf(t_dongle *d, int targ_idx, int comp_idx)
{
	if (d->queue[targ_idx].deadline < d->queue[comp_idx].deadline)
		return (1);
	if (d->queue[targ_idx].deadline == d->queue[comp_idx].deadline)
	{
		if (d->queue[targ_idx].coder_id < d->queue[comp_idx].coder_id)
			return (1);
	}
	return (0);
}

int	check_arbitration(t_dongle *d, int coder_id, int mode)
{
	int	target_idx;
	int	competitor_idx;

	if (d->queue_size == 1)
		return (1);
	if (d->queue[0].coder_id == coder_id)
		target_idx = 0;
	else
		target_idx = 1;
	if (target_idx == 0)
		competitor_idx = 1;
	else
		competitor_idx = 0;
	if (mode == EDF)
		return (evaluate_edf(d, target_idx, competitor_idx));
	return (evaluate_fifo(d, target_idx, competitor_idx));
}

void	request_dongle(t_dongle *dongle, t_coder *coder, t_parameters *param)
{
	struct timespec	ts;
	long			wait;

	enqueue_request(dongle, coder, param);
	while (1)
	{
		if (check_stop(param))
		{
			pthread_mutex_unlock(&dongle->queue_mutex);
			return ;
		}
		if (dongle->is_taken == 0 && get_sim_time(param) >= dongle->available_at
			&& check_arbitration(dongle, coder->id, param->scheduler))
			break ;
		if (dongle->is_taken == 0 && get_sim_time(param) < dongle->available_at)
		{
			wait = dongle->available_at - get_sim_time(param);
			set_timespec(wait, &ts);
			pthread_cond_timedwait(&dongle->cond, &dongle->queue_mutex, &ts);
		}
		else
			pthread_cond_wait(&dongle->cond, &dongle->queue_mutex);
	}
	dequeue_request(dongle, coder);
}
