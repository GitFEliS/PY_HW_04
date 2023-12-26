import multiprocessing
import threading
import time


def fib(n):
    i = 0
    a = 1
    b = 1
    while i < n - 2:
        c = a + b
        a = b
        b = c
        i += 1
    return b


if __name__ == "__main__":
    n = 500000
    print(f"n = {n}")
    start = time.perf_counter()
    for _ in range(10):
        fib(n)
    end = time.perf_counter()
    print(f"sync time: {end - start:.2f} s")


    thread_pool = [threading.Thread(target=fib, args=[n, ]) for i in range(10)]

    start = time.perf_counter()

    for thread in thread_pool:
        thread.start()

    for thread in thread_pool:
        thread.join()

    end = time.perf_counter()
    print(f"threads time: {end - start:.2f} s")

    start = time.perf_counter()

    processes = [multiprocessing.Process(target=fib, args=[n, ]) for i in range(10)]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    end = time.perf_counter()
    print(f"processes time: {end - start:.2f} s")
