from typing import TYPE_CHECKING

from pygame import Vector2

from pycrypts.rooms.room import Room
from pycrypts.tickable.renderable.collidable.entities.entity import Entity

if TYPE_CHECKING:
    from pycrypts.game import PyCrypts


class Candle(Entity):

    def __init__(self, game: "PyCrypts", room: "Room", position: tuple[int, int] | Vector2, light_radius: int = 1200, size: int = 64):
        super().__init__(game, room, position, "lantern", size)

        self.light_radius = light_radius
        self.no_clip = True

    def tick(self):
        self.render()
        self.render_light(self.light_radius)
