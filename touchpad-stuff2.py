import os
import pygame
import time
#Click based version of touchpad-stuff.py...I.e second version
# To prevent audio issues because for some reason they were happening
os.environ["SDL_AUDIODRIVER"] = "dummy"
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Emoji Gesture Writer — Click Series")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

emoji_font_path = "/System/Library/Fonts/Apple Color Emoji.ttc"
if os.path.exists(emoji_font_path):
    base_font = pygame.font.Font(emoji_font_path, 90)
else:
    base_font = pygame.font.SysFont(None, 90)

emoji_scale = 0.3

def make_emoji_surface(char):
    surf = base_font.render(char, True, BLACK)
    w, h = surf.get_size()
    return pygame.transform.smoothscale(surf, (int(w * emoji_scale), int(h * emoji_scale)))

running = True
lines = [[]]
line_y = 100
last_click_time = 0
DOUBLE_CLICK_THRESHOLD = 0.35

def add_emoji(emoji):
    lines[-1].append(make_emoji_surface(emoji))

def next_line():
    lines.append([])

def get_quadrant(pos, width, height):
    x, y = pos
    top = y < height / 2
    left = x < width / 2
    if top and left:
        return "top_left"
    elif top and not left:
        return "top_right"
    elif not top and left:
        return "bottom_left"
    else:
        return "bottom_right"

while running:
    screen.fill(WHITE)
    w, h = screen.get_size()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_time = time.time()
            quadrant = get_quadrant(event.pos, w, h)

            if event.button == 3:
                if "top" in quadrant:
                    add_emoji("👍")
                    print("Right-click top = like 👍")
                else:
                    add_emoji("❤️")
                    print("Right-click bottom = heart ❤️")
                continue

            if event.button == 1: 
                if click_time - last_click_time <= DOUBLE_CLICK_THRESHOLD:
                    if quadrant == "top_left":
                        add_emoji("😆")
                        print("Double top-left = haha 😆")
                    elif quadrant == "top_right":
                        add_emoji("😊")
                        print("Double top-right = yay 😊")
                    elif quadrant == "bottom_left":
                        add_emoji("😥")
                        print("Double bottom-left = cry 😥")
                    elif quadrant == "bottom_right":
                        add_emoji("😡")
                        print("Double bottom-right = angry 😡")
                last_click_time = click_time

    y = line_y
    for line in lines:
        x = 50
        for e in line:
            screen.blit(e, (x, y))
            x += e.get_width() + 8
        y += 75

    pygame.display.flip()

pygame.quit()
