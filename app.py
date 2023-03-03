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

BLOCK_COLOR = WHITE
BLOCK_HEIGHT = 40
BLOCK_GAP = 30
BLOCK_COUNT = (10, 5)

TEXT_HEIGHT = 60

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Tiro de Cañón")

font = pygame.font.SysFont("Arial", TEXT_HEIGHT // 2)


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
        elif next_y + self.RADIUS > HEIGHT:
            return True
        else:
            self.VELOCITY_Y *= -1

        self.center = (self.x, self.y)


class Block:
    COLOR = BLOCK_COLOR
    HEIGHT = BLOCK_HEIGHT

    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width

    def draw(self, screen):
        rect = (self.x, self.y, self.width, self.HEIGHT)
        pygame.draw.rect(screen, self.COLOR, rect)


def draw(screen, cannon, balls, text, blocks):
    screen.fill(BLACK)

    cannon.draw(screen)

    for ball in balls:
        ball.draw(screen)

    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, TEXT_HEIGHT // 2)

    screen.blit(text, text_rect)

    for block in blocks:
        block.draw(screen)

    pygame.display.flip()


def handle_movement(cannon, balls, blocks):
    pos = pygame.mouse.get_pos()
    angle = math.atan2(pos[1] - cannon.y, pos[0] - cannon.x)

    cannon.move(angle)

    balls_to_remove = []

    for ball in balls:
        if ball.move():
            balls_to_remove.append(ball)

    for ball in balls_to_remove:
        balls.remove(ball)

    handle_block_collisions(balls, blocks)


def handle_shoot(cannon, balls):
    ball = cannon.shoot()

    if ball:
        balls.append(ball)


def handle_block_collisions(balls, blocks):
    blocks_to_remove = []

    for ball in balls:
        for block in blocks:
            if ball.center[1] - ball.RADIUS <= block.y + block.HEIGHT and \
               ball.center[1] + ball.RADIUS >= block.y and \
               ball.center[0] - ball.RADIUS <= block.x + block.width and \
               ball.center[0] + ball.RADIUS >= block.x:
                blocks_to_remove.append(block)
                if ball.center[0] < block.x or ball.center[0] > block.x + block.width:
                    ball.VELOCITY_X *= -1
                else:
                    ball.VELOCITY_Y *= -1

    for block in blocks_to_remove:
        blocks.remove(block)


def main():
    running = True

    clock = pygame.time.Clock()

    cannon = Cannon(WIDTH // 2, HEIGHT, 3 * math.pi / 2)

    balls = []

    pressed = False

    blocks = []

    block_width = (WIDTH - BLOCK_GAP * (BLOCK_COUNT[0] + 1)) // BLOCK_COUNT[0]

    start_x = BLOCK_GAP
    step_x = block_width + BLOCK_GAP
    end_x = start_x + BLOCK_COUNT[0] * step_x

    start_y = BLOCK_GAP + TEXT_HEIGHT
    step_y = BLOCK_HEIGHT + BLOCK_GAP
    end_y = start_y + BLOCK_COUNT[1] * step_y

    for i in range(start_x, end_x, step_x):
        for j in range(start_y, end_y, step_y):
            blocks.append(Block(i, j, block_width))

    while running:
        clock.tick(FPS)

        text = font.render(f"Balls: {cannon.BALLS}", True, WHITE)

        draw(screen, cannon, balls, text, blocks)

        handle_movement(cannon, balls, blocks)

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
