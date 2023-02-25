import random
import threading
import time
from lightswitch import Lightswitch

def read(switch: Lightswitch, turnstile:threading.Semaphore, thread_id: int):
    turnstile.acquire()
    turnstile.release()
    switch.lock()
    
    print(f"Reading on thread {thread_id}")

    switch.unlock()

def write(sem: threading.Semaphore, turnstile:threading.Semaphore, switch: Lightswitch, thread_id: int,):
    turnstile.acquire()
    sem.acquire()
    print(f"Writing on thread {thread_id}")
    print(f"there are {switch.count} readers reading during writing")
    turnstile.release()
    sem.release()
    

def main(n_threads = 100):
    allow_write = threading.Semaphore(1)
    turnstile = threading.Semaphore(1)
    readSwitch = Lightswitch(allow_write)

    threads = []
    for i in range(n_threads//2):
        new_thread = threading.Thread(target=read, args=(readSwitch,turnstile,i,))
        threads.append(new_thread)

    for i in range(n_threads//2):
        new_thread = threading.Thread(target=write, args=(allow_write,turnstile,readSwitch,i,))
        threads.append(new_thread)
    
    random.shuffle(threads)

    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
