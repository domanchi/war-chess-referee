import threading
import time
from typing import Callable


def delay(callback: Callable, delay: int):
    def worker():
        threading.Event().wait(delay)
        callback()
    
    threading.Thread(target=worker, daemon=True).start()