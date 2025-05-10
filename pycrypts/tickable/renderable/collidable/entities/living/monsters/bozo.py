import os

import random
from typing import TYPE_CHECKING, Type, List

import pygame

from .ai.goals.back_off_from_target import BackOffFromTargetGoal
from .ai.goals.blast_bozos_balls import BlastBozosBallsGoal
from .ai.goals.random_wander import RandomWanderGoal
from .ai.goals.walk_to_target import WalkToTargetGoal
from .skeleton import Skeleton
from .specter import Specter
from .zombie import Zombie
from ..players.player import Player
from ...helmet import Helmet
from ...projectiles.bozos_ball import BozosBall
from ...shield import Shield
from ....collidable import Collidable
from .monster import Monster
from .....display.boss_health_bar import BossHealthBar

if TYPE_CHECKING:
    from .......rooms.bozo_boss_barrack import BozoBossBarrack
    from .......game import PyCrypts
    from ..living_entity import LivingEntity
    from ...entity import Entity


class Bozo(Monster):

    def __init__(self, game: "PyCrypts", room: "BozoBossBarrack", position: tuple[int, int], summon_mobs_interval: float = 15):
        self.back_off_goal = BackOffFromTargetGoal(self, 0, game, Player, game.players, 0.7, 200)
        self.chase_goal = WalkToTargetGoal(self, 1, game, Player, game.players, 1.1)
        self.blast_balls_goal = BlastBozosBallsGoal(self, 1, game)
        self.wander_goal = RandomWanderGoal(self, 1, game, 1.5, 1.5, 0.1, 0.35)
        self.crazy_wander_goal = RandomWanderGoal(self, 1, game, 2.0, 1.5, 0.1, 0.35)

        self.room = room

        damage_sound = game.get_sound("bozo_damage")
        damage_sound.set_volume(0.5)

        super().__init__(game, room, position, 70, 750, damage_sound)

        self.last_hit = 0

        self.is_calm = True
        self.is_aggressive = False
        self.is_going_crazy = False

        self.remaining_calmness = 5
        self.remaining_aggression = 0
        self.remaining_craziness = 0

        self.summon_mobs_interval = summon_mobs_interval
        self.summon_mobs_timer = self.summon_mobs_interval

        self.ball_types = list(map(lambda f: f.removesuffix(".svg"), os.listdir("./assets/images/entities/balls")))

        game.logger.debug(f"Found {len(self.ball_types)} {type(self).__name__}'s ball types:")
        game.logger.debug(self.ball_types)

        self.health_bar: BossHealthBar | None = None

    def register_goals(self):
        self.goals.append(self.blast_balls_goal)
        self.goals.append(self.back_off_goal)
        self.goals.append(self.chase_goal)
        self.goals.append(self.wander_goal)

    def tick(self):
        super().tick()

        if self.health_bar is not None:
            self.health_bar.tick()

        self.health += (10 if self.game.get_millis() - self.last_hit > 12 * 1000 else 1) * self.game.dt
        self.health = min(self.max_health, self.health)

    def ai_tick(self):
        if not self.room.brittle_wall.is_broken():
            return

        super().ai_tick()

        if self.health_bar is None:
            self.health_bar = BossHealthBar(self.game, self, (50, 50), 5 + self.size + 5, 5)

        self.summon_mobs_timer -= self.game.dt
        if self.summon_mobs_timer <= 0:
            self.summon_mobs_timer = self.summon_mobs_interval

            self.summon_mobs()

        if self.is_calm:
            self.remaining_calmness -= self.game.dt

            if self.remaining_calmness < 0:
                self.is_calm = False

                if random.choice([True, False]):
                    self.is_aggressive = True
                    self.remaining_aggression = random.randint(5, 7)
                    self.on_aggressive()
                else:
                    self.is_going_crazy = True
                    self.remaining_craziness = random.randint(4, 5)
                    self.on_going_crazy()
        elif self.is_aggressive:
            self.remaining_aggression -= self.game.dt

            if self.remaining_aggression < 0:
                self.is_aggressive = False

                if random.choice([True, False]):
                    self.is_calm = True
                    self.remaining_calmness = random.randint(5, 7)
                    self.on_calm()
                else:
                    self.is_going_crazy = True
                    self.remaining_craziness = random.randint(4, 5)
                    self.on_going_crazy()
        elif self.is_going_crazy:
            self.remaining_craziness -= self.game.dt

            if self.remaining_craziness < 0:
                self.is_going_crazy = False

                if random.choice([True, False]):
                    self.is_aggressive = True
                    self.remaining_aggression = random.randint(5, 7)
                    self.on_aggressive()
                else:
                    self.is_calm = True
                    self.remaining_calmness = random.randint(5, 7)
                    self.on_calm()

    def on_calm(self):
        self.game.logger.debug("Bozo calm phase has begun")
        self.goals.clear()

        self.goals.append(self.back_off_goal)
        self.goals.append(self.blast_balls_goal)
        self.goals.append(self.wander_goal)

    def on_aggressive(self):
        self.game.logger.debug("Bozo aggressive phase has begun")
        self.goals.clear()

        self.goals.append(self.blast_balls_goal)
        self.goals.append(self.chase_goal)

    def on_going_crazy(self):
        self.game.logger.debug("Bozo crazy phase has begun")
        self.goals.clear()

        self.goals.append(self.blast_balls_goal)
        self.goals.append(self.crazy_wander_goal)

    def is_colliding(self, entity: Collidable) -> bool:
        if isinstance(entity, BozosBall):
            return False

        return super().is_colliding(entity)

    def attack_entity(self, entity: "LivingEntity"):
        if self.position.distance_squared_to(entity.position) < (10000 * self.game.current_room.scale * self.game.current_room.scale):
            entity.damage(15)
            entity.velocity += (entity.position - self.position).normalize() * 40 * self.room.scale

    def die(self):
        super().die()

        pygame.mixer.music.stop()

    def damage(self, damage: float):
        super().damage(damage)

        self.last_hit = self.game.get_millis()

    def summon_minion(self, entity_type: Type["Entity"], max_attempts: int = 5, distance_scale: float = 1.25, *entity_constructor_arguments):
        entity = super().summon_minion(entity_type, max_attempts, distance_scale, *entity_constructor_arguments)

        if entity is None:
            return None

        if random.random() < 0.25 and not entity.no_clip:
            Shield(entity, self.game, self.room)

        if random.random() < 0.25 and not entity.no_clip:
            Helmet(entity, self.game, self.room)

        return entity

    def summon_mobs(self):
        mob_count = random.randint(1, 2)

        mob_types: List[Type[Monster]] = random.choices(
            [Zombie, Skeleton, Specter],
            [8, 6, 1],
            k = mob_count
        )

        for mob_type in mob_types:
            self.summon_minion(mob_type, 15, 1.25, self.game, self.room, self.position)
