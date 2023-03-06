"""Módulo que contiene la clase Ball."""

import math
import pygame
from colors import WHITE
from common import Coordinate

BALL_COLOR = WHITE
BALL_RADIUS = 10
BALL_VELOCITY = 5


class Ball:
    """Representa una bola disparada por el cañón."""

    def __init__(self, center: Coordinate, angle: float) -> None:
        """Inicializa los atributos del objeto bola.

        Args:
            center (Coordinate): Coordenadas (x, y) del centro de la bola.
            angle (float): Ángulo de disparo de la bola en radianes.
        """
        self.center = [*center]
        self.angle = angle
        self.color = BALL_COLOR
        self.radius = BALL_RADIUS
        self.velocity_x = BALL_VELOCITY
        self.velocity_y = BALL_VELOCITY

    def draw(self, screen: pygame.Surface) -> None:
        """Dibuja la bola en la pantalla."""
        pygame.draw.circle(screen, self.color, self.center, self.radius)

    def move(self, screen: pygame.Surface) -> bool:
        """Mueve la bola en función del ángulo y la velocidad de la misma.

        Returns:
            bool: Si la bola ha llegado al borde inferior de la pantalla.
        """
        next_x = self.center[0] + self.velocity_x * math.cos(self.angle)
        next_y = self.center[1] + self.velocity_y * math.sin(self.angle)

        if next_x - self.radius > 0 and next_x + self.radius < screen.get_width():
            self.center[0] = int(next_x)
        else:
            self.velocity_x *= -1

        if next_y - self.radius > 0 and next_y + self.radius < screen.get_height():
            self.center[1] = int(next_y)
        elif next_y + self.radius > screen.get_height():
            return True
        else:
            self.velocity_y *= -1

        return False
