from typing import TYPE_CHECKING, TypeVar, Generic

from ..goal import Goal
from ...monster import Monster
from ....players.player import Player

T = TypeVar('T')

if TYPE_CHECKING:
    from .........game import PyCrypts


class WalkToTargetGoal(Goal, Generic[T]):
    def __init__(self, owner: Monster, priority: int, game: "PyCrypts", target_type: type[T], target_list: list, speed=1):
        super().__init__(owner, priority, game)

        self.target_type = target_type
        self.target_list = target_list
        self.speed = speed
        self.cached_target: Player | None = None

    def start(self):
        super().start()

    def tick(self):
        if self.owner.velocity.magnitude_squared() > 0:
            return

        self.owner.move_towards(self.cached_target, self.speed)

    def end(self):
        super().end()
        self.cached_target = None

    def can_use(self) -> bool:
        return super().can_use() and self.get_nearby_targets_and_cache() is not None

    def get_nearby_targets_and_cache(self) -> T | None:
        players = list(filter(lambda p: isinstance(p, self.target_type) and self.owner.sees_other(p), self.target_list))

        if len(players) == 0:
            return None

        self.cached_target = min(players, key=lambda p: self.owner.position.distance_squared_to(p.position))
        return self.cached_target
