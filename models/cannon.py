"""Módulo que contiene la clase Cannon."""

import math
from typing import Union
import pygame
from models.ball import Ball
from colors import WHITE
from common import Coordinate

CANNON_COLOR = WHITE
CANNON_RADIUS = 50
CANNON_WIDTH = 20
CANNON_HEIGHT = 80
CANNON_BALLS = 10


class Cannon:
    """Representa el cañón que dispara bolas."""

    def __init__(self, center: Coordinate, angle: float) -> None:
        """Inicializa los atributos del objeto cañón.

        Args:
            center (Coordinate): Coordenadas (x, y) del centro del cañón.
            angle (float): Ángulo inicial del cañón en radianes.
        """
        self.center = center
        self.angle = angle
        self.color = CANNON_COLOR
        self.radius = CANNON_RADIUS
        self.width = CANNON_WIDTH
        self.height = CANNON_HEIGHT
        self.balls = CANNON_BALLS

    def get_end(self) -> Coordinate:
        """Calcula el extremo del cañón en función del ángulo actual.

        Returns:
            Coordinate: Coordenadas (x, y) del extremo del cañón.
        """
        return (self.center[0] + self.height * math.cos(self.angle),
                self.center[1] + self.height * math.sin(self.angle))

    def draw(self, screen: pygame.Surface) -> None:
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
