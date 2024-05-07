import pygame, time

pygame.init()

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 480
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAVITY = 0.5
SPEED = 5
JUMP_SPEED = 10

rect_x = 100
rect_y = 100
rect_change_x = 0
rect_change_y = 0

platform_y = WINDOW_HEIGHT - 50
# time.sleep(2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                rect_change_x = -SPEED
            if event.key == pygame.K_RIGHT:
                rect_change_x = SPEED
            if event.key == pygame.K_SPACE:
                rect_change_y = -JUMP_SPEED
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and rect_change_x < 0:
                rect_change_x = 0
            if event.key == pygame.K_RIGHT and rect_change_x > 0:
                rect_change_x = 0

    screen.fill(BLACK)

    rect_x += rect_change_x
    rect_y += rect_change_y
    rect_change_y += GRAVITY

    if rect_y + 50 >= platform_y:
        rect_y = platform_y - 50 - 1
        rect_change_y = 0

    if rect_y < 0:
        rect_y = 0
        rect_change_y = 0

    if rect_x < 0:
        rect_x = 0
    if rect_x + 50 >= WINDOW_WIDTH:
        rect_x = WINDOW_WIDTH - 50

    pygame.draw.rect(screen, WHITE, (rect_x, rect_y, 50, 50))
    pygame.draw.rect(screen, WHITE, (0, platform_y, WINDOW_WIDTH, 50))

    pygame.display.flip()

    clock = pygame.time.Clock()
    clock.tick(60)

pygame.quit()