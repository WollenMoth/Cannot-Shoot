"""Juego de Tiro de Cañón.

El objetivo del juego es destruir todos los bloques con las bolas que dispara el cañón.
El cañón se mueve con el puntero del mouse y dispara con el click izquierdo.

El juego finaliza cuando se destruyen todos los bloques o cuando se acaban las bolas.

Autores:
    - Ángel Ricardo Gutierrez Meza (201847467)
    - Crhistian André Díaz Bonfigli Pastrana (201829189)
"""

import math
from typing import Union
import pygame

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

TEXT_HEIGHT = 30

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Tiro de Cañón")

font = pygame.font.SysFont("Arial", TEXT_HEIGHT)


class Ball:
    """Representa una bola disparada por el cañón."""

    def __init__(self, center: tuple[int, int], angle: float) -> None:
        """Inicializa los atributos del objeto bola.

        Args:
            center (tuple[int, int]): Coordenadas (x, y) del centro de la bola.
            angle (float): Ángulo de disparo de la bola en radianes.
        """
        self.center = [*center]
        self.angle = angle
        self.color = BALL_COLOR
        self.radius = BALL_RADIUS
        self.velocity_x = BALL_VELOCITY
        self.velocity_y = BALL_VELOCITY

    def draw(self) -> None:
        """Dibuja la bola en la pantalla."""
        pygame.draw.circle(screen, self.color, self.center, self.radius)

    def move(self) -> bool:
        """Mueve la bola en función del ángulo y la velocidad de la misma.

        Returns:
            bool: Si la bola ha llegado al borde inferior de la pantalla.
        """
        next_x = self.center[0] + self.velocity_x * math.cos(self.angle)
        next_y = self.center[1] + self.velocity_y * math.sin(self.angle)

        if next_x - self.radius > 0 and next_x + self.radius < WIDTH:
            self.center[0] = int(next_x)
        else:
            self.velocity_x *= -1

        if next_y - self.radius > 0 and next_y + self.radius < HEIGHT:
            self.center[1] = int(next_y)
        elif next_y + self.radius > HEIGHT:
            return True
        else:
            self.velocity_y *= -1

        return False


class Block:
    """Representa un bloque destruible por las bolas."""

    def __init__(self, start: tuple[int, int], width: int) -> None:
        """Inicializa los atributos del objeto bloque.

        Args:
            start (tuple[int, int]): Coordenadas (x, y) del punto superior izquierdo del bloque.
            width (int): Ancho del bloque.
        """
        self.start = start
        self.width = width
        self.color = BLOCK_COLOR
        self.height = BLOCK_HEIGHT

    def draw(self) -> None:
        """Dibuja el bloque en la pantalla."""
        rect = (*self.start, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect)


class Cannon:
    """Representa el cañón que dispara bolas."""

    def __init__(self, center: tuple[int, int], angle: float) -> None:
        """Inicializa los atributos del objeto cañón.

        Args:
            x (float): Coordenada x del centro del cañón.
            y (float): Coordenada y del centro del cañón.
            angle (float): Ángulo inicial del cañón en radianes.
        """
        self.center = center
        self.angle = angle
        self.color = CANNON_COLOR
        self.radius = CANNON_RADIUS
        self.width = CANNON_WIDTH
        self.height = CANNON_HEIGHT
        self.balls = CANNON_BALLS

    def get_end(self) -> tuple[int, int]:
        """Calcula el extremo del cañón en función del ángulo actual.

        Returns:
            Tuple[int, int]: Coordenadas (x, y) del extremo del cañón.
        """
        return (int(self.center[0] + self.height * math.cos(self.angle)),
                int(self.center[1] + self.height * math.sin(self.angle)))

    def draw(self) -> None:
        """Dibuja el cañón en la pantalla."""
        pygame.draw.circle(screen, self.color, self.center, self.radius)
        end = self.get_end()
        pygame.draw.line(screen, self.color, self.center, end, self.width)

    def move(self, angle: float) -> None:
        """Mueve el cañón a una nueva posición en función del ángulo dado.

        Args:
            angle (float): Nuevo ángulo del cañón en radianes.
        """
        self.angle = angle

    def shoot(self) -> Union[Ball, None]:
        """Crea una nueva bola y la devuelve si hay bolas disponibles."""
        if self.balls:
            self.balls -= 1
            return Ball(self.get_end(), self.angle)
        return None


