import os
import pygame
import time
# To prevent audio issues because for some reason they were happening
# Click based version of touchpad-stuff.py...I.e Second version

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
SWIPE_THRESHOLD = 100  # pixels required for a swipe

running = True
lines = [[]]
line_y = 100
last_click_time = 0
press_start_time = 0
mouse_down_pos = None
DOUBLE_CLICK_THRESHOLD = 0.35

trial_data = []
start_time = time.time()
last_input_time = start_time
line_start_time = start_time
inputs_in_line = 0

def make_emoji_surface(char):
    surf = base_font.render(char, True, BLACK)
    w, h = surf.get_size()
    return pygame.transform.smoothscale(surf, (int(w * emoji_scale), int(h * emoji_scale)))

def add_emoji(emoji):
    global last_input_time, inputs_in_line
    lines[-1].append(make_emoji_surface(emoji))
    current_time = time.time()
    delta = current_time - last_input_time
    total_since_start = current_time - start_time
    trial_data.append({
        "emoji": emoji,
        "timestamp": round(current_time, 3),
        "delta_since_last": round(delta, 3),
        "total_elapsed": round(total_since_start, 3),
        "line_number": len(lines)
    })
    print(f"Emoji: {emoji} | since last: {delta:.3f}s | Total elapsed: {total_since_start:.3f}s | Line {len(lines)}")
    last_input_time = current_time
    inputs_in_line += 1

def next_line():
    global inputs_in_line, line_start_time
    current_time = time.time()
    line_duration = current_time - line_start_time
    if inputs_in_line > 0:
        print(f"--- Line {len(lines)} completed in {line_duration:.3f}s ({inputs_in_line} inputs) ---")
        trial_data.append({
            "emoji": "<LINE_SUBMIT>",
            "timestamp": round(current_time, 3),
            "line_duration": round(line_duration, 3),
            "inputs": inputs_in_line
        })
    lines.append([])
    inputs_in_line = 0
    line_start_time = time.time()

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
            press_start_time = click_time
            mouse_down_pos = event.pos
            quadrant = get_quadrant(event.pos, w, h)
            if event.button == 3:
                if "top" in quadrant:
                    add_emoji("👍")
                    print("Right-click top = like 👍")
                else:
                    add_emoji("❤️")
                    print("Right-click bottom = heart ❤️")
                continue
            if event.button == 1 and (click_time - last_click_time <= DOUBLE_CLICK_THRESHOLD):
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
        elif event.type == pygame.MOUSEBUTTONUP:
            if mouse_down_pos:
                dx = event.pos[0] - mouse_down_pos[0]
                if dx > SWIPE_THRESHOLD:
                    next_line()
                    print("Single swipe right = newline")
                mouse_down_pos = None

    y = line_y
    for line in lines:
        x = 50
        for e in line:
            screen.blit(e, (x, y))
            x += e.get_width() + 8
        y += 75
    pygame.display.flip()

pygame.quit()

print("\n===== SESSION SUMMARY =====")
for entry in trial_data:
    print(entry)
print("============================")
