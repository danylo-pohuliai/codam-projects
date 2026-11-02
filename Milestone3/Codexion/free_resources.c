/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   free_resources.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/29 17:40:32 by dpohulia          #+#    #+#             */
/*   Updated: 2026/08/06 18:20:50 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	destroy_mut_cond(t_parameters *param, int muts, int conds, int muts_c)
{
	if (muts != param->number_of_coders && muts != 0)
		print_error("dongles mutex init failed");
	if (conds != param->number_of_coders && conds != 0)
		print_error("dongles condition init failed");
	if (muts_c != param->number_of_coders && muts_c != 0)
		print_error("coders mutexes init failed");
	while (--muts >= 0)
		pthread_mutex_destroy(&param->dongles[muts].queue_mutex);
	while (--conds >= 0)
		pthread_cond_destroy(&param->dongles[conds].cond);
	while (--muts_c >= 0)
		pthread_mutex_destroy(&param->coders[muts_c].state_mutex);
	return (0);
}

void	join_threads(t_parameters	*param, int amount)
{
	int		i;
	t_coder	*coder;

	i = 0;
	if (amount != param->number_of_coders && amount != 0)
		print_error("failed to create coder's threads");
	while (i < amount)
	{
		coder = &param->coders[i];
		pthread_join(coder->thread, NULL);
		i++;
	}
	return ;
}

int	free_resources(int level, t_parameters *param)
{
	int	amount;

	amount = param->number_of_coders;
	if (level >= 6)
		join_threads(param, amount);
	if (level >= 5)
		pthread_cond_destroy(&param->stop_cond);
	if (level >= 4)
		pthread_mutex_destroy(&param->state_mutex);
	if (level >= 3)
		pthread_mutex_destroy(&param->print_mutex);
	if (level >= 2)
		pthread_mutex_destroy(&param->stop_mutex);
	if (level >= 1)
		destroy_mut_cond(param, amount, amount, amount);
	if (level >= 0)
	{
		free(param->coders);
		free(param->dongles);
	}
	return (0);
}
