import pygame, sys, random, time
from pygame.locals import *
import spritesheet
from collections import deque
pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 650
GRID_SIZE = 60  # Kích thước ô lưới
COUNT = 0
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Run and Run')
# image 
sprite = pygame.image.load('DinoSprites - tard.png').convert_alpha()
start = pygame.image.load('start_.png').convert_alpha()
exit = pygame.image.load('exit_.png').convert_alpha()
youwin = pygame.image.load('youwin.jpg').convert_alpha()
barrier = pygame.image.load('tile_0122.png').convert_alpha()
bottom = pygame.image.load('tile_0022.png').convert_alpha()
game_over = pygame.image.load('game_over..png').convert_alpha()

sprite_sheet_image = pygame.image.load('DinoSprites - tard.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
# color
BG = (50, 50, 50)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)


x_position = random.randint(0, 5) * GRID_SIZE
y_position = random.randint(5, 9) * GRID_SIZE

x_start = x_position
y_start = y_position

x_exit = random.randint(5, 9) * GRID_SIZE
y_exit = random.randint(0, 5) * GRID_SIZE
move_speed = 60  # Điều chỉnh tốc độ di chuyển để khớp với kích thước ô lưới
# Vị trí điểm  exit
exit_position = (x_exit, y_exit)
# Create animation list
animation_list = []
animation_steps = [4, 6, 3, 4]
action = 1
last_update = pygame.time.get_ticks()
animation_cooldown = 100  # speed animation
frame = 0
step_counter = 0

for animation in animation_steps:
    temp_img_list = []
    for _ in range(animation):
        temp_img_list.append(sprite_sheet.get_image(step_counter, 24, 24, 3, BLACK))
        step_counter += 1
    animation_list.append(temp_img_list)
clock = pygame.time.Clock()
# list barrier
list_x = []
list_y = []
for i in range(0, 20):
    list_x.append(random.randint(0, 10) * GRID_SIZE)
    list_y.append(random.randint(0, 10) * GRID_SIZE)
# thuật toán BFS
def bfs(start_pos, exit_pos, grid_size):
    visited = set()
    queue = deque()
    queue.appendleft((start_pos, 0))  # Bắt đầu từ vị trí nhân vật và bước đi là 0

    while queue:
        current_pos, steps = queue.popleft()
        x, y = current_pos

        if current_pos == exit_pos:
            return int(steps/60)

        # Lấy các vị trí kề
        neighbors = [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1)
        ]

        for neighbor in neighbors:
            if neighbor not in visited and 0 <= neighbor[0] < SCREEN_WIDTH and 0 <= neighbor[1] < SCREEN_HEIGHT:
                queue.append((neighbor, steps + 1))
                visited.add(neighbor)
    return -1  # Không tìm thấy đường đi
    
# Tìm đường đi ngắn nhất từ vị trí hiện tại đến điểm exit
steps_to_exit_bfs = bfs((x_start,y_start), (x_exit,y_exit), 60)
# font 
font = pygame.font.Font(None, 36)

while True:
    screen.fill(WHITE)
    
    # Vẽ lưới
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y))
    # Vẽ start và exit
    start_scaled = pygame.transform.scale(start, (GRID_SIZE, GRID_SIZE))
    screen.blit(start_scaled, (x_start, y_start))
    exit_scaled = pygame.transform.scale(exit, (GRID_SIZE, GRID_SIZE))
    screen.blit(exit_scaled, (x_exit, y_exit))
    # Vẽ barrier
    for i in range(0, 20):
        if (list_x[i], list_y[i]) != (x_start,y_start) and (list_x[i], list_y[i]) != (x_exit, y_exit):
            barrier_scaled = pygame.transform.scale(barrier, (GRID_SIZE, GRID_SIZE))
            screen.blit(barrier_scaled, (list_x[i], list_y[i]))
            
    # vẽ khung dưới
    for _ in range(0, 10):
        bottoms  = pygame.transform.scale(bottom, (GRID_SIZE, GRID_SIZE))
        screen.blit(bottoms , (_*60, 600))
    # update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list[action]):
            frame = 0

    # show frame image
    screen.blit(animation_list[action][frame], (x_position, y_position))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:  # Check for key press
    # Tạm thời lưu vị trí cũ của nhân vật
            old_x_position = x_position
            old_y_position = y_position
            COUNT += 1
            if event.key == K_DOWN:
                y_position += move_speed
            elif event.key == K_UP:
                y_position -= move_speed
            elif event.key == K_LEFT:
                x_position -= move_speed
            elif event.key == K_RIGHT:
                x_position += move_speed
    # Kiểm tra xem vị trí mới của nhân vật có nằm ngoài khung hay không
            if y_position < 0 or y_position >= SCREEN_HEIGHT - GRID_SIZE:
                # Nếu vị trí mới nằm ngoài khung, khôi phục vị trí cũ
                x_position = old_x_position
                y_position = old_y_position
    # Kiểm tra xem nhân vật có giao nhau với bất kỳ vật cản nào không
            for i in range(0, 20):
                if (x_position, y_position) == (list_x[i], list_y[i]) :
                    # Nếu nhân vật giao nhau với vật cản, khôi phục vị trí cũ
                    x_position = old_x_position
                    y_position = old_y_position
    # Keep player within the screen boundaries
    x_position = max(0, min(x_position, SCREEN_WIDTH - GRID_SIZE))
    y_position = max(0, min(y_position, SCREEN_HEIGHT - GRID_SIZE))
    print(x_position, y_position)
    # In số bước đi ngắn nhất
    if steps_to_exit_bfs != -1:
        shortest_steps_text = font.render("BFS GO: {}".format(steps_to_exit_bfs), True, BLACK)
        screen.blit(shortest_steps_text, (10, 10))
        
    # In số bước đi
    current_steps_text = font.render("YOU GO: {}".format(COUNT), True, BLACK)
    screen.blit(current_steps_text, (10, 40))
    
    # Kiểm tra nếu nhân vật đến điểm exit
    if (x_position, y_position) == exit_position:
        screen.fill(WHITE)
        screen.blit(youwin, (0, 0))
        pygame.display.update()
        pygame.time.delay(2000)  # Đợi 2 giây trước khi thoát game
        pygame.quit()
        sys.exit()
    # kiểm tra số bước đi nếu mà nhiều hơn số bước đi ngắn nhất thì thua
    if COUNT == steps_to_exit_bfs + 1:
        screen.fill(WHITE)
        screen.blit(game_over, (170, 250))
        pygame.display.update()
        pygame.time.delay(2000)  # Đợi 2 giây trước khi thoát game
        pygame.quit()
        sys.exit()
    pygame.display.update()
    clock.tick(60)
    

