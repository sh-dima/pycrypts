from typing import TYPE_CHECKING

import pygame
from pygame import Vector2

from .ai.goals.back_off_from_target import BackOffFromTargetGoal
from .ai.goals.random_wander import RandomWanderGoal
from .ai.goals.strafe_to_target import StrafeToTargetGoal
from .monster import Monster
from ..players.player import Player
from ...traps.saw_trap import SawTrap

if TYPE_CHECKING:
    from .......game import PyCrypts
    from ..living_entity import LivingEntity
    from .......rooms.room import Room


class Zombie(Monster):
    wander_cooldown = 2.0
    wander_duration = 1.5
    randomness = 0.35

    def __init__(self, game: "PyCrypts", room: "Room", position: tuple[int, int], size: int = 64):
        super().__init__(game, room, position, size, 80, game.get_sound('zombie_damage'), game.get_sound('zombie_death'))

        self.wander_direction = Vector2(0, 0)
        self.wander_time = 0
        self.idle_time = 0
        self.wandering = False

    def register_goals(self):
        self.goals.append(RandomWanderGoal(self, 2, self.game, 0.35, Zombie.wander_duration, Zombie.wander_cooldown, Zombie.randomness))
        self.goals.append(StrafeToTargetGoal(self, 1, self.game, Player, self.game.players, 0.65))
        self.goals.append(BackOffFromTargetGoal(self, 0, self.game, SawTrap, self.game.tickables, 0.7, 100))

    def attack_entity(self, entity: "LivingEntity"):
        if self.position.distance_squared_to(entity.position) < (10000 * self.game.current_room.scale * self.game.current_room.scale):
            entity.damage(20)
            entity.velocity += (entity.position - self.position).normalize() * 40 * self.room.scale
