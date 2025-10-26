from typing import TYPE_CHECKING, Callable

import pygame

from .wall import Wall
from ..entities.living.monsters.monster import Monster

if TYPE_CHECKING:
    from .....game import PyCrypts
    from .....rooms.room import Room


class BrittleWall(Wall):

    def __init__(self, top_left: (int, int), bottom_right: (int, int), monsters_to_defeat: list[Monster], game: "PyCrypts", room: "Room", on_break: Callable[[], None] = lambda: None):
        super().__init__(top_left, bottom_right, game, room)

        self.monsters_to_defeat = monsters_to_defeat
        self.broken = False
        self.on_break = on_break

    def tick(self):
        if self.is_broken():
            self.set_broken()

        return super().tick()

    def is_broken(self):
        return all(map(lambda monster: not monster in self.game.tickables, self.monsters_to_defeat))

    def set_broken(self):
        self.broken = True

        sound = self.game.get_sound('wall_collapse')
        pygame.mixer.Sound.play(sound)

        self.unload()

        self.on_break()
