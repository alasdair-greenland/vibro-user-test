import os
import pygame
import time

# To prevent audio issues because for some reason they were happening
os.environ["SDL_AUDIODRIVER"] = "dummy"
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Emoji Gesture Writer")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

emoji_font_path = "/System/Library/Fonts/Apple Color Emoji.ttc"
if os.path.exists(emoji_font_path):
    base_font = pygame.font.Font(emoji_font_path, 90) 
else:
    base_font = pygame.font.SysFont(None, 90)

running = True
mouse_down_pos = None
last_click_time = 0
SWIPE_THRESHOLD = 50
DOUBLE_CLICK_THRESHOLD = 0.35
LONG_CLICK_THRESHOLD = 0.7

lines = [[]] 
line_y = 100
emoji_scale = 0.3 

def make_emoji_surface(char):
    """Render and resize emoji"""
    surf = base_font.render(char, True, BLACK)
    w, h = surf.get_size()
    scaled = pygame.transform.smoothscale(surf, (int(w * emoji_scale), int(h * emoji_scale)))
    return scaled

def add_emoji(emoji):
    lines[-1].append(make_emoji_surface(emoji))

def next_line():
    lines.append([])

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                next_line()
                print("Newline triggered (right-click)")
                continue

            mouse_down_pos = event.pos
            press_time = time.time()

            if press_time - last_click_time <= DOUBLE_CLICK_THRESHOLD:
                add_emoji("👍")
                print("Double click = 👍")

            last_click_time = press_time

        elif event.type == pygame.MOUSEBUTTONUP:
            release_time = time.time()
            hold_time = release_time - last_click_time

            if mouse_down_pos:
                dx = event.pos[0] - mouse_down_pos[0]
                dy = event.pos[1] - mouse_down_pos[1]
                abs_dx, abs_dy = abs(dx), abs(dy)

                if hold_time > LONG_CLICK_THRESHOLD:
                    add_emoji("❤️")
                    print("Long click = ❤️")

                elif abs_dx > SWIPE_THRESHOLD or abs_dy > SWIPE_THRESHOLD:
                    if abs_dx > abs_dy:
                        if dx > 0:
                            add_emoji("😆") 
                            print("Swipe right = haha 😆")
                        else:
                            add_emoji("😥")
                            print("Swipe left = cry 😥")
                    else:
                        if dy > 0:
                            add_emoji("😡")
                            print("Swipe down = angry 😡")
                        else:
                            add_emoji("😊")
                            print("Swipe up = yay 😊")

                mouse_down_pos = None

    y = line_y
    for line in lines:
        x = 30
        for emoji_surf in line:
            screen.blit(emoji_surf, (x, y))
            x += emoji_surf.get_width() + 8 
        y += 75  # line spacing

    pygame.display.flip()

pygame.quit()
