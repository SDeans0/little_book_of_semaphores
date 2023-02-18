import random
import threading 
import time
from collections import deque


class Producer:
    def __init__(self, sem: threading.Semaphore, mutex: threading.Semaphore, buffer: deque):
        self.buffer = buffer
        self.mutex = mutex
        self.sem = sem

    def add(self):
        self.mutex.acquire()
        e = random.randint(0,100)
        self.buffer.append(e)
        self.mutex.release()
        self.sem.release()

class Consumer:
    def __init__(self, sem: threading.Semaphore, mutex: threading.Semaphore, buffer: deque):
        self.buffer = buffer
        self.mutex = mutex
        self.sem = sem
    
    def process(self):
        self.sem.acquire()
        self.mutex.acquire()
        e = self.buffer.popleft()
        print(f"Consuming {e}")
        self.mutex.release()

def main(n_threads = 10):
    sem = threading.Semaphore(0)
    mutex = threading.Semaphore(1)
    buffer = deque()
    producer = Producer(sem, mutex, buffer)
    consumer = Consumer(sem, mutex, buffer)

    threads = []
    for i in range(n_threads//2):
        new_thread = threading.Thread(target=consumer.process)
        new_thread.start()
        threads.append(new_thread)

    for i in range(n_threads//2):
        time.sleep(1)
        new_thread = threading.Thread(target=producer.add)
        new_thread.start()
        threads.append(new_thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
