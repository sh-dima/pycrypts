from typing import TYPE_CHECKING

from pygame import Vector2

from ..entity import Entity
from ..living.living_entity import LivingEntity
from .projectile import Projectile
from ...collidable import Collidable
from ......rooms.room import Room

if TYPE_CHECKING:
    from pycrypts.game import PyCrypts


class BozosBall(Projectile):
    def __init__(self, game: "PyCrypts", room: "Room", shooter: Entity, position: tuple[int, int] | Vector2, direction: Vector2 | tuple[int, int], color: str = "red", strength: float = 3, speed = 1, size: int = 48):
        super().__init__(game, room, shooter, position, f"balls/{color}", direction, strength, speed, size)

    def tick(self):
        super().tick()

        self.speed += 2.5 * self.game.dt

    def is_colliding(self, entity: Collidable) -> bool:
        from ..living.monsters.bozo import Bozo
        if isinstance(entity, Bozo) or isinstance(entity, BozosBall):
            return False

        return super().is_colliding(entity)

    def on_hit(self, entity: Collidable):
        super().on_hit(entity)

        from ..living.monsters.bozo import Bozo
        if isinstance(entity, LivingEntity) and not isinstance(entity, Bozo):
            entity.damage(5 * self.speed)
