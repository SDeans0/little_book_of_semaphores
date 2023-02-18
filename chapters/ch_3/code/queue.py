import threading
from abc import ABC
from time import sleep

class Queue(ABC):
    def __init__(self):
        self.count = 0
        self.mutex = threading.Semaphore(1)
        self.semaphore = threading.Semaphore(0)

    def inc(self):
        self.mutex.acquire()
        self.count += 1
        self.mutex.release()

    def dec(self):
        self.mutex.acquire()
        self.count -= 1
        self.mutex.release()
    
    @property
    def empty(self):
        return self.count <= 0
    
    def push(self, lq):
        if lq.empty:
            self.inc()
            print("waiting")
            self.semaphore.acquire()
        else:
            lq.pop()
        self.act()
        
    def pop(self):
        self.dec()
        self.semaphore.release()

    def act(self):
        raise NotImplementedError
    

class FollowerQueue(Queue):
    def act(self):
        print("Follower Action")


class LeaderQueue(Queue):
    def act(self):
        print("Leader Action")

def pq(q1, q2):
    q1.push(q2)

def main(n_threads=20):
    lq = LeaderQueue()
    fq = FollowerQueue()

    threads = []
    for i in range(n_threads//2):
        new_thread = threading.Thread(target=pq, args=(lq, fq))
        new_thread.start()
        threads.append(new_thread)
    
    for i in range(n_threads//2):
        sleep(1)
        new_thread = threading.Thread(target=pq, args=(fq, lq))
        new_thread.start()
        threads.append(new_thread)
    
    for thread in threads:
        thread.join()

if __name__=="__main__":
    main()