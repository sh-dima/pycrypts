from typing import TYPE_CHECKING

from pygame import Vector2

from ..tickable.renderable.collidable.collidable import Collidable
from ..tickable.renderable.collidable.entities.living.living_entity import LivingEntity
from ..tickable.renderable.collidable.walls.wall import Wall

if TYPE_CHECKING:
    from ..game import PyCrypts


class Room:
    def __init__(self, game: "PyCrypts", spawn: Vector2, scale=1.0, illuminated=False):
        game.logger.info(f"Instantiating room {self}")

        self.spawn = spawn
        self.scale = scale
        self.game = game
        self.created = False
        self.illuminated = illuminated

    def create(self):
        self.game.logger.info(f"Creating room {self} for the first time")
        self.created = True

    def load(self):
        self.game.logger.info(f"Loading room {self}")

        self.game.current_room = self

        if not self.created:
            self.create()

    def unload(self):
        from ..tickable.renderable.collidable.entities.projectiles.projectile import Projectile
        for collidable in self.get_collidables():
            if isinstance(collidable, Projectile):
                collidable.unload()

    def get_collidables(self) -> list[Collidable]:
        return list(filter(lambda collidable: collidable.room == self, self.game.get_collidables()))

    def get_monsters(self):
        return list(filter(lambda monster: monster.room == self, self.game.get_monsters()))

    def get_walls(self) -> list[Wall]:
        return list(filter(lambda collidable: isinstance(collidable, Wall), self.get_collidables()))

    def get_living_entities(self) -> list[LivingEntity]:
        return list(filter(lambda collidable: isinstance(collidable, LivingEntity), self.get_collidables()))

    def __str__(self):
        return type(self).__name__
