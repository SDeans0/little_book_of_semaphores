import threading

def threada(semA, semB, flag):
    print(f"First step for thread: {flag}")
    semA.release()
    semB.acquire()
    print(f"Second step for thread {flag}")

def threadb(semA, semB, flag):
    print(f"First step for thread {flag}")
    semB.release()
    semA.acquire()
    print(f"Second step for thread {flag}")

def main():
    semAphore = threading.Semaphore(0)
    semBphore = threading.Semaphore(0)
    print("main starts")
    a = threading.Thread(target=threada, args=(semAphore, semBphore, 1))
    b = threading.Thread(target=threadb, args=(semAphore, semBphore, 2))
    b.start()
    a.start()
    a.join()
    b.join()
    print("main finishes")

if __name__ == "__main__":
    main()