/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/20 12:47:23 by dpohulia          #+#    #+#             */
/*   Updated: 2026/04/28 15:41:54 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

float	compute_disorder(t_ring *ring)
{
	float	mistakes;
	float	total_pairs;
	int		i;
	int		j;

	if (ring->size <= 1)
		return (0.0f);
	mistakes = 0;
	total_pairs = 0;
	i = 0;
	while (i < ring->size - 1)
	{
		j = i + 1;
		while (j < ring->size)
		{
			total_pairs++;
			if (ring->data[i] > ring->data[j])
				mistakes++;
			j++;
		}
		i++;
	}
	return (mistakes / total_pairs);
}

void	choose_strategy(t_app *app)
{
	if (app->config.disorder < 0.2f)
		app->config.strategy = STRAT_SIMPLE;
	else if (app->config.disorder < 0.5f)
		app->config.strategy = STRAT_MEDIUM;
	else
		app->config.strategy = STRAT_COMPLEX;
}

void	run_sort(t_app *app)
{
	if (is_sorted(app->a))
		return ;
	if (app->a->size <= 5)
	{
		if (app->a->size == 2)
			do_sa(app);
		else if (app->a->size == 3)
			hard_3(app);
		else if (app->a->size == 4)
			hard_4(app);
		else if (app->a->size == 5)
			hard_5(app);
		return ;
	}
	if (app->config.strategy == STRAT_ADAPTIVE)
		choose_strategy(app);
	if (app->config.strategy == STRAT_SIMPLE)
		sort_simple(app);
	else if (app->config.strategy == STRAT_MEDIUM)
		sort_medium(app);
	else if (app->config.strategy == STRAT_COMPLEX)
		sort_complex(app);
}

int	main(int argc, char **argv)
{
	t_app	app;

	ft_bzero(&app, sizeof(t_app));
	app.config.strategy = STRAT_ADAPTIVE;
	parse_and_validate(argc, argv, &app);
	app.b = init_ring(app.a->capacity);
	app.config.disorder = compute_disorder(app.a);
	run_sort(&app);
	if (app.config.bench_mode)
		print_benchmark(&app);
	free_ring(app.a);
	free_ring(app.b);
	return (0);
}
