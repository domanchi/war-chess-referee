from enum import Enum

import cv2
import numpy as np

from ..logic.enum import ResultType
from ..util.delay import delay
from ..util.shape import Rectangle


class Drawing:
    def __init__(self, focal_area: Rectangle):
        self.focal_frame = focal_area
        self.focal_frame_color = Color.GRAY

        self.status = 'Waiting for Attacker'

    def render(self, frame: np.ndarray):
        # Drawing the focal frame.
        cv2.rectangle(
            frame,
            tuple(self.focal_frame.start_point),
            tuple(self.focal_frame.end_point),
            color=self.focal_frame_color.value,
            thickness=2,
        )

        if self.status:
            cv2.putText(
                frame,
                f'Status: {self.status}',
                (20, 50),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1,
                color=Color.WHITE.value,
                thickness=2,
                bottomLeftOrigin=False,
            )

        if self.focal_frame_color == Color.GREEN:
            cv2.putText(
                frame,
                'Captured!',
                (
                    int(
                        (self.focal_frame.end_point.x -
                         self.focal_frame.start_point.x) / 2
                        + self.focal_frame.start_point.x
                        - 80,
                    ),
                    self.focal_frame.end_point.y - 20,
                ),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1,
                color=Color.GREEN.value,
                thickness=2,
                bottomLeftOrigin=False,
            )

    def process_result(self, result: ResultType):
        def revert_focal_frame_color():
            self.focal_frame_color = Color.GRAY

        delay(revert_focal_frame_color, 1)

        if result == ResultType.ERROR:
            self.focal_frame_color = Color.RED
            return
        else:
            self.focal_frame_color = Color.GREEN

        self.status = {
            ResultType.VICTORY: 'Victory!',
            ResultType.BOTH_LOSE: 'Both players lose!',
            ResultType.ATTACKER_LOSE: 'Defender wins!',
            ResultType.DEFENDER_LOSE: 'Attacker wins!',
            ResultType.PENDING: 'Waiting for Defender',
        }.get(result)

        def revert_status():
            self.status = 'Waiting for Attacker'

        if result != ResultType.PENDING:
            delay(revert_status, 3)


class Color(Enum):
    # Remember that OpenCV defaults to BGR (instead of RGB).
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)
    GRAY = (120, 120, 120)
    WHITE = (255, 255, 255)
