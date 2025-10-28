import os
import pygame
import time

# To prevent audio issues because for some reason they were happening
# Swipe based version of touchpad-stuff.py...I.e First version

os.environ["SDL_AUDIODRIVER"] = "dummy"
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Emoji Gesture Writer - Swipe Series")

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

trial_data = []
start_time = time.time()
last_input_time = start_time
inputs_in_line = 0
line_start_time = start_time

def make_emoji_surface(char):
    """Render and resize emoji"""
    surf = base_font.render(char, True, BLACK)
    w, h = surf.get_size()
    scaled = pygame.transform.smoothscale(
        surf, (int(w * emoji_scale), int(h * emoji_scale))
    )
    return scaled


def add_emoji(emoji):
    """Add emoji to display and log timing"""
    global last_input_time, inputs_in_line
    lines[-1].append(make_emoji_surface(emoji))
    current_time = time.time()
    delta = current_time - last_input_time
    total_since_start = current_time - start_time
    trial_data.append(
        {
            "emoji": emoji,
            "timestamp": round(current_time, 3),
            "delta_since_last": round(delta, 3),
            "total_elapsed": round(total_since_start, 3),
            "line_number": len(lines),
        }
    )
    print(
        f"Emoji: {emoji} | since last: {delta:.3f}s | Total elapsed: {total_since_start:.3f}s | Line {len(lines)}"
    )
    last_input_time = current_time
    inputs_in_line += 1


def next_line():
    """Start a new line, record total time for previous one"""
    global inputs_in_line, line_start_time
    current_time = time.time()
    line_duration = current_time - line_start_time
    if inputs_in_line > 0:
        print(
            f"--- Line {len(lines)} completed in {line_duration:.3f}s ({inputs_in_line} inputs) ---"
        )
        trial_data.append(
            {
                "emoji": "<LINE_SUBMIT>",
                "timestamp": round(current_time, 3),
                "line_duration": round(line_duration, 3),
                "inputs": inputs_in_line,
            }
        )
    lines.append([])
    inputs_in_line = 0
    line_start_time = time.time()

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
                            add_emoji("😊")
                            print("Swipe left = yay 😊")
                    else:
                        if dy > 0:
                            add_emoji("😡")
                            print("Swipe down = angry 😡")
                        else:
                            add_emoji("😥")
                            print("Swipe up = cry 😥")

                mouse_down_pos = None

    y = line_y
    for line in lines:
        x = 30
        for emoji_surf in line:
            screen.blit(emoji_surf, (x, y))
            x += emoji_surf.get_width() + 8
        y += 75

    pygame.display.flip()

pygame.quit()

print("\n===== SESSION SUMMARY =====")
for entry in trial_data:
    print(entry)
print("============================")
