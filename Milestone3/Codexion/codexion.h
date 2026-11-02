/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dpohulia <dpohulia@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/23 12:47:08 by dpohulia          #+#    #+#             */
/*   Updated: 2026/08/06 18:20:53 by dpohulia         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CODEXION_H
# define CODEXION_H
# define EDF 1
# define FIFO 0
# include <unistd.h>
# include <stdlib.h>
# include <pthread.h>
# include <stdio.h>
# include <sys/time.h>
# include <string.h>

typedef struct s_parameters	t_parameters;

typedef struct s_request
{
	int		coder_id;
	long	arrival_time;
	long	deadline;
}	t_request;

typedef struct s_dongle
{
	pthread_mutex_t	queue_mutex;
	pthread_cond_t	cond;
	int				is_taken;
	long			available_at;
	t_request		queue[2];
	int				queue_size;
}	t_dongle;

typedef struct s_coder
{
	int				id;
	pthread_t		thread;
	t_dongle		*left_dongle;
	t_dongle		*right_dongle;
	long			last_compile;
	int				compiles_done;
	t_parameters	*param;
	pthread_mutex_t	state_mutex;
}	t_coder;

typedef struct s_parameters
{
	int				number_of_coders;
	int				time_to_burnout;
	int				time_to_compile;
	int				time_to_debug;
	int				time_to_refactor;
	int				number_of_compiles_required;
	int				dongle_cooldown;
	int				scheduler;
	int				finished_coders;
	long			start_time;
	int				stop;
	pthread_mutex_t	stop_mutex;
	pthread_t		monitor_thread;
	t_coder			*coders;
	t_dongle		*dongles;
	pthread_mutex_t	print_mutex;
	pthread_mutex_t	state_mutex;
	pthread_cond_t	stop_cond;
	pthread_t		mon_thread;
}	t_parameters;

void	print_routine(t_coder *coder, char *action, int action_len);
void	stop_simulation(t_parameters *param, int dead_coder);
void	_sleep(long duration_in_ms, t_coder *coder);

int		destroy_mut_cond(t_parameters *param, int muts, int conds, int muts_c);
void	join_threads(t_parameters	*param, int amount);
int		free_resources(int level, t_parameters *param);

int		init_simulation(t_parameters	*param);

int		ft_isspace(int c);
int		print_error(char *msg);
void	set_timespec(long duration_ms, struct timespec *ts);
long	get_time(void);
long	get_sim_time(t_parameters *param);
int		check_stop(t_parameters *param);
void	dequeue_request(t_dongle *dongle, t_coder *coder);

int		parse(char **argv, t_parameters	*param);

void	*routine(void *arg);
void	*monitor(void *arg);

void	request_dongle(t_dongle *dongle, t_coder *coder, t_parameters *param);
void	release_dongle(t_dongle *dongle, t_parameters *param);

#endif