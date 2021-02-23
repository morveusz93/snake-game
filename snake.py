import pygame
import random

pygame.init()
pygame.mixer.init()
width = 750
fps = 20
game_clock = pygame.time.Clock()

pygame.display.set_caption("Snake by Morvy")
screen = pygame.display.set_mode((width, width))
screen.fill((30,30,30)) # color of background
red = (255,0,0)  # color of snake

my_font = pygame.font.SysFont('georgia', 30)
points_font = pygame.font.SysFont('opensans', 25)

block = width//50

def draw_food(food_x, food_y):
        pygame.draw.rect(screen, (245, 66, 194), (food_x, food_y, block, block))
    

def print_points(points):
    points_msg = ("Points: {}" .format(points))
    p = points_font.render(points_msg, True, (0, 0, 255))
    screen.blit(p, (10, 10))


def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, red, (x[0], x[1], block, block))


def print_mess(mess):
    msg = my_font.render(mess, True, (0, 255, 0))
    screen.blit(msg, (width//2 - msg.get_width()//2, width//2 - msg.get_height()//2))


def main():
    snake_list = []
    snake_len = 1
    x, y = (width//block//2, width//block//2) # picking start 
    x *=block
    y *=block
    change_x = block # when you start -> go right
    change_y = 0
    direction = 'right'
    play = True
    lost = False
    points = 0
    food_x = random.randint(1, width//block-1) * block  # create first food
    food_y = random.randint(1, width//block-1) * block
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('menu_music.mp3'), -1)

    while play:
        while lost:
            print_mess("You LOST!!! Press [Q]-Quit or [A]-Again")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                    lost = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        x, y = (width//block//2, width//block//2) 
                        x *=block
                        y *=block   # reset all
                        change_x = block
                        change_y = 0
                        direction = 'right'
                        food_x = random.randint(1, width//block -1) * block
                        food_y = random.randint(1, width//block -1) * block
                        snake_len = 1
                        snake_list = []
                        points = 0
                        lost = False
                    if event.key == pygame.K_q:
                        play = False
                        lost = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != 'right':
                    change_x = -block
                    change_y = 0
                    direction = 'left'
                elif event.key == pygame.K_RIGHT and direction != 'left':
                    change_x = block
                    change_y = 0
                    direction = 'right'
                elif event.key == pygame.K_UP and direction != 'down':
                    change_x = 0
                    change_y = -block
                    direction = 'up'
                elif event.key == pygame.K_DOWN and direction != 'up':
                    change_x = 0
                    change_y = block
                    direction = 'down'
        x += change_x 
        y += change_y
        if [x,y] in snake_list: # if you bit yourself
            lost = True
        snake_list.append([x, y])
        if x == food_x and y == food_y:  # when you eat
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('eating.mp3'))
            snake_len += 1
            points += 10
            food_x = random.randint(1, width//block-1) * block
            food_y = random.randint(1, width//block-1) * block
        if len(snake_list) > snake_len:
            snake_list.pop(0)
        if x <= 0 or x >= width - block: # when you go out the window
            lost = True
        if y <= 0 or y >= width - block:
            lost = True
        if lost == True:
            pygame.mixer.Channel(2).play(pygame.mixer.Sound('die.mp3'))
        screen.fill((30,30,30))
        draw_snake(snake_list)
        draw_food(food_x, food_y)
        print_points(points)
        pygame.display.update()
        game_clock.tick(fps)
    pygame.quit()

main()
