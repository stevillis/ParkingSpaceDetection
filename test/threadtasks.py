import threading
import time


def time_parking_change(t):
    print('{} starting...'.format(threading.currentThread().getName()))
    # Thread is stopped for t seconds
    time.sleep(t)
    print('{} exiting...'.format(threading.currentThread().getName()))


def start_thread(t):
    w = threading.Thread(name='Thread 2', target=time_parking_change, args=(1,))
    w.start()
