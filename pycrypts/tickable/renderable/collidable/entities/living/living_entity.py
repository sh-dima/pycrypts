from typing import TYPE_CHECKING

import pygame
from pygame.mixer import Sound

from ..entity import Entity

if TYPE_CHECKING:
    from ......game import PyCrypts
    from ......rooms.room import Room



class LivingEntity(Entity):

    def __init__(self, game: "PyCrypts", room: "Room", position: tuple[int, int], character: str, size: int, health: float, damage_sound: Sound | None = None, death_sound: Sound | None = None):
        super().__init__(game, room, position, "living/" + character, size)

        self.health = health
        self.max_health = health

        self.damage_sound = damage_sound
        self.death_sound = death_sound

    def damage(self, damage: float):
        self.health -= damage

        if self.health <= 0:
            self.health = 0
            self.die()
        elif self.damage_sound is not None:
            pygame.mixer.Sound.play(self.damage_sound)

    def die(self):
        self.unload()

        if self.death_sound is not None:
            pygame.mixer.Sound.play(self.death_sound)

    def attack(self):
        pass

    def attack_entity(self, entity: "LivingEntity"):
        pass
