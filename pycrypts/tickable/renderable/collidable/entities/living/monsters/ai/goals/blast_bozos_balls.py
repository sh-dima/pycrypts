import random
from typing import TYPE_CHECKING

from pygame import Vector2

from .....projectiles.bozos_ball import BozosBall
from ..goal import Goal

if TYPE_CHECKING:
    from ...bozo import Bozo
    from .........game import PyCrypts


class BlastBozosBallsGoal(Goal):
    def __init__(self, owner: "Bozo", priority: int, game: "PyCrypts"):
        super().__init__(owner, priority, game)

        self.owner = owner
        self.last_shot = 0

    def can_use(self) -> bool:
        return self.owner.is_going_crazy or self.game.get_millis() - self.last_shot > 2 * 1000

    def start(self):
        super().start()

    def tick(self):
        if random.random() > 0.05:
            return

        for _ in range(3):
            random_angle = random.randrange(0, 360)

            direction = Vector2(1, 1)
            direction = direction.rotate(random_angle)

            BozosBall(self.game, self.owner.room, self.owner, self.owner.position, direction, random.choice(self.owner.ball_types))

        now = self.game.get_millis()
        self.last_shot = now
