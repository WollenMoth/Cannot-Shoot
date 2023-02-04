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
CANNON_BALLS = 10

BALL_COLOR = WHITE
BALL_RADIUS = 10
BALL_VELOCITY = 5

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Tiro de Cañón")


class Cannon:
    COLOR = CANNON_COLOR
    RADIUS = CANNON_RADIUS
    WIDTH = CANNON_WIDTH
    HEIGHT = CANNON_HEIGHT
    BALLS = CANNON_BALLS

    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.center = (x, y)
        self.angle = angle
        self.end = self.get_end()

    def get_end(self):
        return (self.x + self.HEIGHT * math.cos(self.angle),
                self.y + self.HEIGHT * math.sin(self.angle))

    def draw(self, screen):
        pygame.draw.circle(screen, self.COLOR, self.center, self.RADIUS)
        pygame.draw.line(screen, self.COLOR, self.center, self.end, self.WIDTH)

    def move(self, angle):
        self.angle = angle
        self.end = self.get_end()

    def shoot(self):
        if self.BALLS:
            self.BALLS -= 1
            return Ball(*self.end, self.angle)


class Ball:
    COLOR = BALL_COLOR
    RADIUS = BALL_RADIUS
    VELOCITY_X = BALL_VELOCITY
    VELOCITY_Y = BALL_VELOCITY

    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.center = (x, y)
        self.angle = angle

    def draw(self, screen):
        pygame.draw.circle(screen, self.COLOR, self.center, self.RADIUS)

    def move(self):
        next_x = self.x + self.VELOCITY_X * math.cos(self.angle)
        next_y = self.y + self.VELOCITY_Y * math.sin(self.angle)

        if next_x - self.RADIUS > 0 and next_x + self.RADIUS < WIDTH:
            self.x = next_x
        else:
            self.VELOCITY_X *= -1

        if next_y - self.RADIUS > 0 and next_y + self.RADIUS < HEIGHT:
            self.y = next_y
        else:
            self.VELOCITY_Y *= -1

        self.center = (self.x, self.y)


def draw(screen, cannon, balls):
    screen.fill(BLACK)
    cannon.draw(screen)
    for ball in balls:
        ball.draw(screen)
    pygame.display.flip()


def handle_movement(cannon, balls):
    pos = pygame.mouse.get_pos()
    angle = math.atan2(pos[1] - cannon.y, pos[0] - cannon.x)
    cannon.move(angle)

    for ball in balls:
        ball.move()


def handle_shoot(cannon, balls):
    ball = cannon.shoot()

    if ball:
        balls.append(ball)


def main():
    running = True
    clock = pygame.time.Clock()

    cannon = Cannon(WIDTH // 2, HEIGHT, 3 * math.pi / 2)

    balls = []

    pressed = False

    while running:
        clock.tick(FPS)

        draw(screen, cannon, balls)

        handle_movement(cannon, balls)

        last_pressed = pressed
        pressed = pygame.mouse.get_pressed()[0]

        if (pressed and not last_pressed):
            handle_shoot(cannon, balls)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

    pygame.quit()


if __name__ == "__main__":
    main()
