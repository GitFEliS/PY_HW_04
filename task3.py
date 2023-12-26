import codecs
import sys
import time
from multiprocessing import Pipe, Process, Queue

def a(b_conn, pipe):
    queue = Queue()
    last_sent = time.time() - 5

    while True:
        if pipe.poll():
            msg = pipe.recv()
            if msg == "  __BREAK__  ":
                b_conn.send(msg)
                break
            msg = msg.lower()
            queue.put(msg)
        if time.time() - last_sent >= 5 and not queue.empty():
            b_conn.send(queue.get())
            last_sent = time.time()


def b(a_conn, main_conn):
    while True:
        msg = a_conn.recv()
        if msg == "  __BREAK__  ":
            break
        msg = codecs.encode(msg, "rot_13")
        main_conn.send(msg)


if __name__ == "__main__":
    with open("task3.txt", "w") as f:
        time_format = "[%d.%m.%Y %H:%M:%S]"

        queue = Queue()
        main_a_conn, a_main_conn = Pipe()
        a_b_conn, b_a_conn = Pipe()
        main_b_conn, b_main_conn = Pipe()
        p_a = Process(target=a, args=(a_b_conn, a_main_conn))
        p_b = Process(target=b, args=(b_a_conn, b_main_conn))
        p_a.start()
        p_b.start()

        while True:
            user_input = sys.stdin.readline()
            if not user_input.strip():
                break
            current_time = time.strftime(time_format, time.localtime())
            main_a_conn.send(user_input.strip())
            f.write(f"{current_time} [User] {user_input.strip()}\n")

            if (main_b_conn.poll()):
                new_msg = main_b_conn.recv()
                current_time = time.strftime(time_format, time.localtime())
                f.write(f"{current_time} [Program] {new_msg}\n")
                print(f"GET: {new_msg}")
        main_a_conn.send("  __BREAK__  ")
        p_a.join()
        p_b.join()
