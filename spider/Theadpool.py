import threading
from concurrent.futures import ThreadPoolExecutor
import time

def sing(i,b):
    print("正在唱歌...%d"%i)
    print("正在唱歌...%d"%b)





if __name__ == "__main__":

    threadPool = ThreadPoolExecutor(max_workers=20, thread_name_prefix="claw")
    for i in range(0, 20):
        future = threadPool.submit(sing(i*12931,(i + 1)*12931))
    threadPool.shutdown(wait=True)
