import random
import threading
import time

class ReadWrite:
    def __init__(self):
        self.count = 0
        self.mutex = threading.Semaphore(1)
        self.critical = threading.Semaphore(1)
        self.new_read = threading.Semaphore(1)
    
    def inc(self):
        self.mutex.acquire()
        self.count += 1
        self.mutex.release()
    
    def dec(self):
        self.mutex.acquire()
        self.count -= 1
        self.mutex.release()
    
    @property
    def room_empty(self):
        return self.count == 0

def read(sem: ReadWrite, thread_id: int):
    if sem.room_empty:
        sem.new_read.acquire()
        sem.critical.acquire()
        sem.new_read.release()
    
    sem.inc()
    
    print(f"Reading on thread {thread_id}")

    sem.dec()

    if sem.room_empty:
        sem.critical.release()

def write(sem: ReadWrite, thread_id: int):
    sem.new_read.acquire()
    sem.critical.acquire()
    print(f"Writing on thread {thread_id}")
    print(f"There are {sem.count} readers during the write section")
    sem.critical.release()
    sem.new_read.release()
    

def main(n_threads = 100):
    rw_lock = ReadWrite()

    threads = []
    for i in range(n_threads//2):
        new_thread = threading.Thread(target=read, args=(rw_lock,i,))
        threads.append(new_thread)

    for i in range(n_threads//2):
        new_thread = threading.Thread(target=write, args=(rw_lock,i,))
        threads.append(new_thread)
    
    random.shuffle(threads)

    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
