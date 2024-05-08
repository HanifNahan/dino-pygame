import pygame

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 720, 480
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

BLACK, WHITE = (0, 0, 0), (255, 255, 255)
GRAVITY, SPEED, JUMP_SPEED = 0.5, 5, 10

platform_y = WINDOW_HEIGHT - 50

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(topleft=(100, 100))
        self.change = [0, 0]

    def update(self):
        self.rect.x += self.change[0]
        self.change[1] += GRAVITY
        self.rect.y += self.change[1]
        if self.rect.y + 50 >= platform_y:
            self.rect.y = platform_y - 50 - 1
            self.change[1] = 0
        if self.rect.y < 0:
            self.rect.y = 0
            self.change[1] = 0
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x + 50 >= WINDOW_WIDTH:
            self.rect.x = WINDOW_WIDTH - 50

    def jump(self):
        self.change[1] = -JUMP_SPEED

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def handle_key_press(self, key):
        if key == pygame.K_LEFT:
            self.change[0] = -SPEED
        elif key == pygame.K_RIGHT:
            self.change[0] = SPEED
        elif key == pygame.K_SPACE:
            self.jump()

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
    pygame.draw.rect(screen, WHITE, (0, platform_y, WINDOW_WIDTH, 50))
    player.draw(screen)
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()

