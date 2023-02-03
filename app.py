import pygame
import math

WIDTH, HEIGHT = 800, 600

FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CANNON_COLOR = WHITE
CANNON_RADIUS = 50
CANNON_WIDTH = 20
CANNON_HEIGHT = 80

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Tiro de Cañón")


class Cannon:
    COLOR = CANNON_COLOR
    RADIUS = CANNON_RADIUS
    WIDTH = CANNON_WIDTH
    HEIGHT = CANNON_HEIGHT

    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def draw(self, screen):
        center = (self.x, self.y)
        pygame.draw.circle(screen, self.COLOR, center, self.RADIUS)
        end = (self.x + self.HEIGHT * math.cos(self.angle),
               self.y + self.HEIGHT * math.sin(self.angle))
        pygame.draw.line(screen, self.COLOR, center, end, self.WIDTH)

    def move(self, angle):
        self.angle = angle


def draw(screen, cannon):
    screen.fill(BLACK)
    cannon.draw(screen)
    pygame.display.flip()


def handle_movement(cannon):
    pos = pygame.mouse.get_pos()
    angle = math.atan2(pos[1] - cannon.y, pos[0] - cannon.x)
    cannon.move(angle)


def main():
    running = True
    clock = pygame.time.Clock()

    cannon = Cannon(WIDTH // 2, HEIGHT, 3 * math.pi / 2)

    while running:
        clock.tick(FPS)

        draw(screen, cannon)

        handle_movement(cannon)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

    pygame.quit()


if __name__ == "__main__":
    main()
