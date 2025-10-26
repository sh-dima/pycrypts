import math
from typing import TYPE_CHECKING

from pygame import Vector2

from .ai.goals.back_off_from_target import BackOffFromTargetGoal
from .ai.goals.random_wander import RandomWanderGoal
from .ai.goals.walk_to_target import WalkToTargetGoal
from .monster import Monster
from ..living_entity import LivingEntity
from ..players.player import Player
from ...entity import Entity
from ...traps.saw_trap import SawTrap

if TYPE_CHECKING:
    from .......game import PyCrypts
    from .......rooms.room import Room


class Specter(Monster):

    def __init__(self, game: "PyCrypts", room: "Room", position: tuple[int, int], size: int = 64):
        damage_sound = game.get_sound("specter_damage")
        damage_sound.set_volume(0.5)

        super().__init__(game, room, position, size, 80, damage_sound, game.get_sound("specter_death"))

        self.wander_direction = Vector2(0, 0)
        self.wander_time = 0
        self.idle_time = 0
        self.wandering = False
        self.no_clip = True
        self.light_counter = 0
        self.light_radius = 100

    def render(self):
        super().render()
        self.light_counter += 1

        factor = math.sin(self.light_counter * 0.01)
        if factor < 0:
            return

        self.render_light(int(self.light_radius * factor))

    def register_goals(self):
        self.goals.append(BackOffFromTargetGoal(self, 0, self.game, SawTrap, self.game.tickables, 0.7, 100))
        self.goals.append(WalkToTargetGoal(self, 1, self.game, Player, self.game.players, 0.65))
        self.goals.append(RandomWanderGoal(self, 2, self.game, 0.35, 2.0, 1.5, 0.35))

    def attack_entity(self, entity: "LivingEntity"):
        if self.position.distance_squared_to(entity.position) < (10000 * self.game.current_room.scale * self.game.current_room.scale):
            entity.damage(15)
            entity.velocity += (entity.position - self.position).normalize() * 80

    def sees_other(self, other: "Entity") -> bool:
        return other.position.distance_squared_to(self.position) < 500 * 500
