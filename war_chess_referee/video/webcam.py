from contextlib import contextmanager

from imutils.video import VideoStream


@contextmanager
def start():
    vs = VideoStream(src=0).start()

    try:
        yield vs
    finally:
        vs.stop()
