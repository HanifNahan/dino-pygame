import pygame

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 720, 480
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

BLACK, WHITE = (0, 0, 0), (255, 255, 255)
GRAVITY, SPEED, JUMP_SPEED = 0.5, 5, 10

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

platform = Platform(0, WINDOW_HEIGHT - 50, WINDOW_WIDTH, 50)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = []
        for i in range(1, 5):
            image = pygame.image.load(f'assets/walk_{i}.png').convert_alpha()
            image = pygame.transform.scale(image, (100, 100))
            self.images.append(image)
        self.jump_image = pygame.image.load('assets/jump.png').convert_alpha()
        self.jump_image = pygame.transform.scale(self.jump_image, (100, 100))
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
        if self.rect.y + 80 >= platform.rect.y:
            self.rect.y = platform.rect.y - 80 - 1
            self.change[1] = 0
        if self.rect.y < 0:
            self.rect.y = 0
            self.change[1] = 0
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x + 50 >= WINDOW_WIDTH:
            self.rect.x = WINDOW_WIDTH - 50
        if self.rect.y > 345:
            self.is_grounded = True
            self.is_jumping = False
        if self.is_jumping:
            self.image = self.jump_image
        else:
            self.run()

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

    screen.fill(BLACK)
    player.update()
    platform.draw(screen)
    player.draw(screen)
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()


