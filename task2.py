import concurrent.futures
import logging
import math
import multiprocessing
import time

logging.basicConfig(
    filename="integrate.log",
    level=logging.INFO,
    format="%(asctime)s\t%(levelname)s\t%(message)s",
    datefmt="%d.%m.%Y %H:%M:%S",
)


def integral(f, a, b, step):
    acc = 0
    i = 0
    while (a + i * step < b):
        acc += f(a + i * step) * step
        i += 1
    return acc


def integrate(f, a, b, *, n_jobs=1, n_iter=1000, executor=concurrent.futures.ProcessPoolExecutor()):
    logging.info(f"Integration started with {n_jobs} workers")

    acc = 0
    step = (b - a) / n_iter
    segment = (b-a) // n_jobs
    segments = []

    for i in range(n_jobs):
        int_start = i*segment
        int_end = min((i+1) * segment, b)
        segments.append((int_start, int_end))

    futures = [executor.submit(integral, f, int_start, int_end, step)
               for int_start, int_end in segments]
    for future in concurrent.futures.as_completed(futures):
        acc += future.result()

    logging.info(f"Integration complete")

    return acc


if __name__ == "__main__":
    cpu_num = multiprocessing.cpu_count()

    print("ThreadPoolExecutor results:")
    for i in range(1, cpu_num+1):
        start = time.perf_counter()
        integrate(math.cos, 0, math.pi/2, n_jobs=i,
                  executor=concurrent.futures.ThreadPoolExecutor())
        end = time.perf_counter()
        print(f"ThreadPool jobs:{i} time:{end-start:.2f}")

    print()
    print()

    print("ThreadPoolExecutor results:")
    for i in range(1, cpu_num+1):
        start = time.perf_counter()
        integrate(math.cos, 0, math.pi/2, n_jobs=i,
                  executor=concurrent.futures.ProcessPoolExecutor())
        end = time.perf_counter()
        print(f"ProcessPool jobs:{i} time:{end-start:.2f}")


