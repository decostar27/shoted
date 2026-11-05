import math
import random
import struct

import pygame

from balloon_anim import BalloonField, TARGETS_BY_LEVEL
from gui import draw_background, draw_crosshair, draw_hud


WIDTH = 1280
HEIGHT = 720
MAX_MISSES = 8
POPS_PER_MEGA = 10
SAMPLE_RATE = 22050


def create_pop_sound():
    duration = 0.13
    sample_count = int(SAMPLE_RATE * duration)
    samples = bytearray(sample_count * 2)
    noise = random.Random(7)

    for index in range(sample_count):
        time = index / SAMPLE_RATE
        progress = time / duration
        frequency = 900 - 520 * progress
        envelope = (1 - progress) ** 2
        tone = math.sin(2 * math.pi * frequency * time) * 0.55
        value = int((tone + noise.uniform(-0.45, 0.45)) * envelope * 15000)
        struct.pack_into("<h", samples, index * 2, max(-32768, min(32767, value)))

    return pygame.mixer.Sound(buffer=samples)


def main():
    pygame.mixer.pre_init(SAMPLE_RATE, -16, 1, 512)
    pygame.init()
    pygame.display.set_caption("SHOTED | Balloon Pop")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    pop_sound = None
    if pygame.mixer.get_init() is None:
        try:
            pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1, buffer=512)
        except pygame.error as error:
            print(f"Audio is unavailable; continuing without sound: {error}")
    if pygame.mixer.get_init() is not None:
        pop_sound = create_pop_sound()

    title_font = pygame.font.SysFont("arial", 44, bold=True)
    hud_font = pygame.font.SysFont("arial", 22, bold=True)
    small_font = pygame.font.SysFont("arial", 16)

    background = draw_background(WIDTH, HEIGHT)
    field = BalloonField(WIDTH, HEIGHT)
    score = 0
    level = 1
    pops_toward_mega = 0
    mega_charges = 0
    misses = 0
    running = True
    elapsed = 0.0
    spawn_timer = 0.0
    game_over = False

    def award_pops(count):
        nonlocal score, pops_toward_mega, mega_charges
        score += count
        pops_toward_mega += count
        while pops_toward_mega >= POPS_PER_MEGA:
            pops_toward_mega -= POPS_PER_MEGA
            mega_charges += 1

    pygame.mouse.set_visible(False)

    while running:
        delta_time = min(clock.tick(60) / 1000.0, 0.05)
        elapsed += delta_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r and game_over:
                    field.reset()
                    score = 0
                    level = 1
                    pops_toward_mega = 0
                    mega_charges = 0
                    misses = 0
                    elapsed = 0.0
                    spawn_timer = 0.0
                    game_over = False
                elif event.key == pygame.K_SPACE and not game_over and mega_charges > 0:
                    popped = field.pop_all()
                    if popped:
                        mega_charges -= 1
                        award_pops(popped)
                        if pop_sound is not None:
                            pop_sound.play()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
                if field.pop_at(event.pos):
                    award_pops(1)
                    if pop_sound is not None:
                        pop_sound.play()

        if not game_over:
            level = min(score // 10 + 1, len(TARGETS_BY_LEVEL))
            field.set_level(level)
            spawn_timer += delta_time
            spawn_interval = max(0.4, 0.9 - (level - 1) * 0.045)
            while spawn_timer >= spawn_interval:
                field.spawn()
                spawn_timer -= spawn_interval

            misses += field.update(delta_time)
            if misses >= MAX_MISSES:
                game_over = True

        screen.blit(background, (0, 0))
        field.draw(screen)
        draw_hud(
            screen,
            score,
            misses,
            MAX_MISSES,
            elapsed,
            title_font,
            hud_font,
            small_font,
            pops_toward_mega,
            mega_charges,
            level,
            min(score % 10, 10) if level < len(TARGETS_BY_LEVEL) else min(max(score - 90, 0), 10),
            TARGETS_BY_LEVEL[level - 1],
        )

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((8, 15, 35, 185))
            screen.blit(overlay, (0, 0))

            panel = pygame.Rect(0, 0, 430, 250)
            panel.center = (WIDTH // 2, HEIGHT // 2)
            pygame.draw.rect(screen, (24, 37, 68), panel, border_radius=24)
            pygame.draw.rect(screen, (87, 205, 235), panel, width=2, border_radius=24)
            heading = title_font.render("ROUND OVER", True, (255, 255, 255))
            result = hud_font.render(f"Final score  {score}", True, (115, 231, 220))
            prompt = small_font.render("Press R to play again  •  Esc to quit", True, (196, 209, 229))
            screen.blit(heading, heading.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 48)))
            screen.blit(result, result.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 8)))
            screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 65)))

        draw_crosshair(screen)
        pygame.display.flip()

    pygame.mouse.set_visible(True)
    pygame.quit()


if __name__ == "__main__":
    main()