def draw(
    cannon: Cannon,
    balls: list[Ball],
    blocks: list[Block],
    text: pygame.Surface,
    message: Union[pygame.Surface, None]
) -> None:
    """Dibuja todos los elementos en la pantalla.

    Args:
        cannon (Cannon): Objeto cañón.
        balls (list[Ball]): Lista de bolas.
        blocks (list[Block]): Lista de bloques.
        text (pygame.Surface): Superficie con el texto de las bolas disponibles.
        message (pygame.Surface): Superficie con el mensaje de victoria o derrota.
    """
    screen.fill(BLACK)

    cannon.draw()

    for ball in balls:
        ball.draw()

    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, TEXT_HEIGHT // 2)

    screen.blit(text, text_rect)

    if message:
        message_rect = message.get_rect()
        message_rect.center = (WIDTH // 2, TEXT_HEIGHT)

        screen.blit(message, message_rect)

    for block in blocks:
        block.draw()

    pygame.display.flip()


def handle_movement(cannon: Cannon, balls: list[Ball], blocks: list[Block]) -> None:
    """Mueve el cañón y las bolas en función de la posición del ratón.

    Args:
        cannon (Cannon): Objeto cañón.
        balls (list[Ball]): Lista de bolas.
        blocks (list[Block]): Lista de bloques.
    """
    pos = pygame.mouse.get_pos()
    angle = math.atan2(*(pos[i] - cannon.center[i] for i in [1, 0]))

    cannon.move(angle)

    balls_to_remove = []

    for ball in balls:
        if ball.move():
            balls_to_remove.append(ball)

    for ball in balls_to_remove:
        balls.remove(ball)

    handle_block_collisions(balls, blocks)


def handle_shoot(cannon: Cannon, balls: list[Ball]) -> None:
    """Dispara una nueva bola si hay bolas disponibles.

    Args:
        cannon (Cannon): Objeto cañón.
        balls (list[Ball]): Lista de bolas.
    """
    ball = cannon.shoot()

    if ball:
        balls.append(ball)


def handle_block_collisions(balls: list[Ball], blocks: list[Block]) -> None:
    """Revisa si las bolas colisionan con los bloques y los elimina si es necesario.

    Args:
        balls (list[Ball]): Lista de bolas.
        blocks (list[Block]): Lista de bloques.
    """
    blocks_to_remove = []

    for ball in balls:
        for block in blocks:
            if ball.center[1] - ball.radius <= block.start[1] + block.height and \
               ball.center[1] + ball.radius >= block.start[1] and \
               ball.center[0] - ball.radius <= block.start[0] + block.width and \
               ball.center[0] + ball.radius >= block.start[0]:
                blocks_to_remove.append(block)
                if ball.center[0] < block.start[0] or ball.center[0] > block.start[0] + block.width:
                    ball.velocity_x *= -1
                else:
                    ball.velocity_y *= -1

    for block in blocks_to_remove:
        blocks.remove(block)


def check_win(
    balls: list[Ball],
    blocks: list[Block],
    cannon: Cannon
) -> Union[pygame.Surface, None]:
    """Revisa si el jugador ha ganado o perdido y devuelve el mensaje correspondiente.

    Args:
        balls (list[Ball]): Lista de bolas.
        blocks (list[Block]): Lista de bloques.
        cannon (Cannon): Objeto cañón.

    Returns:
        Union[pygame.Surface, None]: Superficie con el mensaje de victoria o derrota.
    """
    if len(balls) + cannon.balls == 0 and len(blocks) > 0:
        return font.render("Perdiste. Presiona espacio para reiniciar.", True, WHITE)
    if len(blocks) == 0:
        return font.render("Ganaste. Presiona espacio para reiniciar.", True, WHITE)
    return None


def main() -> None:
    """Función principal del juego."""
    restart = True

    while restart:
        clock = pygame.time.Clock()

        cannon = Cannon((WIDTH // 2, HEIGHT), 3 * math.pi / 2)

        balls = []

        pressed = False

        blocks = []

        block_width = (WIDTH - BLOCK_GAP *
                       (BLOCK_COUNT[0] + 1)) // BLOCK_COUNT[0]

        step_x = block_width + BLOCK_GAP
        step_y = BLOCK_HEIGHT + BLOCK_GAP

        for i in range(BLOCK_GAP, BLOCK_GAP + BLOCK_COUNT[0] * step_x, step_x):
            for j in range(2 * TEXT_HEIGHT, 2 * TEXT_HEIGHT + BLOCK_COUNT[1] * step_y, step_y):
                blocks.append(Block((i, j), block_width))

        while True:
            clock.tick(FPS)

            text = font.render(f"Balls: {cannon.balls}", True, WHITE)

            message = check_win(balls, blocks, cannon)

            draw(cannon, balls, blocks, text, message)

            handle_movement(cannon, balls, blocks)

            last_pressed = pressed
            pressed = pygame.mouse.get_pressed()[0]

            if (pressed and not last_pressed):
                handle_shoot(cannon, balls)

            if message and pygame.key.get_pressed()[pygame.K_SPACE]:
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    restart = False
                    break

    pygame.quit()


if __name__ == "__main__":
    main()
