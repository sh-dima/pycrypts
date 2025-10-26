from typing import TYPE_CHECKING

from ..monster import Monster

if TYPE_CHECKING:
    from ........game import PyCrypts


class Goal:
    def __init__(self, owner: Monster, priority: int, game: "PyCrypts"):
        self.owner = owner
        self.priority = priority
        self.game = game

    def start(self):
        self.game.logger.debug(f"Started goal {self}")

    def tick(self):
        pass

    def end(self):
        self.game.logger.debug(f"Ended goal {self}")

    def can_use(self) -> bool:
        return True

    def __str__(self):
        return f"{type(self).__name__} of monster {self.owner}"
