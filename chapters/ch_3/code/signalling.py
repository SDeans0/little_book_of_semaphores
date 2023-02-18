import threading
import time

def threada(sem, flag):
    print(f"Thread running: {flag}")
    time.sleep(0.5)
    sem.release()

def threadb(sem, flag):
    sem.acquire()
    print(f"Thread running: {flag}")

def main():
    semaphore = threading.Semaphore(0)
    print("main starts")
    a = threading.Thread(target=threada, args=(semaphore, 1))
    b = threading.Thread(target=threadb, args=(semaphore, 2))
    b.start()
    a.start()
    a.join()
    b.join()
    print("main finishes")

if __name__ == "__main__":
    main()