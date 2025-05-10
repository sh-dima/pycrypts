import random

from pygame import Vector2

from ..goal import Goal


class RandomWanderGoal(Goal):
    def __init__(self, owner, priority, game, speed=1, wander_duration=1, wander_cooldown=1, randomness=0.35):
        super().__init__(owner, priority, game)

        self.speed = speed
        self.wander_duration = wander_duration
        self.wander_cooldown = wander_cooldown
        self.randomness = randomness

        self.wander_time = 0
        self.idle_time = 0

        self.wander_direction: Vector2 | None = None
        self.wandering = False

    def start(self):
        super().start()
        self.start_wandering()

    def tick(self, move=True):
        if self.wandering:
            if move:
                self.owner.move_without_collision(self.wander_direction, self.speed)
            self.wander_time += self.game.dt

            if self.wander_time >= self.wander_duration + random.uniform(-self.randomness, self.randomness):
                self.stop_wandering()
        else:
            self.idle_time += self.game.dt

            if self.idle_time >= self.wander_cooldown + random.uniform(-self.randomness, self.randomness):
                self.start_wandering()

    def end(self):
        super().end()
        self.stop_wandering()

    def can_use(self) -> bool:
        return super().can_use()

    def start_wandering(self):
        self.wander_direction = Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.wandering = True
        self.idle_time = 0

    def stop_wandering(self):
        self.wandering = False
        self.wander_time = 0
