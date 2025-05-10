import math
from typing import TYPE_CHECKING

import pygame
from pygame import Vector2

from .projectiles.fireball import Fireball
from .projectiles.projectile import Projectile
from .entity import Entity
from .living.living_entity import LivingEntity
from ..collidable import Collidable

if TYPE_CHECKING:
    from .....game import PyCrypts
    from .living.players.player import Player
    from .....rooms.room import Room


class Sword(Entity):

    def __init__(self, target: "Entity", user: "Player", position: tuple[int, int] | Vector2, game: "PyCrypts", room: "Room"):
        super().__init__(game, room, position, "sword", 64)

        self.target = target
        self.user = user
        self.time_left = 0.5
        self.used = False
        self.very_clip = True

    def tick(self):
        super().tick()
        self.time_left -= self.game.dt

        if self.time_left <= 0 or not self.user.is_valid():
            self.unload()

        offset = Vector2(self.target.position - self.user.position)

        y = offset.y
        offset.y = 0

        if offset.length_squared() != 0:
            offset = offset.normalize() * (self.user.size / 2)
        offset.y = math.copysign(1, y) * (self.user.size / 4)

        if offset.x < 0:
            self.image = pygame.transform.flip(self.base_image, False, True)
        else:
            self.image = pygame.transform.flip(self.base_image, True, True)

        self.position = self.user.position + offset

        if self.is_hitting(self.target) and not self.used:
            if isinstance(self.target, Fireball):
                self.target.unload()
                return

            if isinstance(self.target, LivingEntity):
                self.target.damage(20)
                self.target.velocity = (self.target.position - self.user.position).normalize() * 20 * self.user.room.scale
                self.used = True
                self.time_left = 0.2

    def is_colliding(self, entity: Collidable) -> bool:
        if super().is_colliding(entity):
            if isinstance(entity, type(self.user)):
                return False

            if isinstance(entity, Projectile):
                entity.unload()

            return True
        return False

    def is_hitting(self, entity: Collidable) -> bool:
        return super().is_colliding(entity)
