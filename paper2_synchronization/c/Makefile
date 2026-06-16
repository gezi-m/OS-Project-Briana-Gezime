CC     = gcc
CFLAGS = -O2 -Wall -Wextra
LIBS   = -lpthread -lrt

all: producer_consumer dining_hierarchy

producer_consumer: producer_consumer.c
	$(CC) $(CFLAGS) -o $@ $< $(LIBS)

dining_hierarchy: dining_hierarchy.c
	$(CC) $(CFLAGS) -o $@ $< $(LIBS)

clean:
	rm -f producer_consumer dining_hierarchy
