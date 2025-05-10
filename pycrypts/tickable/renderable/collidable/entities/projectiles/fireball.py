import random
from typing import TYPE_CHECKING

from pygame import Vector2

from .projectile import Projectile
from ..entity import Entity
from ..living.living_entity import LivingEntity
from ...collidable import Collidable

if TYPE_CHECKING:
    from ......game import PyCrypts
    from ......rooms.room import Room


class Fireball(Projectile):

    def __init__(self, game: "PyCrypts", room: "Room", shooter: Entity, position: tuple[int, int] | Vector2, direction: Vector2, strength: float = -1, speed: float = 1, size: int = 32):
        super().__init__(game, room, shooter, position, "fireball", direction, strength, speed, size)
        self.light_radius = 100

    def render(self):
        super().render()
        self.render_light(self.light_radius)

    def on_hit(self, collidable: Collidable):
        super().on_hit(collidable)

        if isinstance(collidable, LivingEntity):
            collidable.damage(10)
            return False
