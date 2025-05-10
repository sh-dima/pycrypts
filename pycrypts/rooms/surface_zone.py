from typing import TYPE_CHECKING

from .room import Room
from ..tickable.renderable.collidable.entities.helmet import Helmet
from ..tickable.renderable.collidable.entities.living.monsters.skeleton import Skeleton
from ..tickable.renderable.collidable.entities.living.monsters.zombie import Zombie
from ..tickable.renderable.collidable.entities.shield import Shield
from ..tickable.renderable.collidable.walls.door import Door
from ..tickable.renderable.collidable.walls.wall import Wall

if TYPE_CHECKING:
    from ..game import PyCrypts


class SurfaceZone(Room):
    def __init__(self, game: "PyCrypts"):
        spawn = (game.top_right + (-200, 240))

        super().__init__(game, spawn)

    def create(self):
        super().create()

        Zombie(self.game, self, self.game.bottom_left + (160, -200))
        Zombie(self.game, self, self.game.bottom_left + (300, -200))

        Wall(self.game.top_left, self.game.bottom_left + (80, 0), self.game, self, True)
        border_right_1 = Wall(self.game.top_right + (-80, 0), self.game.top_right + (0, 240), self.game, self, True)
        border_right_2 = Wall(self.game.top_right + (-80, 480), self.game.bottom_right, self.game, self, True)
        Wall(border_right_1.bottom_right, border_right_2.top_left + (160, 0), self.game, self, True)
        border_top_1 = Wall(self.game.top_left, self.game.top_left + (160, 80), self.game, self, True)
        border_top_2 = Wall(self.game.top_left + (400, 0), self.game.top_right + (0, 80), self.game, self, True)
        Wall(border_top_1.bottom_right + (0, -160), border_top_2.top_left, self.game, self, True)
        Wall(self.game.bottom_left + (0, -80), self.game.bottom_right, self.game, self, True)

        Wall(self.game.top_left + (480, 0), self.game.top_left + (560, 160), self.game, self)
        Wall(self.game.top_left + (480, 320), self.game.bottom_left + (560, 0), self.game, self)

        Door(
            self.game.top_right + (-80, 240),
            self.game.top_right + (0, 480),
            None, None, self.game, self)

        Door(
            self.game.top_left + (160, 0),
            self.game.top_left + (400, 80),
            self.game.entrance_zone,
            self.game.entrance_zone.spawn,
            self.game, self)
