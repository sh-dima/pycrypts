from typing import TYPE_CHECKING

import pygame
from pygame import Vector2

from ..living_entity import LivingEntity
from ...projectiles.arrow import Arrow
from ...sword import Sword
from ....collidable import Collidable

if TYPE_CHECKING:
    from ..monsters.monster import Monster
    from .......game import PyCrypts
    from .......rooms.room import Room


class Player(LivingEntity):
    attack_cooldown = 0.75
    attack_range = 100
    regeneration_rate = 1.5

    render_distance = 400
    render_distance_squared = render_distance**2

    def __init__(self, position: tuple[int, int], character: str, size: int, movement_type: str, attack_key: int, game: "PyCrypts", room: "Room"):
        super().__init__(game, room, position, "players/" + character, size, 100)

        self.movement_type = movement_type
        self.attack_key = attack_key

        self.time_since_last_attack = Player.attack_cooldown + 1

        self.light_radius = Player.render_distance

        self.base_candle_image = self.game.get_asset("assets/images/entities/lantern")
        self.candle_image = self.base_candle_image

    def load(self):
        super().load()
        self.game.players.append(self)

    def unload(self):
        super().unload()
        if self in self.game.players:
            self.game.players.remove(self)

    def tick(self):
        super().tick()

        self.time_since_last_attack += self.game.dt

        keys = pygame.key.get_pressed()
        if keys[self.attack_key]:
            self.attack()

        self.health += self.regeneration_rate * self.game.dt
        self.health = min(self.health, self.max_health)

        if keys[pygame.K_LALT]:
            self.no_clip = not self.no_clip

    def set_scale(self, scale: float):
        super().set_scale(scale)

        try:
            self.candle_image = pygame.transform.scale(self.base_candle_image, (32 * scale, 32 * scale))
        except AttributeError:
            pass

    def render(self):
        super().render()
        self.render_light(self.light_radius)

        self.game.screen.blit(self.candle_image, self.position + Vector2(50, 20) * self.room.scale)

    def move(self):
        super().move()

        keys = pygame.key.get_pressed()

        direction = pygame.Vector2()

        if keys[pygame.K_w if self.movement_type == "WASD" else pygame.K_UP]:
            direction.y -= 1
        if keys[pygame.K_s if self.movement_type == "WASD" else pygame.K_DOWN]:
            direction.y += 1
        if keys[pygame.K_a if self.movement_type == "WASD" else pygame.K_LEFT]:
            direction.x -= 1
        if keys[pygame.K_d if self.movement_type == "WASD" else pygame.K_RIGHT]:
            direction.x += 1

        if direction.magnitude_squared() == 0:
            return

        self.velocity += direction.normalize() * 250 * self.game.dt

        self.velocity *= 0.5
        self.velocity *= self.room.scale

        if self.velocity.magnitude_squared() == 0:
            return

        self.velocity = self.velocity.normalize() * min(self.velocity.magnitude(), 25)

    def attack(self):
        if self.time_since_last_attack < Player.attack_cooldown:
            return

        attackable_entities: list[Monster] = list(filter(lambda e: not isinstance(e, Player) and self.sees_other(e), self.room.get_monsters()))

        if len(attackable_entities) == 0:
            return

        closest_entity = min(attackable_entities, key=lambda e: e.position.distance_squared_to(self.position))

        if not closest_entity.seen:
            return

        self.attack_entity(closest_entity)

    def sword_attack(self, entity: LivingEntity):
        Sword(entity, self, self.get_center(), self.game, self.room)

    def bow_attack(self, entity: LivingEntity):
        Arrow(self.game, self.room, self, self.get_center(), entity.position - self.position)

    def attack_entity(self, entity: LivingEntity):
        if entity.position.distance_squared_to(self.position) < (Player.attack_range * Player.attack_range) * self.game.current_room.scale * self.game.current_room.scale:
            self.sword_attack(entity)
        else:
            self.bow_attack(entity)

        self.time_since_last_attack = 0

    def damage(self, damage: int):
        super().damage(damage)

        sound = self.game.get_sound("damage")
        pygame.mixer.Sound.play(sound)

    def die(self):
        super().die()

        if len(self.game.players) == 0:
            self.game.end()

    def is_colliding(self, entity: Collidable) -> bool:
        if isinstance(entity, Player):
            return False

        if isinstance(entity, Arrow):
            return False

        if isinstance(entity, Sword):
            return False

        return super().is_colliding(entity)
