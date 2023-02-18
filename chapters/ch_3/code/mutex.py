import threading

class Counter:
    def __init__(self) -> None:
        self.count = 0
    
    def increment_unsafe(self):
        self.count += 1
    
    def increment_safe(self, semaphore: threading.Semaphore):
        semaphore.acquire()
        self.increment_unsafe()
        semaphore.release()
    
    def __repr__(self) -> str:
        return f"Count: {self.count}"

def main(n_threads: int = 2) -> int:
    count = Counter()
    mutex = threading.Semaphore(1)
    inc = lambda: count.increment_safe(mutex)
    threads = []
    for _ in range(n_threads):
        new_thread = threading.Thread(target=inc)
        new_thread.start()
        threads.append(new_thread)
    
    for thread  in threads:
        thread.join()
    
    print(count)
    return count.count

if __name__ == "__main__":
    main()