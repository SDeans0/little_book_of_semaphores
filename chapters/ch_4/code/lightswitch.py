import threading

class Lightswitch:
    def __init__(self, sem: threading.Semaphore):
        self.count = 0
        self.mutex = threading.Semaphore(1)
        self.sem = sem
    
    def lock(self):
        self.mutex.acquire()
        self.count += 1
        if self.count == 1:
            self.sem.acquire()
        self.mutex.release()
    
    def unlock(self):
        self.mutex.acquire()
        self.count -= 1
        if self.count == 0:
            self.sem.release()
        self.mutex.release()