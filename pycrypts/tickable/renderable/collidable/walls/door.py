from typing import TYPE_CHECKING, Sequence, Callable

import pygame
from pygame import Rect, Vector2, Color

from .wall import Wall
from ..collidable import Collidable

if TYPE_CHECKING:
    from .....game import PyCrypts
    from .....rooms.room import Room


class Door(Wall):
    def __init__(self, top_left: tuple[int, int], bottom_right: tuple[int, int], destination: "Room", spawn: Vector2 | None, game: "PyCrypts", room: "Room", color: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | Sequence[int] = None, locked: Callable[[], bool] = lambda: False, on_enter: Callable[[], None] = lambda: None):
        if color is None:
            color = [140, 65, 5, 255]

        self.destination = destination
        self.spawn = spawn
        self.game = game
        self.locked = locked
        self.on_enter = on_enter

        super().__init__(top_left, bottom_right, game, room, False, color)

    def render(self):
        width = self.bottom_right.x - self.top_left.x
        height = self.bottom_right.y - self.top_left.y

        in_door = False
        for living in self.room.get_living_entities():
            if self.is_in_door(living):
                in_door = True
                break

        if in_door:
            translucent_color = self.color
            translucent_color[3] = 224

            transparent_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            transparent_surface.fill(translucent_color)
            self.game.screen.blit(transparent_surface, self.top_left)
        else:
            pygame.draw.rect(self.game.screen, self.color, Rect(self.top_left, (width, height)))

    def on_players_enter(self):
        self.on_enter()

        if self.destination is None:
            return

        players = self.game.players

        for player in players:
            self.game.logger.info(f"Sending {player} to {self.destination} at {self.spawn}")

            player.position = Vector2(self.spawn) + (player.size, player.size) # Clone the vector.
            player.set_scale(self.destination.scale)
            player.room = self.destination

        self.destination.load()
        self.room.unload()

    def tick(self):
        super().tick()

        players = self.game.players

        if len(players) == 0:
            return

        for player in players:
            if not self.is_in_door(player):
                return

        self.on_players_enter()

    def is_colliding(self, other: Collidable) -> bool:
        if self.locked():
            return self.is_in_door(other)

        return False

    def is_in_door(self, other: Collidable) -> bool:
        return super().is_colliding(other)
