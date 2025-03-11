import pygame
import random
import sys
print(sys.path)
    
pygame.init()
WIDTH, HEIGHT = 500, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

snake = [(100, 100)]
direction = (20, 0)
food = (random.randint(0, 24) * 20, random.randint(0, 24) * 20)

running = True
while running:
    win.fill((0, 0, 0))
    pygame.draw.rect(win, (255, 0, 0), (*food, 20, 20))
    for part in snake:
        pygame.draw.rect(win, (0, 255, 0), (*part, 20, 20))

    pygame.display.update()
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]: direction = (0, -20)
    if keys[pygame.K_DOWN]: direction = (0, 20)
    if keys[pygame.K_LEFT]: direction = (-20, 0)
    if keys[pygame.K_RIGHT]: direction = (20, 0)

    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    if new_head == food:
        food = (random.randint(0, 24) * 20, random.randint(0, 24) * 20)
    else:
        snake.pop()

    if new_head in snake or not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
        running = False

    snake.insert(0, new_head)

pygame.quit()
