import math
import random
from typing import TypeVar

from pygame import Vector2

from .walk_to_target import WalkToTargetGoal

T = TypeVar('T')


def adjust_vector_by_angle(v: Vector2, angle: float) -> Vector2:
    radians = math.radians(angle)
    cos_angle = math.cos(radians)
    sin_angle = math.sin(radians)
    return Vector2(v.x * cos_angle - v.y * sin_angle, v.x * sin_angle + v.y * cos_angle)


class StrafeToTargetGoal(WalkToTargetGoal[T]):
    def __init__(self, owner, priority, game, target_type: type[T], target_list: list, speed=1):
        super().__init__(owner, priority, game, target_type, target_list, speed)
        self.strafe_timer = 0
        self.strafe_direction = 60

    def start(self):
        super().start()

    def tick(self):
        if self.owner.velocity.magnitude() > 0:
            return

        self.strafe_timer += self.game.dt

        if self.strafe_timer >= 1 + random.uniform(-0.15, 0.15):
            self.strafe_direction = -self.strafe_direction
            self.strafe_timer = 0

        distance = self.cached_target.position - self.owner.position
        strafe = adjust_vector_by_angle(distance, self.strafe_direction)

        distance = distance.normalize() + strafe.normalize() * 3
        self.owner.move_without_collision(distance, self.speed)

    def end(self):
        super().end()
