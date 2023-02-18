"""Rendevous for n threads"""
import threading


class ReusableBarrier:
    def __init__(self, n_threads: int) -> None:
        self.count = 0
        self.n_threads = n_threads
        self.mutex = threading.Semaphore(1)
        self.current_semaphore = threading.Semaphore(0)
        self.next_semaphore = threading.Semaphore(1)
    
    def reached(self) -> bool:
        return self.count == self.n_threads

    def inc(self):
        self.mutex.acquire()
        self.count += 1
        self.mutex.release()
    
    def dec(self):
        self.mutex.acquire()
        self.count -= 1
        self.mutex.release()
    
    def reset(self):
        self.mutex.acquire()
        self.count = 0
        self.mutex.release()


def wait_for_critical(rv: ReusableBarrier, thread_id: int):
    print(f"Started {thread_id}")
    for i in range(3):
        rv.inc()
        if rv.reached():
            rv.next_semaphore.acquire()
            rv.current_semaphore.release()
        rv.current_semaphore.acquire()
        print(f"Critical_section {i}: {thread_id}")
        rv.dec()
        rv.current_semaphore.release()
        if rv.count == 0:
            rv.current_semaphore.acquire()
            rv.next_semaphore.release()
        rv.next_semaphore.acquire()
        rv.next_semaphore.release()


def main(n_threads = 4000):
    rv = ReusableBarrier(n_threads)
    threads = []
    for i in range(n_threads):
        new_thread = threading.Thread(target=wait_for_critical, args=(rv, i))
        new_thread.start()
        threads.append(new_thread)
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()