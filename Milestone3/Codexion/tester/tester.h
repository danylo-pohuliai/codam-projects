#ifndef TESTER_H
# define TESTER_H

# include <stdlib.h>
# include <pthread.h>

void	*tester_malloc(size_t size);
void	tester_free(void *ptr);
int		tester_pthread_mutex_init(pthread_mutex_t *mutex, const pthread_mutexattr_t *attr);
int		tester_pthread_mutex_destroy(pthread_mutex_t *mutex);
int		tester_pthread_cond_init(pthread_cond_t *cond, const pthread_condattr_t *attr);
int		tester_pthread_cond_destroy(pthread_cond_t *cond);
int		tester_pthread_create(pthread_t *thread, const pthread_attr_t *attr, void *(*start_routine)(void *), void *arg);
int		tester_pthread_join(pthread_t thread, void **retval);
int		tester_pthread_detach(pthread_t thread);

#  define malloc(size) tester_malloc(size)
#  define free(ptr) tester_free(ptr)
#  define pthread_mutex_init(m, a) tester_pthread_mutex_init(m, a)
#  define pthread_mutex_destroy(m) tester_pthread_mutex_destroy(m)
#  define pthread_cond_init(c, a) tester_pthread_cond_init(c, a)
#  define pthread_cond_destroy(c) tester_pthread_cond_destroy(c)
#  define pthread_create(t, a, s, arg) tester_pthread_create(t, a, s, arg)
#  define pthread_join(t, r) tester_pthread_join(t, r)
#  define pthread_detach(t) tester_pthread_detach(t)

#endif