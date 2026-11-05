import math
import random

import pygame


SKY_TOP = (14, 24, 58)
SKY_BOTTOM = (45, 93, 135)


def draw_background(width, height):
    background = pygame.Surface((width, height))
    for y in range(height):
        blend = y / height
        color = tuple(
            round(SKY_TOP[index] * (1 - blend) + SKY_BOTTOM[index] * blend)
            for index in range(3)
        )
        pygame.draw.line(background, color, (0, y), (width, y))

    random_generator = random.Random(12)
    for _ in range(85):
        x = random_generator.randrange(width)
        y = random_generator.randrange(30, 610)
        radius = random_generator.choice((1, 1, 2))
        brightness = random_generator.randrange(95, 190)
        pygame.draw.circle(background, (brightness, brightness + 15, 225), (x, y), radius)

    pygame.draw.circle(background, (255, 222, 157), (1080, 130), 48)
    pygame.draw.circle(background, (255, 231, 183), (1080, 130), 39)

    pygame.draw.ellipse(background, (29, 68, 91), (-180, 548, 890, 250))
    pygame.draw.ellipse(background, (24, 58, 82), (420, 562, 1080, 280))
    pygame.draw.rect(background, (16, 43, 62), (0, 650, width, height - 650))
    pygame.draw.line(background, (89, 190, 197), (0, 650), (width, 650), 2)

    return background


def draw_hud(
    screen,
    score,
    misses,
    max_misses,
    elapsed,
    title_font,
    hud_font,
    small_font,
    pops_toward_mega,
    mega_charges,
    level,
    level_progress,
    unlocked_target,
):
    width = screen.get_width()
    header = pygame.Surface((width, 124), pygame.SRCALPHA)
    header.fill((8, 15, 37, 176))
    screen.blit(header, (0, 0))

    title = title_font.render("SHOTED", True, (248, 251, 255))
    title_shadow = title_font.render("SHOTED", True, (38, 196, 209))
    screen.blit(title_shadow, (48, 25))
    screen.blit(title, (45, 22))
    subtitle = small_font.render("BALLOON POP", True, (145, 221, 229))
    screen.blit(subtitle, (49, 72))

    pygame.draw.line(screen, (77, 117, 153), (300, 35), (300, 91), 1)

    score_label = small_font.render("SCORE", True, (162, 184, 209))
    score_value = hud_font.render(f"{score:03d}", True, (255, 255, 255))
    screen.blit(score_label, (338, 30))
    screen.blit(score_value, (338, 56))

    misses_label = small_font.render("MISSED", True, (162, 184, 209))
    screen.blit(misses_label, (485, 30))
    for index in range(max_misses):
        color = (255, 105, 125) if index < misses else (74, 91, 119)
        pygame.draw.circle(screen, color, (493 + index * 21, 73), 6)

    mega_label = small_font.render("MEGA BLAST", True, (162, 184, 209))
    screen.blit(mega_label, (674, 30))
    pygame.draw.rect(screen, (50, 69, 98), (674, 68, 190, 10), border_radius=5)
    progress_width = round(190 * min(pops_toward_mega / 10, 1))
    if progress_width:
        pygame.draw.rect(screen, (75, 220, 199), (674, 68, progress_width, 10), border_radius=5)
    status_text = f"READY x{mega_charges}" if mega_charges else f"{pops_toward_mega}/10"
    status_color = (116, 242, 207) if mega_charges else (220, 230, 242)
    status = small_font.render(status_text, True, status_color)
    screen.blit(status, (878, 64))

    level_label = small_font.render(f"LEVEL {level}/10", True, (162, 184, 209))
    screen.blit(level_label, (977, 27))
    pygame.draw.rect(screen, (50, 69, 98), (977, 57, 110, 8), border_radius=4)
    if level_progress:
        progress_width = round(110 * level_progress / 10)
        pygame.draw.rect(screen, (255, 190, 94), (977, 57, progress_width, 8), border_radius=4)
    unlocked_label = small_font.render(f"NEW: {unlocked_target.upper()}", True, (255, 211, 135))
    screen.blit(unlocked_label, (977, 77))

    time_label = small_font.render("TIME", True, (162, 184, 209))
    time_value = hud_font.render(f"{int(elapsed // 60):02d}:{int(elapsed % 60):02d}", True, (255, 255, 255))
    screen.blit(time_label, (width - 166, 30))
    screen.blit(time_value, (width - 166, 56))

    hint = small_font.render("CLICK TO POP  •  SPACE: MEGA BLAST", True, (194, 214, 230))
    screen.blit(hint, hint.get_rect(center=(width // 2, 682)))


def draw_crosshair(screen):
    x, y = pygame.mouse.get_pos()
    color = (247, 252, 255)
    pygame.draw.circle(screen, (22, 38, 60), (x, y), 13, 3)
    pygame.draw.circle(screen, color, (x, y), 11, 1)
    pygame.draw.line(screen, color, (x - 18, y), (x - 6, y), 2)
    pygame.draw.line(screen, color, (x + 6, y), (x + 18, y), 2)
    pygame.draw.line(screen, color, (x, y - 18), (x, y - 6), 2)
    pygame.draw.line(screen, color, (x, y + 6), (x, y + 18), 2)
