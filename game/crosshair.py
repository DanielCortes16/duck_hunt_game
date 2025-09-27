"""
Sistema de mira para Duck Hunt
"""

import pygame
import math
from typing import Tuple
from utils.config import *
from utils.helpers import smooth_movement


class Crosshair:
    """Clase que maneja la mira del juego."""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Posición actual y objetivo
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.target_x = self.x
        self.target_y = self.y
        
        # Configuración visual
        self.size = CROSSHAIR_SIZE
        self.color = CROSSHAIR_COLOR
        self.thickness = CROSSHAIR_THICKNESS
        
        # Suavizado del movimiento
        self.smoothing_factor = SMOOTHING_FACTOR
        
        # Estado de disparo
        self.is_shooting = False
        self.shoot_animation_time = 0
        self.max_shoot_animation = 0.2  # Duración de la animación de disparo
        
    def update_position(self, target_x: float, target_y: float) -> None:
        """Actualiza la posición objetivo de la mira."""
        # Limitar a los bordes de la pantalla
        self.target_x = max(self.size, min(self.screen_width - self.size, target_x))
        self.target_y = max(self.size, min(self.screen_height - self.size, target_y))
        
        # Aplicar suavizado
        self.x, self.y = smooth_movement(
            (self.x, self.y), 
            (self.target_x, self.target_y), 
            self.smoothing_factor
        )
    
    def shoot(self) -> None:
        """Inicia la animación de disparo."""
        self.is_shooting = True
        self.shoot_animation_time = 0
    
    def update(self, dt: float) -> None:
        """Actualiza la animación de disparo."""
        if self.is_shooting:
            self.shoot_animation_time += dt
            if self.shoot_animation_time >= self.max_shoot_animation:
                self.is_shooting = False
                self.shoot_animation_time = 0
    
    def draw(self, screen: pygame.Surface) -> None:
        """Dibuja la mira en la pantalla."""
        center_x = int(self.x)
        center_y = int(self.y)
        
        # Usar sprites auténticos del Duck Hunt
        if self.is_shooting:
            self._draw_authentic_crosshair_shooting(screen, center_x, center_y)
        else:
            self._draw_authentic_crosshair(screen, center_x, center_y)
    
    def _draw_authentic_crosshair(self, screen: pygame.Surface, center_x: int, center_y: int) -> None:
        """Dibuja la mira normal (estilo NES)."""
        # Cruz de la mira (píxeles individuales como en NES)
        # Línea horizontal
        for x in range(center_x - 8, center_x + 8):
            screen.set_at((x, center_y), self.color)
            screen.set_at((x, center_y + 1), self.color)
        
        # Línea vertical
        for y in range(center_y - 8, center_y + 8):
            screen.set_at((center_x, y), self.color)
            screen.set_at((center_x + 1, y), self.color)
        
        # Punto central (blanco)
        screen.set_at((center_x, center_y), (255, 255, 255))
        screen.set_at((center_x + 1, center_y), (255, 255, 255))
        screen.set_at((center_x, center_y + 1), (255, 255, 255))
        screen.set_at((center_x + 1, center_y + 1), (255, 255, 255))
    
    def _draw_authentic_crosshair_shooting(self, screen: pygame.Surface, center_x: int, center_y: int) -> None:
        """Dibuja la mira disparando (estilo NES)."""
        # Cruz más grande
        # Línea horizontal
        for x in range(center_x - 12, center_x + 12):
            screen.set_at((x, center_y), self.color)
            screen.set_at((x, center_y + 1), self.color)
        
        # Línea vertical
        for y in range(center_y - 12, center_y + 12):
            screen.set_at((center_x, y), self.color)
            screen.set_at((center_x + 1, y), self.color)
        
        # Punto central más grande (blanco)
        for x in range(center_x - 1, center_x + 3):
            for y in range(center_y - 1, center_y + 3):
                screen.set_at((x, y), (255, 255, 255))
        
        # Efecto de destello (píxeles blancos)
        flash_radius = 8
        for i in range(-flash_radius, flash_radius + 1):
            for j in range(-flash_radius, flash_radius + 1):
                if i * i + j * j <= flash_radius * flash_radius:
                    screen.set_at((center_x + i, center_y + j), (255, 255, 255))
    
    def get_position(self) -> Tuple[float, float]:
        """Retorna la posición actual de la mira."""
        return (self.x, self.y)
    
    def get_radius(self) -> float:
        """Retorna el radio de colisión de la mira."""
        return self.size // 2
    
    def is_ready_to_shoot(self) -> bool:
        """Verifica si la mira está lista para disparar (no en animación)."""
        return not self.is_shooting
