#include <stdlib.h>
#include <pthread.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>

#undef malloc
#undef free
#undef pthread_mutex_init
#undef pthread_mutex_destroy
#undef pthread_cond_init
#undef pthread_cond_destroy
#undef pthread_create
#undef pthread_join
#undef pthread_detach

static volatile int created_mutexes = 0;
static volatile int destroyed_mutexes = 0;
static volatile int created_conds = 0;
static volatile int destroyed_conds = 0;
static volatile int created_threads = 0;
static volatile int joined_threads = 0;
static volatile int allocated_mallocs = 0;
static volatile int freed_mallocs = 0;

static int fail_malloc_at = 0;
static int fail_mutex_at = 0;
static int fail_cond_at = 0;
static int fail_thread_at = 0;

__attribute__((constructor)) static void setup_tester(void) {
    char *target;
    if ((target = getenv("FAIL_MALLOC_AT"))) fail_malloc_at = atoi(target);
    if ((target = getenv("FAIL_MUTEX_AT"))) fail_mutex_at = atoi(target);
    if ((target = getenv("FAIL_COND_AT"))) fail_cond_at = atoi(target);
    if ((target = getenv("FAIL_THREAD_AT"))) fail_thread_at = atoi(target);
}

__attribute__((destructor)) static void teardown_tester(void) {
    char msg[256];
    snprintf(msg, sizeof(msg), "[INJECTOR_STATS] Mallocs: %d/%d, Mutexes: %d/%d, Conds: %d/%d, Threads: %d/%d\n",
             freed_mallocs, allocated_mallocs,
             destroyed_mutexes, created_mutexes,
             destroyed_conds, created_conds,
             joined_threads, created_threads);
    write(2, msg, strlen(msg));
}

void *tester_malloc(size_t size) {
    static int malloc_counter = 0;
    if (fail_malloc_at > 0) {
        int current = __sync_add_and_fetch(&malloc_counter, 1);
        if (current == fail_malloc_at) {
            char msg[64];
            snprintf(msg, sizeof(msg), "[INJECTOR] Blocked malloc #%d!\n", fail_malloc_at);
            write(2, msg, strlen(msg));
            return NULL;
        }
    }
    void *res = malloc(size);
    if (res) __sync_add_and_fetch(&allocated_mallocs, 1);
    return res;
}

void tester_free(void *ptr) {
    if (ptr) __sync_add_and_fetch(&freed_mallocs, 1);
    free(ptr);
}

int tester_pthread_mutex_init(pthread_mutex_t *mutex, const pthread_mutexattr_t *attr) {
    static int mutex_counter = 0;
    if (fail_mutex_at > 0) {
        int current = __sync_add_and_fetch(&mutex_counter, 1);
        if (current == fail_mutex_at) {
            char msg[64];
            snprintf(msg, sizeof(msg), "[INJECTOR] Blocked pthread_mutex_init #%d!\n", fail_mutex_at);
            write(2, msg, strlen(msg));
            return 12;
        }
    }
    int res = pthread_mutex_init(mutex, attr);
    if (res == 0) __sync_add_and_fetch(&created_mutexes, 1);
    return res;
}

int tester_pthread_mutex_destroy(pthread_mutex_t *mutex) {
    int res = pthread_mutex_destroy(mutex);
    if (res == 0) __sync_add_and_fetch(&destroyed_mutexes, 1);
    return res;
}

int tester_pthread_cond_init(pthread_cond_t *cond, const pthread_condattr_t *attr) {
    static int cond_counter = 0;
    if (fail_cond_at > 0) {
        int current = __sync_add_and_fetch(&cond_counter, 1);
        if (current == fail_cond_at) {
            char msg[64];
            snprintf(msg, sizeof(msg), "[INJECTOR] Blocked pthread_cond_init #%d!\n", fail_cond_at);
            write(2, msg, strlen(msg));
            return 12; // ENOMEM
        }
    }
    int res = pthread_cond_init(cond, attr);
    if (res == 0) __sync_add_and_fetch(&created_conds, 1);
    return res;
}

int tester_pthread_cond_destroy(pthread_cond_t *cond) {
    int res = pthread_cond_destroy(cond);
    if (res == 0) __sync_add_and_fetch(&destroyed_conds, 1);
    return res;
}

int tester_pthread_create(pthread_t *thread, const pthread_attr_t *attr, void *(*start_routine)(void *), void *arg) {
    static int thread_counter = 0;
    if (fail_thread_at > 0) {
        int current = __sync_add_and_fetch(&thread_counter, 1);
        if (current == fail_thread_at) {
            char msg[64];
            snprintf(msg, sizeof(msg), "[INJECTOR] Blocked pthread_create #%d!\n", fail_thread_at);
            write(2, msg, strlen(msg));
            return 11; // EAGAIN
        }
    }
    int res = pthread_create(thread, attr, start_routine, arg);
    if (res == 0) __sync_add_and_fetch(&created_threads, 1);
    return res;
}

int tester_pthread_join(pthread_t thread, void **retval) {
    int res = pthread_join(thread, retval);
    if (res == 0) __sync_add_and_fetch(&joined_threads, 1);
    return res;
}

int tester_pthread_detach(pthread_t thread) {
    int res = pthread_detach(thread);
    if (res == 0) __sync_add_and_fetch(&joined_threads, 1);
    return res;
}