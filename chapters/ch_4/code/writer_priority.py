import random
import threading
import time
from lightswitch import Lightswitch

def read(switch: Lightswitch, allow_read:threading.Semaphore,write_switch: Lightswitch, thread_id: int):
    print(f"read thread started: {thread_id}")
    allow_read.acquire()

    switch.lock()
    
    print(f"Reading on thread {thread_id}")

    switch.unlock()
    allow_read.release()

def write(sem: threading.Semaphore, write_switch: Lightswitch, read_switch: Lightswitch, thread_id: int,):
    print(f"write thread started: {thread_id}")
    write_switch.lock()
    sem.acquire()
    print(f"Writing on thread {thread_id}")
    print(f"there are {read_switch.count} readers reading during writing")
    write_switch.unlock()
    sem.release()
    

def main(n_threads = 100):
    allow_write = threading.Semaphore(1)
    allow_read = threading.Semaphore(1)
    readSwitch = Lightswitch(allow_write)
    writeSwitch = Lightswitch(allow_read)

    threads = []
    for i in range(n_threads//2):
        new_thread = threading.Thread(target=read, args=(readSwitch,allow_read, writeSwitch,i,))
        threads.append(new_thread)

    for i in range(n_threads//2):
        new_thread = threading.Thread(target=write, args=(allow_write, writeSwitch, readSwitch,i,))
        threads.append(new_thread)
    
    random.shuffle(threads)

    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
