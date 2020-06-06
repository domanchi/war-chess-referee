"""The game engine."""
from typing import Optional

import cv2
import numpy as np
from PIL import Image

from .logic.game import GameState
from .ocr.predictor import CRNNPredictor
from .util.shape import Point
from .util.shape import Rectangle
from .video import webcam
from .video.draw import Drawing
from .video.preview import visible_window


class GameEngine:
    def __init__(self, width: int, height: int):
        """
        :param width: specifies the width for the target area for capturing the image.
            Adjust accordingly (larger means the piece has to be closer to the camera).
        :param height: see width
        """
        self.predictor = CRNNPredictor()
        self.game = GameState()
        
        self.width = width
        self.height = height

        # This is initialized upon run since we need the size of the window first.
        self.focal_area = None
        self.renderer = None

    def run(self):
        with webcam.start() as vs, visible_window() as window:
            frame = vs.read()
            while frame is not None:
                try:
                    self._process_frame(frame)
                except StopIteration:
                    break

                window.show(frame)
                frame = vs.read()
    
    def _process_frame(self, frame: np.ndarray):
        if not self.focal_area:
            height, width = frame.shape[:2]
            center_point = Point(width / 2, height / 2)
            self.focal_area = Rectangle(
                self.width,
                self.height,
                center_point.x - self.width / 2,
                center_point.y - self.height / 2,
            )
            self.renderer = Drawing(self.focal_area)

        self.renderer.render(frame)

        self._process_key_input(cv2.waitKey(20), frame)
    
    def _process_key_input(self, key: Optional[int], frame: np.ndarray):
        if key == 27:
            raise StopIteration

        elif key == ord(' '):
            captured_area = frame[
                self.focal_area.start_point.y:self.focal_area.end_point.y,
                self.focal_area.start_point.x:self.focal_area.end_point.x,
            ]

            piece = self.predictor.predict(Image.fromarray(captured_area))
            result = self.game.process(piece)

            self.renderer.process_result(result)
