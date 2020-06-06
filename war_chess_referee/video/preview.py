from contextlib import contextmanager

import cv2
import numpy as np


@contextmanager
def visible_window(window_name: str = 'preview'):
    cv2.namedWindow(window_name)
    cv2.moveWindow(window_name, 0, 0)

    try:
        yield WindowManager(window_name)
    finally:
        cv2.destroyWindow(window_name)


class WindowManager:
    def __init__(self, window_name: str):
        self.window_name = window_name

    def show(self, frame: np.ndarray):
        cv2.imshow(self.window_name, frame)
