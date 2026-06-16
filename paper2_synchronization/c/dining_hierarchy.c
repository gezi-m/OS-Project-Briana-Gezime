/*
 * dining_hierarchy.c -- Dining Philosophers, resource hierarchy solution
 * Compile: gcc -O2 -Wall -o dining_hierarchy dining_hierarchy.c -lpthread
 * Usage:   ./dining_hierarchy --philosophers <N> --duration <sec>
 */
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sys/resource.h>
#include <time.h>
#include <string.h>
#include <unistd.h>

static int N = 5;
static pthread_mutex_t *forks;
static volatile int running = 1;
static long *meal_counts;

static void *philosopher(void *arg) {
    int id = *(int *)arg;
    int left = id, right = (id + 1) % N;
    pthread_mutex_t *first  = (left < right) ? &forks[left]  : &forks[right];
    pthread_mutex_t *second = (left < right) ? &forks[right] : &forks[left];
    long local = 0;
    while (running) {
        pthread_mutex_lock(first);
        pthread_mutex_lock(second);
        local++;   /* eat */
        pthread_mutex_unlock(second);
        pthread_mutex_unlock(first);
    }
    meal_counts[id] = local;
    return NULL;
}

int main(int argc, char **argv) {
    int duration = 3;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--philosophers")) N        = atoi(argv[++i]);
        if (!strcmp(argv[i], "--duration"))     duration = atoi(argv[++i]);
    }
    forks       = malloc(N * sizeof(pthread_mutex_t));
    meal_counts = calloc(N, sizeof(long));
    int *ids    = malloc(N * sizeof(int));
    for (int i = 0; i < N; i++) pthread_mutex_init(&forks[i], NULL);

    pthread_t *threads = malloc(N * sizeof(pthread_t));
    struct timespec t_start, t_end;
    clock_gettime(CLOCK_MONOTONIC, &t_start);

    for (int i = 0; i < N; i++) { ids[i] = i; pthread_create(&threads[i], NULL, philosopher, &ids[i]); }
    sleep(duration);
    running = 0;
    for (int i = 0; i < N; i++) pthread_join(threads[i], NULL);
    clock_gettime(CLOCK_MONOTONIC, &t_end);

    double elapsed = (t_end.tv_sec - t_start.tv_sec) + (t_end.tv_nsec - t_start.tv_nsec) / 1e9;
    long total = 0;
    for (int i = 0; i < N; i++) total += meal_counts[i];
    printf("N=%d elapsed=%.3f total_meals=%ld throughput=%.0f\n", N, elapsed, total, total/elapsed);

    free(forks); free(meal_counts); free(ids); free(threads);
    return 0;
}
