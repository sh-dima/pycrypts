from typing import TYPE_CHECKING

from ..tickable import Tickable

if TYPE_CHECKING:
    from ...game import PyCrypts

class Renderable(Tickable):

    def __init__(self, game: "PyCrypts"):
        super().__init__(game)

    def tick(self):
        super().tick()
        self.render()

    def render(self):
        pass
