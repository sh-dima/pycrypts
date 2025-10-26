from typing import TYPE_CHECKING

import pygame

from .entity import Entity
from .projectiles.projectile import Projectile
from ..collidable import Collidable

if TYPE_CHECKING:
    from .....game import PyCrypts
    from .....rooms.room import Room
    from .living.living_entity import LivingEntity


class Helmet(Entity):
    def __init__(self, user: "LivingEntity", game: "PyCrypts", room: "Room"):
        super().__init__(game, room, user.position, "helmet", 80)

        self.user = user
        self.no_clip = True
        self.block_sound = game.get_sound("shield_block")

        self.user.max_health += 20
        self.user.health += 20

    def tick(self):
        super().tick()

        if not self.user.is_valid():
            self.unload()

        self.position = self.user.position + (-8 * self.room.scale, -self.user.size * 3.0 / 5.0)

    def is_colliding(self, entity: Collidable) -> bool:
        if not isinstance(entity, Projectile):
            return False

        if isinstance(entity.shooter, type(self.user)):
            return False

        if self.position.distance_squared_to(entity.position) < ((self.size / 2 + entity.size / 2) ** 2):
            entity.unload()
            pygame.mixer.Sound.play(self.block_sound)

        return False