/*
 * producer_consumer.c -- POSIX pthreads bounded-buffer Producer-Consumer
 * Compile: gcc -O2 -Wall -o producer_consumer producer_consumer.c -lpthread -lrt
 * Usage:   ./producer_consumer --buf <N> --producers <M> --consumers <K> --duration <sec>
 *
 * Paper 2: Comparative Performance Evaluation of Multithreaded Synchronization
 */
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <sys/resource.h>
#include <time.h>
#include <string.h>

typedef long buffer_item;

static buffer_item  *buffer;
static int           buf_size, buf_in = 0, buf_out = 0;
static pthread_mutex_t mutex;
static sem_t           sem_empty, sem_full;
static volatile int    running = 1;
static long           *produced_count, *consumed_count;
static int             num_producers, num_consumers;

static void *producer(void *arg) {
    int id = *(int *)arg;
    buffer_item item = 0;
    while (running) {
        item++;
        sem_wait(&sem_empty);
        pthread_mutex_lock(&mutex);
        buffer[buf_in] = item;
        buf_in = (buf_in + 1) % buf_size;
        produced_count[id]++;
        pthread_mutex_unlock(&mutex);
        sem_post(&sem_full);
    }
    return NULL;
}

static void *consumer(void *arg) {
    int id = *(int *)arg;
    buffer_item item;
    while (running) {
        sem_wait(&sem_full);
        pthread_mutex_lock(&mutex);
        item = buffer[buf_out];
        buf_out = (buf_out + 1) % buf_size;
        consumed_count[id]++;
        pthread_mutex_unlock(&mutex);
        sem_post(&sem_empty);
        (void)item;
    }
    return NULL;
}

int main(int argc, char **argv) {
    buf_size = 10; num_producers = 2; num_consumers = 2;
    int duration = 2;

    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--buf"))       buf_size      = atoi(argv[++i]);
        if (!strcmp(argv[i], "--producers")) num_producers = atoi(argv[++i]);
        if (!strcmp(argv[i], "--consumers")) num_consumers = atoi(argv[++i]);
        if (!strcmp(argv[i], "--duration"))  duration      = atoi(argv[++i]);
    }

    buffer         = calloc(buf_size, sizeof(buffer_item));
    produced_count = calloc(num_producers, sizeof(long));
    consumed_count = calloc(num_consumers, sizeof(long));

    pthread_mutex_init(&mutex, NULL);
    sem_init(&sem_empty, 0, buf_size);
    sem_init(&sem_full,  0, 0);

    pthread_t *prod_threads = malloc(num_producers * sizeof(pthread_t));
    pthread_t *cons_threads = malloc(num_consumers * sizeof(pthread_t));
    int *prod_ids = malloc(num_producers * sizeof(int));
    int *cons_ids = malloc(num_consumers * sizeof(int));

    struct timespec t_start, t_end;
    clock_gettime(CLOCK_MONOTONIC, &t_start);
    struct rusage ru_start;
    getrusage(RUSAGE_SELF, &ru_start);

    for (int i = 0; i < num_producers; i++) { prod_ids[i] = i; pthread_create(&prod_threads[i], NULL, producer, &prod_ids[i]); }
    for (int i = 0; i < num_consumers; i++) { cons_ids[i] = i; pthread_create(&cons_threads[i], NULL, consumer, &cons_ids[i]); }

    sleep(duration);
    running = 0;
    /* Unblock all blocked threads */
    for (int i = 0; i < num_producers; i++) sem_post(&sem_empty);
    for (int i = 0; i < num_consumers; i++) sem_post(&sem_full);

    for (int i = 0; i < num_producers; i++) pthread_join(prod_threads[i], NULL);
    for (int i = 0; i < num_consumers; i++) pthread_join(cons_threads[i], NULL);

    clock_gettime(CLOCK_MONOTONIC, &t_end);
    struct rusage ru_end;
    getrusage(RUSAGE_SELF, &ru_end);

    double elapsed = (t_end.tv_sec - t_start.tv_sec) + (t_end.tv_nsec - t_start.tv_nsec) / 1e9;
    long total_produced = 0;
    for (int i = 0; i < num_producers; i++) total_produced += produced_count[i];

    double cpu_user = (ru_end.ru_utime.tv_sec - ru_start.ru_utime.tv_sec)
                    + (ru_end.ru_utime.tv_usec - ru_start.ru_utime.tv_usec) / 1e6;
    double cpu_sys  = (ru_end.ru_stime.tv_sec - ru_start.ru_stime.tv_sec)
                    + (ru_end.ru_stime.tv_usec - ru_start.ru_stime.tv_usec) / 1e6;

    printf("N=%d M=%d K=%d elapsed=%.3f produced=%ld throughput=%.0f cpu_user=%.3f cpu_sys=%.3f nvcsw=%ld nivcsw=%ld rss=%ld\n",
           buf_size, num_producers, num_consumers, elapsed, total_produced,
           total_produced / elapsed, cpu_user, cpu_sys,
           ru_end.ru_nvcsw - ru_start.ru_nvcsw,
           ru_end.ru_nivcsw - ru_start.ru_nivcsw,
           ru_end.ru_maxrss);

    free(buffer); free(produced_count); free(consumed_count);
    free(prod_threads); free(cons_threads); free(prod_ids); free(cons_ids);
    return 0;
}
