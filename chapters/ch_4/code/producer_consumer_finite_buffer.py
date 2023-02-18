import random
import threading 
import time
from collections import deque

MAX_BUFFER_SIZE = 2

class Producer:
    def __init__(self, sem: threading.Semaphore, mutex: threading.Semaphore,buffer_sem: threading.Semaphore, buffer: deque):
        self.buffer = buffer
        self.mutex = mutex
        self.sem = sem
        self.buffer_sem = buffer_sem

    def add(self):
        self.buffer_sem.acquire()
        self.mutex.acquire()
        e = random.randint(0,100)
        self.buffer.append(e)
        print(f"adding {e}")
        self.mutex.release()
        self.sem.release()

class Consumer:
    def __init__(self, sem: threading.Semaphore, mutex: threading.Semaphore,buffer_sem: threading.Semaphore, buffer: deque):
        self.buffer = buffer
        self.mutex = mutex
        self.sem = sem
        self.buffer_sem = buffer_sem
    
    def process(self):
        self.sem.acquire()
        self.mutex.acquire()
        print(f"Buffer is length {len(self.buffer)}")
        e = self.buffer.popleft()
        print(f"Consuming {e}")
        self.mutex.release()
        self.buffer_sem.release()

def main(n_threads = 10):
    consumer_sem = threading.Semaphore(0)
    mutex = threading.Semaphore(1)
    buffer_sem = threading.Semaphore(MAX_BUFFER_SIZE)
    buffer = deque()
    producer = Producer(consumer_sem, mutex,buffer_sem, buffer)
    consumer = Consumer(consumer_sem, mutex,buffer_sem, buffer)

    threads = []
    for i in range(n_threads//2):
        new_thread = threading.Thread(target=consumer.process)
        new_thread.start()
        threads.append(new_thread)

    for i in range(n_threads//2):
        new_thread = threading.Thread(target=producer.add)
        new_thread.start()
        threads.append(new_thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
