from typing import TYPE_CHECKING

from pygame import Vector2

from ..entity import Entity
from ...collidable import Collidable

if TYPE_CHECKING:
    from pycrypts.rooms.room import Room
    from pycrypts.game import PyCrypts


class Projectile(Entity):

    def __init__(self, game: "PyCrypts", room: "Room", shooter: Entity, position: tuple[int, int] | Vector2, character: str, direction: Vector2, strength: float = 0, speed: float = 1, size: int = 32):
        super().__init__(game, room, position, character, size)

        self.direction = direction
        self.shooter = shooter
        self.speed = speed
        self.strength = strength

    def tick(self):
        super().tick()

        from ..living.monsters.monster import Monster
        if isinstance(self.shooter, Monster) and self.shooter.seen:
            return

        from ..living.players.player import Player
        threshold = Player.render_distance_squared * self.room.scale * self.room.scale

        for player in self.game.players:
            distance_squared = player.position.distance_squared_to(self.position)

            if distance_squared < threshold:
                self.shooter.seen = True
                self.game.logger.debug(f"Player {player} saw monster {self.shooter} for the first time!")
                break

    def move(self):
        self.move_without_collision(self.direction, self.speed)

    def is_colliding(self, entity: Collidable) -> bool:
        colliding = super().is_colliding(entity)

        if not colliding:
            return False

        if isinstance(entity, type(self)):
            return False

        if isinstance(entity, type(self.shooter)):
            return False

        if isinstance(entity, Projectile):
            if entity.strength <= self.strength:
                entity.unload()
                return False

        self.on_hit(entity)
        return True

    def on_hit(self, collidable: Collidable):
        self.unload()
