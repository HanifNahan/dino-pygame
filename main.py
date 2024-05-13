import pygame
import time
import random

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 720, 480
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

LIGHT_BLUE, WHITE = (135, 206, 250), (255, 255, 255)
GRAVITY, SPEED, JUMP_SPEED = 0.4, 5, 10
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 50
PLATFORM_WIDTH, PLATFORM_HEIGHT = 720, 50
spawn_time = time.time()
MIN_SPAWN_INTERVAL = 1.0
MAX_SPAWN_INTERVAL = 20.0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([OBSTACLE_WIDTH, OBSTACLE_HEIGHT])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(
            topleft=(random.randint(WINDOW_WIDTH, WINDOW_WIDTH + OBSTACLE_WIDTH),
                     WINDOW_HEIGHT - PLATFORM_HEIGHT - OBSTACLE_HEIGHT))
        self.change = [-4, 0]

    def update(self):
        self.rect.x += self.change[0]
        if self.rect.x + OBSTACLE_WIDTH <= 0:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

platform = Platform(0, WINDOW_HEIGHT - 50, WINDOW_WIDTH, 50)
obstacles = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = []
        for i in range(1, 5):
            image = pygame.image.load(f'assets/walk_{i}.png').convert_alpha()
            orig_width, orig_height = image.get_size()
            new_width = orig_width * 150 // orig_height
            image = pygame.transform.scale(image, (new_width, 150))
            self.images.append(image)
        self.jump_image = pygame.image.load('assets/jump.png').convert_alpha()
        orig_width, orig_height = self.jump_image.get_size()
        new_width = orig_width * 150 // orig_height
        self.jump_image = pygame.transform.scale(self.jump_image, (new_width, 150))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(100, 100))
        self.change = [0, 0]
        self.fps = 10
        self.clock = pygame.time.Clock()
        self.is_grounded = False
        self.is_jumping = False

    def update(self):
        self.rect.x += self.change[0]
        self.change[1] += GRAVITY
        self.rect.y += self.change[1]
        if self.rect.y + 120 >= platform.rect.y:
            self.rect.y = platform.rect.y - 120 - 1
            self.change[1] = 0
        if self.rect.y < 0:
            self.rect.y = 0
            self.change[1] = 0
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x + 50 >= WINDOW_WIDTH:
            self.rect.x = WINDOW_WIDTH - 50
        if self.rect.y > 305:
            self.is_grounded = True
            self.is_jumping = False
        if self.is_jumping:
            self.image = self.jump_image
        else:
            self.run()

        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                self.is_grounded = False

    def run(self):
        now = pygame.time.get_ticks()
        if now - self.clock.get_time() > self.fps:
            self.clock.tick()
            self.index += 0.2
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[int(self.index)]

    def jump(self):
        self.is_jumping = True
        self.change[1] = -JUMP_SPEED

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def handle_key_press(self, key):
        if key == pygame.K_LEFT:
            self.change[0] = -SPEED
        elif key == pygame.K_RIGHT:
            self.change[0] = SPEED
        elif key == pygame.K_SPACE and self.is_grounded:
            self.jump()
            self.is_grounded = False

    def handle_key_release(self, key):
        if key in (pygame.K_LEFT, pygame.K_RIGHT):
            self.change[0] = 0

player = Player()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            player.handle_key_press(event.key)
        if event.type == pygame.KEYUP:
            player.handle_key_release(event.key)

    screen.fill(LIGHT_BLUE)
    player.update()
    platform.draw(screen)
    for obstacle in obstacles:
        obstacle.update()
        obstacle.draw(screen)
    player.draw(screen)
    pygame.display.flip()
    pygame.time.Clock().tick(60)
    if len(obstacles) < 10 and time.time() - spawn_time > random.uniform(MIN_SPAWN_INTERVAL, MAX_SPAWN_INTERVAL):
        spawn_time = time.time()
        obstacles.add(Obstacle())

pygame.quit()


