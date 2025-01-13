import pygame  
import random  

pygame.init()  

SCREEN_WIDTH = 1008  
SCREEN_HEIGHT = 567  
CELL_SIZE = 15  
MAZE_HEIGHT = (SCREEN_HEIGHT - 40) // CELL_SIZE  

WHITE = (255, 255, 255)  
BLACK = (0, 0, 0)  
MAZE_WALL_COLOR = (0, 102, 204)  
BOOST_COLOR = (0, 255, 255)
PLAYER_COLOR = (255, 20, 0)
END_POSITION_COLOR = (255, 215, 0)
BACKGROUND_COLOR = (20, 20, 20) 


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  
pygame.display.set_caption("m4ze m4r4th0n")  
clock = pygame.time.Clock()  
font = pygame.font.SysFont(None, 36)  
large_font = pygame.font.SysFont(None, 72)  


def generate_maze(width, height):  
    maze = [[1 for _ in range(width)] for _ in range(height)]  

    def carve_passages(x, y):  
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  
        random.shuffle(directions)  
        for dx, dy in directions:  
            nx, ny = x + dx, y + dy  
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:  
                if sum(maze[ny + dy][nx + dx] for dx, dy in directions if 0 <= nx + dx < width and 0 <= ny + dy < height) >= 2:  
                    maze[y][x] = 0  
                    maze[ny][nx] = 0  
                    carve_passages(nx, ny)  

    carve_passages(0, 0)  
    return maze  

def place_special_blocks(maze, width, height):  
    for y in range(height):  
        for x in range(width):  
            if maze[y][x] == 0:   
                if random.random() < 0.05:  
                    maze[y][x] = 'dark_red'  
                elif random.random() < 0.1:  
                    maze[y][x] = 'boost'  
    return maze  



def show_start_screen():  
    screen.fill(BACKGROUND_COLOR)  
    title_text = large_font.render("m4ze m4r4th0n", True, WHITE)  
    instruction_text = font.render("more the time you use, more the points you lose.", True, WHITE)  
    challenge_text = font.render("Developer'sChallenge_SCORE 500 POINTS,,,,,,for a surprise at the end", True, WHITE)  
    start_button_text = font.render("Press ENTER to Start", True, WHITE)  

    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))  
    screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))  
    screen.blit(challenge_text, (SCREEN_WIDTH // 2 - challenge_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))  
    screen.blit(start_button_text, (SCREEN_WIDTH // 2 - start_button_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))  

    pygame.display.flip()  



def game_start():  
    show_start_screen()
    waiting = True  
    while waiting:  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                pygame.quit()  
                quit()  
            elif event.type == pygame.KEYDOWN:  
                if event.key == pygame.K_RETURN:
                    return True  



def reset_game():  
    maze = generate_maze(maze_width, maze_height)  
    maze = place_special_blocks(maze, maze_width, maze_height)  
    
    maze[maze_height - 1][maze_width - 1] = 0  
    return maze  

maze_width = SCREEN_WIDTH // CELL_SIZE  
maze_height = MAZE_HEIGHT 
maze = reset_game()  
player_pos = [0, 0]  
end_pos = [maze_width - 1, maze_height - 1]  
score = 0  

start_time = pygame.time.get_ticks()    
elapsed_time = 0 
last_time_checked = 0
running = False  

if game_start():  
    running = True  

while running:  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            running = False  
        elif event.type == pygame.KEYDOWN:  
            x, y = player_pos  
            if event.key == pygame.K_UP and y > 0 and maze[y - 1][x] != 1:  
                player_pos[1] -= 1  
            elif event.key == pygame.K_DOWN and y < maze_height - 1 and maze[y + 1][x] != 1:  
                player_pos[1] += 1  
            elif event.key == pygame.K_LEFT and x > 0 and maze[y][x - 1] != 1:  
                player_pos[0] -= 1  
            elif event.key == pygame.K_RIGHT and x < maze_width - 1 and maze[y][x + 1] != 1:  
                player_pos[0] += 1  

    if player_pos == end_pos:  
        screen.fill(BLACK)  

        victory_text = font.render("You Win!", True, END_POSITION_COLOR)  
        time_text = font.render(f"Time: {int(elapsed_time)}s", True, WHITE)  
        score_text = font.render(f"Score: {score}", True, WHITE)  

        if score == 500:  
            special_message = font.render("aura ∞", True, WHITE)  
            screen.blit(special_message, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 60))  

        screen.blit(victory_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 20))  
        screen.blit(time_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 20))  
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 100))  
        pygame.display.flip()  
        pygame.time.delay(3000)  
        running = False  

    x, y = player_pos  
    if maze[y][x] == 'dark_red':  
        score -= 100  
        maze[y][x] = 0  
    elif maze[y][x] == 'boost':  
        score += 50  
        maze[y][x] = 0  

    current_time = pygame.time.get_ticks()  
    elapsed_time = (current_time - start_time) / 1000  

    if int(elapsed_time) > last_time_checked:  
        score -= 20  
        last_time_checked = int(elapsed_time)  

    screen.fill(BACKGROUND_COLOR)  
    pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, 40))  
    timer_text = font.render(f"Time: {int(elapsed_time)}s", True, BLACK)  
    score_text = font.render(f"Score: {score}", True, BLACK)  
    screen.blit(timer_text, (10, 10))  
    screen.blit(score_text, (SCREEN_WIDTH - 150, 10))  



  
    for y in range(maze_height):  
        for x in range(maze_width):  
            if maze[y][x] == 1:  
                color = MAZE_WALL_COLOR  
            elif maze[y][x] == 'dark_red':  
                color = (255, 105, 180)  
            elif maze[y][x] == 'boost':  
                color = BOOST_COLOR  
            else:  
                color = BLACK  
            pygame.draw.rect(screen, color,   
                             (x * CELL_SIZE, y * CELL_SIZE + 40, CELL_SIZE, CELL_SIZE))  

    pygame.draw.rect(screen, PLAYER_COLOR,   
                     (player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE + 40, CELL_SIZE, CELL_SIZE))  

    pygame.draw.rect(screen, END_POSITION_COLOR,   
                     (end_pos[0] * CELL_SIZE, end_pos[1] * CELL_SIZE + 40, CELL_SIZE, CELL_SIZE))  

    pygame.display.flip()  

    clock.tick(60)  

pygame.quit()
