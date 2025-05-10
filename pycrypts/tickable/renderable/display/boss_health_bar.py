from typing import TYPE_CHECKING

from pygame import Vector2

from ..collidable.entities.living.living_entity import LivingEntity
from .health_bar import HealthBar

if TYPE_CHECKING:
    from pycrypts.game import PyCrypts

class BossHealthBar(HealthBar):

    def __init__(self, game: "PyCrypts", entity: LivingEntity, top_left: (int, int) or Vector2, width: int, height: int):
        super().__init__(game, entity, top_left, width, height, 2, False)

        self.unload()

    def tick(self):
        self.top_left = Vector2(self.entity.position.x - 5, self.entity.position.y - 10)

        super().tick()
