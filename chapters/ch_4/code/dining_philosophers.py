import threading
import time
import random

class Philosopher:
    def __init__(self,id_: int, mutex: threading.Semaphore, left_fork: threading.Semaphore, right_fork: threading.Semaphore):
        self.mutex = mutex
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.hungry: bool = False
        self.id = id_
    
    def __repr__(self):
        return f"Philosopher {self.id}"

    def philosophise(self):
        print(f"{self} is thinking...")
        think_time = random.randint(1,5)
        time.sleep(think_time/10)
        print(f"{self} is hungry")
        self.hungry = True
    
    def eat(self):
        self.mutex.acquire()
        l = self.left_fork.acquire(blocking=False)
        r = self.right_fork.acquire(blocking=False)
        if l and r:
            self.mutex.release()
            print(f"{self} is eating")
            eat_time = random.randint(1,2)
            time.sleep(eat_time/10)
            self.hungry = False
            self.left_fork.release()
            self.right_fork.release()
            print(f"{self} is done eating")
        else:
            if l:
                self.left_fork.release()
            if r:
                self.right_fork.release()
            self.mutex.release()
    
    def run(self):
        while True:
            if self.hungry:
                self.eat()
            else:
                self.philosophise()

def main(n_diners = 5):
    mutex = threading.Semaphore(1)
    forks = [threading.Semaphore(1) for _ in range(n_diners)]
    diners = []
    for i in range(n_diners):
        philosopher = Philosopher(i, mutex=mutex, left_fork=forks[i], right_fork=forks[(i+1) % n_diners])
        diners.append(threading.Thread(target=philosopher.run))
    
    for d in diners:
        d.start()

if __name__ == "__main__":
    main()
    

