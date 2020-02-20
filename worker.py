import queue
import ffmpegWrapper
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

def init():
    global statusQueue
    statusQueue = {}

workerQ = queue.Queue()

def workerDispatcher():
    """
    Generates Queue that handles creation and deletion 
    of work based on CPU core count.
    """
    with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        while True:
            hash, handle = workerQ.get()
            executor.submit(ffmpegWrapper.create_video, hash, handle)