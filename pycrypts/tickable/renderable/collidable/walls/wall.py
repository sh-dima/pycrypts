from typing import TYPE_CHECKING, Sequence

import pygame
from pygame import Vector2, Rect, Color

from ..collidable import Collidable
from ..entities.entity import Entity
from ....tickable import Tickable

if TYPE_CHECKING:
    from .....game import PyCrypts
    from .....rooms.room import Room


class Wall(Collidable):
    points: list[  # list of
        tuple[  # pair of
            tuple[int, int],  # top left 
            tuple[int, int]  # bottom right
        ]
    ] = []

    def __init__(self, top_left: tuple[int, int], bottom_right: tuple[int, int], game: "PyCrypts", room: "Room", border = False, color: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | Sequence[int] = (65, 65, 65)):
        self.top_left = Vector2(top_left)
        self.bottom_right = Vector2(bottom_right)

        super().__init__(game, room)

        self.game = game
        self.color = color
        self.very_clip = border

    def get_center(self):
        return (self.top_left + self.bottom_right) / 2.0

    def get_width(self):
        return self.bottom_right.x - self.top_left.x

    def get_height(self):
        return self.bottom_right.y - self.top_left.y

    def get_top_right(self):
        return Vector2(self.bottom_right.x, self.top_left.y)

    def get_bottom_left(self):
        return Vector2(self.top_left.x, self.bottom_right.y)

    def get_lines(self):
        return [
            (self.top_left, self.get_top_right()),
            (self.top_left, self.get_bottom_left()),
            (self.get_top_right(), self.bottom_right),
            (self.get_bottom_left(), self.bottom_right)
        ]

    def tick(self):
        self.render()

    def render(self):
        width = self.bottom_right.x - self.top_left.x
        height = self.bottom_right.y - self.top_left.y

        pygame.draw.rect(self.game.screen, self.color, Rect(self.top_left, (width, height)))

    def is_colliding(self, other: Collidable) -> bool:
        if isinstance(other, Entity):
            if other.no_clip and not (self.very_clip or other.very_clip):
                return False

            points = other.get_points()

            for point in points:
                if self.contains_point(point):
                    return True
        return False

    def contains_point(self, point: Vector2 | tuple[int, int]) -> bool:
        point = Vector2(point)

        return self.top_left.x <= point.x <= self.bottom_right.x and self.top_left.y <= point.y <= self.bottom_right.y

    def __str__(self):
        return f'{super().__str__()} defined by ({self.top_left}, {self.bottom_right})'
