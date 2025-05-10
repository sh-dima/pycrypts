from typing import TYPE_CHECKING

from pygame import Vector2

from .room import Room
from ..tickable.renderable.collidable.entities.helmet import Helmet
from ..tickable.renderable.collidable.entities.living.monsters.skeleton import Skeleton
from ..tickable.renderable.collidable.entities.living.monsters.specter import Specter
from ..tickable.renderable.collidable.entities.living.monsters.zombie import Zombie
from ..tickable.renderable.collidable.entities.shield import Shield
from ..tickable.renderable.collidable.entities.traps.saw_trap import SawTrap
from ..tickable.renderable.collidable.walls.brittle_wall import BrittleWall
from ..tickable.renderable.collidable.walls.door import Door
from ..tickable.renderable.collidable.walls.wall import Wall

if TYPE_CHECKING:
    from ..game import PyCrypts


class EntranceZone(Room):
    scale = 0.5

    def __init__(self, game: "PyCrypts"):
        spawn = Vector2(game.top_right + (-150, 240))

        self.monsters_to_defeat = []

        super().__init__(game, spawn, EntranceZone.scale)

    def create(self):
        super().create()

        skeleton_1 = Skeleton(self.game, self, (525, 375))
        skeleton_2 = Skeleton(self.game, self, (450, 375))
        skeleton_3 = Skeleton(self.game, self, (375, 375))
        skeleton_4 = Skeleton(self.game, self, (525, 275))
        skeleton_5 = Skeleton(self.game, self, (450, 275))
        skeleton_6 = Skeleton(self.game, self, (375, 275))
        skeleton_7 = Skeleton(self.game, self, (525, 175))
        skeleton_8 = Skeleton(self.game, self, (450, 175))
        skeleton_9 = Skeleton(self.game, self, (375, 175))

        Shield(skeleton_3, self.game, self)
        Shield(skeleton_6, self.game, self)
        Shield(skeleton_9, self.game, self)
        Helmet(skeleton_9, self.game, self)

        self.monsters_to_defeat.extend([skeleton_1, skeleton_2, skeleton_3, skeleton_4, skeleton_5, skeleton_6, skeleton_7, skeleton_8, skeleton_9])

        Zombie(self.game, self, (900, 400))
        shield_zombie = Zombie(self.game, self, (1000, 400))
        Shield(shield_zombie, self.game, self)

        Specter(self.game, self, (200, 600))

        SawTrap(self.game, self, Vector2(325, 450 + 32), Vector2(325, self.game.height - 95))

        Wall(self.game.top_left, self.game.bottom_left + (50, 0), self.game, self, True)
        border_right_1 = Wall(self.game.top_right + (-50, 0), self.game.top_right + (0, 240), self.game, self, True)
        border_right_2 = Wall(self.game.top_right + (-50, 480), self.game.bottom_right, self.game, self, True)

        border_right_2.unload()

        Wall(border_right_1.bottom_right, border_right_2.top_left + (100, 0), self.game, self, True)
        Wall(self.game.top_left, self.game.top_right + (0, 50), self.game, self, True)

        bottom_wall = Wall(self.game.bottom_left + (0, -50), self.game.bottom_right, self.game, self, True)

        corridor_wall = Wall((650, 500), (border_right_1.top_left.x, 550), self.game, self)

        entrance_from_surface = Door(
            self.game.top_right + (-50, 240),
            self.game.top_right + (0, 480),
            self.game.surface_zone,
            Vector2(250, 150),
            self.game, self)

        def on_enter():
            sound = self.game.get_sound("bozo_laugh")

            sound.set_volume(0.5)

            sound.play()

        bozo_boss_barrack_barricade = Door(
            corridor_wall.bottom_right,
            bottom_wall.get_top_right(),
            self.game.bozo_boss_barrack,
            self.game.bozo_boss_barrack.spawn,
            self.game,
            self,
            [125, 35, 35, 255],
            on_enter=on_enter
        )

        bozo_boss_barrack_barricade_border = Wall(
            bozo_boss_barrack_barricade.get_top_right(),
            bozo_boss_barrack_barricade.bottom_right + (50, 0),
            self.game,
            self,
            True
        )

        border_right_3 = Wall(
            entrance_from_surface.get_bottom_left(),
            bozo_boss_barrack_barricade.get_top_right(),
            self.game,
            self,
            True
        )

        Wall((1050, 200), (1100, 500), self.game, self)
        Wall((850, 25), (900, 325), self.game, self)
        wall_4 = Wall((650, 200), (700, 500), self.game, self)
        wall_5 = BrittleWall([300, 125], [350, 375], self.monsters_to_defeat, self.game, self)
        Wall(wall_5.bottom_right + (-50, 50), wall_4.bottom_right + (0, -25), self.game, self)
        Wall(wall_5.top_left + (0, -75), wall_5.bottom_right + (0, -250), self.game, self)
        Wall(wall_5.top_left + (0, 250), wall_5.bottom_right + (0, 50), self.game, self)
