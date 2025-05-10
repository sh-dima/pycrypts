from math import sqrt
import random
from typing import TYPE_CHECKING, Type

import pygame
from pygame import Vector2, Surface

from ..collidable import Collidable

if TYPE_CHECKING:
    from .....game import PyCrypts
    from .....rooms.room import Room


class Entity(Collidable):
    def __init__(self, game: "PyCrypts", room: "Room", position: tuple[int, int] | Vector2, character: str, size: int):
        super().__init__(game, room)

        self.position = Vector2(position)
        self.velocity = Vector2(0, 0)

        self.game = game

        self.image = self.game.get_asset("./assets/images/entities/" + character)

        self.absolute_size = size
        self.size = size

        self.base_image = self.image

        self.set_scale(room.scale)

        self.base_image = self.image

    def render(self):
        self.game.screen.blit(self.image, self.position)

    def render_light(self, radius: int):
        radius = int(radius * self.room.scale)

        position = self.get_int_position()
        x, y = position[0] - radius, position[1] - radius

        texture = self.game.get_vision_texture(radius)

        self.game.fog.blit(texture, (x, y), special_flags=pygame.BLEND_RGBA_MIN)

    def tick(self):
        super().tick()
        self.move()

    def move(self):
        self.move_without_collision(self.velocity * self.game.dt)
        self.velocity *= (0.9 ** (1 / self.game.current_room.scale))

        if self.velocity.magnitude_squared() < 0.1:
            self.velocity = Vector2(0, 0)

    def move_without_collision(self, distance_travelled: Vector2, speed_factor: float = 1):
        magnitude_squared = distance_travelled.magnitude_squared()

        if magnitude_squared == 0:
            return

        collidables = self.room.get_collidables()

        distance_travelled = (distance_travelled / sqrt(magnitude_squared)) * 250 * self.room.scale * speed_factor * self.game.dt

        filtered = list(filter(lambda c: c != self, collidables))

        self.position.x += distance_travelled.x
        collision_x = any(self.is_colliding(collidable) or collidable.is_colliding(self) for collidable in filtered)
        if collision_x:
            self.position.x -= distance_travelled.x

        self.position.y += distance_travelled.y
        collision_y = any(self.is_colliding(collidable) or collidable.is_colliding(self) for collidable in filtered)
        if collision_y:
            self.position.y -= distance_travelled.y

    def move_towards(self, entity: "Entity", speed_factor: float = 1):
        self.move_towards_location(entity.position, speed_factor)

    def move_towards_location(self, location: Vector2, speed_factor: float = 1):
        distance = location - self.position
        self.move_without_collision(distance, speed_factor)

    def move_away_from(self, entity: "Entity", speed_factor: float = 1):
        distance = entity.position - self.position
        distance *= -1
        self.move_without_collision(distance, speed_factor)

    def is_colliding(self, entity: Collidable) -> bool:
        if self.no_clip or entity.no_clip and not (self.very_clip or entity.very_clip):
            return False

        if isinstance(entity, Entity):
            return self.position.distance_squared_to(entity.position) < ((self.size / 2 + entity.size / 2) ** 2)

        from ..walls.wall import Wall
        if isinstance(entity, Wall):
            return entity.is_colliding(self)
        return False

    def is_clipping(self):
        return any(filter(lambda c: self.is_colliding(c) or c.is_colliding(self), self.room.get_collidables()))

    def set_scale(self, scale: float):
        self.size = self.absolute_size * scale
        self.image = pygame.transform.scale(self.base_image, (self.size, self.size))

    def get_radius(self):
        return self.size / 2.0

    def get_center(self):
        return self.position

    def get_actual_center(self):
        return self.position + (self.get_radius(), self.get_radius())

    def get_int_position(self):
        center = self.get_actual_center()

        return int(center[0]), int(center[1])

    def get_top_left(self):
        return self.position

    def get_bottom_right(self):
        return self.position + (self.size, self.size)

    def get_top_right(self):
        return self.position + (self.size, 0)

    def get_bottom_left(self):
        return self.position + (0, self.size)

    def get_points(self):
        return [self.get_top_left(), self.get_bottom_right(), self.get_top_right(), self.get_bottom_left()]

    def sees_other(self, other: "Entity") -> bool:
        center = self.get_actual_center()
        other_center = other.get_actual_center()

        for wall in self.room.get_walls():
            from ..walls.door import Door
            if isinstance(wall, Door):
                continue

            wall_edges = wall.get_lines()  # Assume this returns [(p1, p2), (p2, p3), (p3, p4), (p4, p1)]
            for edge in wall_edges:
                if self.line_intersects(center, other_center, edge[0], edge[1]):
                    return False

        return True

    def line_intersects(self, a1: Vector2, a2: Vector2, b1: Vector2, b2: Vector2) -> bool:
        return self.ccw(a1, b1, b2) != self.ccw(a2, b1, b2) and self.ccw(a1, a2, b1) != self.ccw(a1, a2, b2)

    def ccw(self, p1, p2, p3):
        return (p3.y - p1.y) * (p2.x - p1.x) > (p2.y - p1.y) * (p3.x - p1.x)

    def summon_minion(self, entity_type: Type["Entity"], max_attempts: int = 5, distance_scale: float = 1.25, *entity_constructor_arguments):
        entity = entity_type(*entity_constructor_arguments)

        entity.unload()

        vector = Vector2(self.size + entity.size, self.size + entity.size) * distance_scale

        attempts = 0

        while entity.is_clipping():
            if attempts == max_attempts:
                return None

            vector = vector.rotate(random.randint(1, 360))
            entity.position = self.position + vector

            attempts += 1

        entity.load()
        return entity