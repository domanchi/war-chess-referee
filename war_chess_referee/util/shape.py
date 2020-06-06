import math
import os
from collections import namedtuple
from typing import Tuple
from typing import TypeVar


RectangleType = TypeVar('Rectangle')


class Point(
    namedtuple(
        'Point',
        (
            'x',
            'y',
        ),
    ),
):
    def __new__(cls, x: float, y: float):
        # Everything is integers, because we don't need to be that precise.
        return super().__new__(cls, int(x), int(y))


class Rectangle(
    namedtuple(
        'Rectangle',
        (
            'width',
            'height',
            'x',
            'y',
        ),
    ),
):
    def __new__(
        cls,
        width: float,
        height: float,
        x: float = 0,
        y: float = 0,
    ):
        return super().__new__(
            cls,
            width=width,
            height=height,
            x=x,
            y=y,
        )

    @property
    def start_point(self) -> Point:
        return Point(self.x, self.y)

    @property
    def end_point(self) -> Point:
        return Point(self.x + self.width, self.y + self.height)

    @property
    def coordinates(self) -> Tuple[int, int, int, int]:
        return (*self.start_point, *self.end_point)

    @property
    def dimensions(self) -> Tuple[float, float]:
        return (self.width, self.height)

    def __mul__(self, other: RectangleType) -> RectangleType:
        # Used for ratio calculation.
        return Rectangle(
            self.width * other.width,
            self.height * other.height,
            self.x * other.width,
            self.y * other.height,
        )

    def __truediv__(self, other: RectangleType) -> RectangleType:
        # Used for ratio calculation.
        return Rectangle(
            self.width / other.width,
            self.height / other.height,
            self.x / other.width,
            self.y / other.height,
        )
