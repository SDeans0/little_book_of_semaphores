"""Rendevous for n threads"""
import threading

class Rendezvous:
    def __init__(self, n_threads: int) -> None:
        self.count = 0
        self.n_threads = n_threads
    
    def reached(self) -> bool:
        return self.count == self.n_threads
    
    def inc(self):
        self.count += 1
    
    def dec(self):
        self.count -= 1

def wait_for_critical(sem: threading.Semaphore, rv: Rendezvous, thread_id: int):
    print(f"Started {thread_id}")
    rv.inc()
    if rv.reached():
        sem.release()
    sem.acquire()
    print(f"Critical_section {thread_id}")
    sem.release()


def main(n_threads = 10):
    sem = threading.Semaphore(0)
    rv = Rendezvous(n_threads)
    threads = []
    for i in range(n_threads):
        new_thread = threading.Thread(target=wait_for_critical, args=(sem, rv, i))
        new_thread.start()
        threads.append(new_thread)
    
    for thread  in threads:
        thread.join()

if __name__ == "__main__":
    main()