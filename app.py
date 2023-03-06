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
from models import Ball, Block, Cannon
from colors import BLACK, WHITE

WIDTH, HEIGHT = 800, 600

FPS = 60

BLOCK_HEIGHT = 40
BLOCK_GAP = 30
BLOCK_COUNT = (10, 5)

TEXT_HEIGHT = 30

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Tiro de Cañón")

font = pygame.font.SysFont("Arial", TEXT_HEIGHT)


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

    cannon.draw(screen)

    for ball in balls:
        ball.draw(screen)

    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, TEXT_HEIGHT // 2)

    screen.blit(text, text_rect)

    if message:
        message_rect = message.get_rect()
        message_rect.center = (WIDTH // 2, (3 * TEXT_HEIGHT) // 2)

        screen.blit(message, message_rect)

    for block in blocks:
        block.draw(screen)

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

    balls_to_remove = set(b for b in balls if b.move_or_remove(screen))

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
    blocks_to_remove = set[Block]()

    for ball in balls:
        for block in blocks:
            if block.collide(ball):
                blocks_to_remove.add(block)
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

        for i in range(
            BLOCK_GAP,
            BLOCK_GAP + BLOCK_COUNT[0] * step_x,
            step_x
        ):
            for j in range(
                2 * TEXT_HEIGHT + BLOCK_GAP,
                2 * TEXT_HEIGHT + BLOCK_COUNT[1] * step_y,
                step_y
            ):
                blocks.append(Block((i, j), block_width, BLOCK_HEIGHT))

        while restart:
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
