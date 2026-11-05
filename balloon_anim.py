import math
import random

import pygame


TARGETS_BY_LEVEL = (
    "balloon",
    "bottle",
    "boomerang",
    "star",
    "ufo",
    "duck",
    "rocket",
    "potion",
    "gem",
    "comet",
)

TARGET_COLORS = {
    "balloon": (255, 91, 112),
    "bottle": (81, 219, 174),
    "boomerang": (255, 183, 74),
    "star": (255, 226, 91),
    "ufo": (111, 190, 255),
    "duck": (255, 205, 87),
    "rocket": (255, 116, 95),
    "potion": (193, 111, 255),
    "gem": (77, 231, 231),
    "comet": (255, 145, 207),
}


def polygon_points(center, radius, count, rotation=0, inner_radius=None):
    points = []
    for index in range(count):
        angle = rotation + math.tau * index / count
        point_radius = radius
        if inner_radius is not None and index % 2:
            point_radius = inner_radius
        points.append(
            (round(center[0] + math.cos(angle) * point_radius),
             round(center[1] + math.sin(angle) * point_radius))
        )
    return points


class Target:
    def __init__(self, kind, x, y, radius, speed, drift):
        self.kind = kind
        self.x = float(x)
        self.y = float(y)
        self.radius = radius
        self.speed = speed
        self.drift = drift
        self.phase = random.random() * math.tau
        self.rotation = random.uniform(0, 360)
        self.color = TARGET_COLORS[kind]

    def update(self, delta_time):
        self.phase += delta_time * 2.2
        self.rotation += delta_time * (170 if self.kind in ("boomerang", "star", "gem") else 75)
        self.x += (self.drift + math.sin(self.phase) * 12) * delta_time
        self.y -= self.speed * delta_time

    def draw(self, screen):
        center = (round(self.x), round(self.y))
        radius = self.radius
        color = self.color
        dark = tuple(max(0, channel - 48) for channel in color)
        light = tuple(min(255, channel + 65) for channel in color)

        if self.kind == "balloon":
            pygame.draw.ellipse(screen, dark, (center[0] - radius + 3, center[1] - radius + 5, radius * 2 - 6, radius * 2 - 4))
            pygame.draw.ellipse(screen, color, (center[0] - radius, center[1] - radius, radius * 2, radius * 2))
            pygame.draw.polygon(screen, dark, ((center[0] - 5, center[1] + radius - 1), (center[0] + 5, center[1] + radius - 1), (center[0], center[1] + radius + 7)))
            pygame.draw.line(screen, (218, 222, 230), (center[0], center[1] + radius + 6), (center[0] + round(math.sin(self.phase) * 5), center[1] + radius + 24), 1)
            pygame.draw.ellipse(screen, (255, 255, 255), (center[0] - radius // 2, center[1] - radius // 2, max(5, radius // 4), max(8, radius // 2)))
        elif self.kind == "bottle":
            body = pygame.Rect(center[0] - radius // 2, center[1] - radius // 2, radius, radius + 10)
            neck = pygame.Rect(center[0] - radius // 4, center[1] - radius - 8, radius // 2, radius // 2)
            pygame.draw.rect(screen, dark, body.move(2, 3), border_radius=7)
            pygame.draw.rect(screen, color, body, border_radius=7)
            pygame.draw.rect(screen, light, neck, border_radius=3)
            pygame.draw.rect(screen, (255, 219, 120), (body.x + 3, body.y + 8, body.width - 6, 6), border_radius=3)
            pygame.draw.line(screen, (235, 255, 249), (body.x + 5, body.y + 6), (body.x + 5, body.bottom - 6), 2)
        elif self.kind == "boomerang":
            angle = math.radians(self.rotation)
            shape = ((-radius, -radius // 2), (-radius // 2, -radius // 3), (radius, radius // 2), (radius // 2, radius), (radius // 3, radius // 2), (-radius // 2, radius // 3))
            points = [(round(center[0] + x * math.cos(angle) - y * math.sin(angle)), round(center[1] + x * math.sin(angle) + y * math.cos(angle))) for x, y in shape]
            pygame.draw.polygon(screen, dark, [(x + 2, y + 3) for x, y in points])
            pygame.draw.polygon(screen, color, points)
            pygame.draw.lines(screen, light, False, points[1:4], 3)
        elif self.kind == "star":
            points = polygon_points(center, radius, 10, math.radians(self.rotation) - math.pi / 2, radius * 0.46)
            pygame.draw.polygon(screen, (94, 69, 33), [(x + 2, y + 3) for x, y in points])
            pygame.draw.polygon(screen, color, points)
            pygame.draw.circle(screen, (255, 255, 224), center, max(3, radius // 5))
        elif self.kind == "ufo":
            pygame.draw.ellipse(screen, light, (center[0] - radius // 2, center[1] - radius // 2 - 7, radius, radius))
            pygame.draw.ellipse(screen, color, (center[0] - radius, center[1] - radius // 3, radius * 2, radius))
            pygame.draw.ellipse(screen, dark, (center[0] - radius, center[1] - radius // 3, radius * 2, radius), 3)
            for offset in (-radius // 2, 0, radius // 2):
                pygame.draw.circle(screen, (255, 240, 139), (center[0] + offset, center[1] + radius // 3), 3)
        elif self.kind == "duck":
            pygame.draw.ellipse(screen, color, (center[0] - radius, center[1] - radius // 2, radius * 2, radius))
            pygame.draw.circle(screen, color, (center[0] + radius // 2, center[1] - radius // 2), radius // 2)
            pygame.draw.polygon(screen, (255, 137, 71), ((center[0] + radius, center[1] - radius // 2), (center[0] + radius + 10, center[1] - radius // 3), (center[0] + radius, center[1] - radius // 5)))
            pygame.draw.circle(screen, (40, 47, 67), (center[0] + radius // 2 + 3, center[1] - radius // 2 - 2), 2)
            pygame.draw.ellipse(screen, light, (center[0] - radius // 2, center[1], radius, radius // 3))
        elif self.kind == "rocket":
            angle = math.radians(self.rotation)
            direction = pygame.Vector2(math.cos(angle), math.sin(angle))
            side = pygame.Vector2(-direction.y, direction.x)
            tip = pygame.Vector2(center) + direction * radius
            tail = pygame.Vector2(center) - direction * radius
            body_points = [tip, tail + side * (radius * 0.48), tail - side * (radius * 0.48)]
            pygame.draw.polygon(screen, color, body_points)
            pygame.draw.polygon(screen, light, [tip, tail + side * (radius * 0.14), tail - side * (radius * 0.14)])
            pygame.draw.circle(screen, (121, 218, 255), (round(center[0] + direction.x * radius * 0.1), round(center[1] + direction.y * radius * 0.1)), max(3, radius // 5))
            pygame.draw.polygon(screen, (255, 179, 68), [tail - direction * 8, tail + side * 6, tail - side * 6])
        elif self.kind == "potion":
            body = pygame.Rect(center[0] - radius // 2, center[1] - radius // 3, radius, radius + 2)
            pygame.draw.rect(screen, color, body, border_radius=radius // 3)
            pygame.draw.rect(screen, light, (center[0] - radius // 4, center[1] - radius // 2 - 6, radius // 2, 9), border_radius=2)
            pygame.draw.rect(screen, (255, 255, 255), (body.x + 4, body.y + 7, 3, max(7, body.height // 3)), border_radius=2)
            pygame.draw.arc(screen, light, body, math.pi, math.tau, 2)
        elif self.kind == "gem":
            points = polygon_points(center, radius, 6, math.radians(self.rotation) - math.pi / 2)
            pygame.draw.polygon(screen, dark, [(x + 2, y + 3) for x, y in points])
            pygame.draw.polygon(screen, color, points)
            pygame.draw.polygon(screen, light, (points[0], points[1], center, points[5]))
            pygame.draw.line(screen, light, points[1], points[4], 2)
        else:
            tail = (center[0] - radius - 15, center[1] + round(math.sin(self.phase) * 5))
            pygame.draw.line(screen, dark, tail, center, radius // 2)
            pygame.draw.circle(screen, color, center, radius)
            pygame.draw.circle(screen, light, (center[0] - radius // 3, center[1] - radius // 3), max(4, radius // 3))
            pygame.draw.circle(screen, (255, 244, 191), center, radius, 2)

    def contains(self, point):
        dx = point[0] - self.x
        dy = point[1] - self.y
        return dx * dx + dy * dy <= (self.radius * 1.15) ** 2


class Particle:
    def __init__(self, x, y, color):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(55, 230)
        self.x = float(x)
        self.y = float(y)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = color
        self.life = random.uniform(0.3, 0.65)
        self.max_life = self.life
        self.radius = random.randint(2, 5)

    def update(self, delta_time):
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time
        self.vx *= 0.97
        self.vy *= 0.97
        self.life -= delta_time

    def draw(self, screen):
        fade = max(0, self.life / self.max_life)
        color = tuple(round(channel * fade) for channel in self.color)
        radius = max(1, round(self.radius * fade))
        pygame.draw.circle(screen, color, (round(self.x), round(self.y)), radius)


class BalloonField:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.balloons = []
        self.particles = []
        self.level = 1

    def set_level(self, level):
        self.level = max(1, min(level, len(TARGETS_BY_LEVEL)))

    def spawn(self):
        kind = random.choice(TARGETS_BY_LEVEL[:self.level])
        radius = random.randint(22, 34)
        speed_bonus = (self.level - 1) * 5
        self.balloons.append(
            Target(
                kind,
                random.randint(radius + 20, self.width - radius - 20),
                self.height + radius,
                radius,
                random.uniform(95, 155) + speed_bonus,
                random.uniform(-30, 30),
            )
        )

    def _burst(self, target):
        self.particles.extend(Particle(target.x, target.y, target.color) for _ in range(18))

    def update(self, delta_time):
        for target in self.balloons:
            target.update(delta_time)
        for particle in self.particles:
            particle.update(delta_time)

        escaped = sum(target.y + target.radius < 124 for target in self.balloons)
        self.balloons = [target for target in self.balloons if target.y + target.radius >= 124]
        self.particles = [particle for particle in self.particles if particle.life > 0]
        return escaped

    def draw(self, screen):
        for target in self.balloons:
            target.draw(screen)
        for particle in self.particles:
            particle.draw(screen)

    def pop_at(self, position):
        for index in range(len(self.balloons) - 1, -1, -1):
            target = self.balloons[index]
            if target.contains(position):
                self._burst(target)
                del self.balloons[index]
                return True
        return False

    def pop_all(self):
        popped = len(self.balloons)
        for target in self.balloons:
            self._burst(target)
        self.balloons.clear()
        return popped

    def reset(self):
        self.balloons.clear()
        self.particles.clear()
        self.set_level(1)
