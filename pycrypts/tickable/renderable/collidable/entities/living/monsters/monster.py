from typing import TYPE_CHECKING

from pygame.mixer import Sound

from ..living_entity import LivingEntity
from ..players.player import Player

if TYPE_CHECKING:
    from .......game import PyCrypts
    from .......rooms.room import Room
    from .ai.goal import Goal


class Monster(LivingEntity):
    attack_interval = 1.0

    def __init__(self, game: "PyCrypts", room: "Room", position: tuple[int, int], size: int = 64, health: int = 50, damage_sound: Sound | None = None, death_sound: Sound | None = None):
        super().__init__(game, room, position, "monsters/" + type(self).__name__.lower(), size, health, damage_sound, death_sound)
        self.attack_timer = 0
        self.game = game
        self.goals: list["Goal"] = []
        self.last_ticked_goals: list["Goal"] = []
        self.seen = False

        self.register_goals()

    def register_goals(self):
        pass

    def tick(self):
        super().tick()

        if not self.seen:
            threshold = Player.render_distance_squared * self.room.scale * self.room.scale

            for player in self.game.players:
                distance_squared = player.position.distance_squared_to(self.position)

                if distance_squared < threshold:
                    self.seen = True
                    self.game.logger.debug(f"Player {player} saw monster {self} for the first time!")
                    break

        self.ai_tick()

        self.attack_timer += self.game.dt

        if self.attack_timer >= self.attack_interval:
            self.attack_timer = 0
            self.attack()

    def ai_tick(self):
        usable_goals : list["Goal"] = list(filter(lambda g: g.can_use(), self.goals))
        if len(usable_goals) == 0:
            return

        highest_priority = list(sorted(usable_goals, key=lambda g: g.priority))[0].priority
        goals_to_tick = list(filter(lambda g: g.priority == highest_priority, usable_goals))
        goals_to_end = list(filter(lambda g: g not in goals_to_tick, self.last_ticked_goals))

        for goal in goals_to_end:
            goal.end()

        for goal in goals_to_tick:
            if goal not in self.last_ticked_goals:
                goal.start()

            goal.tick()

        self.last_ticked_goals = goals_to_tick

    def attack(self):
        players = list(filter(lambda p: self.sees_other(p), self.game.players))
        player_count = len(players)

        if player_count == 0:
            return

        player = min(players, key=lambda p: self.position.distance_squared_to(p.position))
        self.attack_entity(player)

    def attack_entity(self, entity: LivingEntity):
        pass
