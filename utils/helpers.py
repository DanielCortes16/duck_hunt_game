"""
Funciones auxiliares para el juego Duck Hunt
"""

import math
import pygame
from typing import Tuple, List


def distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """Calcula la distancia euclidiana entre dos puntos."""
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Limita un valor entre un mínimo y máximo."""
    return max(min_val, min(max_val, value))


def lerp(start: float, end: float, factor: float) -> float:
    """Interpolación lineal entre dos valores."""
    return start + (end - start) * factor


def smooth_movement(current_pos: Tuple[float, float], 
                   target_pos: Tuple[float, float], 
                   smoothing_factor: float) -> Tuple[float, float]:
    """Suaviza el movimiento entre la posición actual y la objetivo."""
    x = lerp(current_pos[0], target_pos[0], smoothing_factor)
    y = lerp(current_pos[1], target_pos[1], smoothing_factor)
    return (x, y)


def is_point_in_circle(point: Tuple[float, float], 
                      center: Tuple[float, float], 
                      radius: float) -> bool:
    """Verifica si un punto está dentro de un círculo."""
    return distance(point, center) <= radius


def normalize_hand_position(hand_x: float, hand_y: float, 
                           camera_width: int, camera_height: int,
                           screen_width: int, screen_height: int) -> Tuple[float, float]:
    """Normaliza las coordenadas de la mano a coordenadas de pantalla."""
    # Invertir coordenadas Y (la cámara tiene Y invertido)
    normalized_x = hand_x / camera_width
    normalized_y = (hand_y / camera_height)
    
    # Convertir a coordenadas de pantalla
    screen_x = normalized_x * screen_width
    screen_y = normalized_y * screen_height
    
    return (screen_x, screen_y)


def draw_text(surface: pygame.Surface, text: str, font: pygame.font.Font, 
              color: Tuple[int, int, int], position: Tuple[int, int]) -> None:
    """Dibuja texto en la superficie."""
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)


def create_gradient_background(width: int, height: int) -> pygame.Surface:
    """Crea un fondo con gradiente cielo-pasto."""
    surface = pygame.Surface((width, height))
    
    # Gradiente del cielo
    for y in range(height // 2):
        color_intensity = int(255 * (1 - y / (height // 2)))
        color = (135, 206, color_intensity)
        pygame.draw.line(surface, color, (0, y), (width, y))
    
    # Pasto
    grass_height = height // 3
    for y in range(height // 2, height):
        grass_intensity = int(255 * ((y - height // 2) / grass_height))
        color = (34, min(139, 34 + grass_intensity), 34)
        pygame.draw.line(surface, color, (0, y), (width, y))
    
    return surface


def calculate_duck_score(duck_speed: float, distance_traveled: float) -> int:
    """Calcula la puntuación basada en la velocidad del pato y distancia recorrida."""
    base_score = 100
    speed_bonus = int(duck_speed * 10)
    distance_bonus = int(distance_traveled * 0.1)
    return base_score + speed_bonus + distance_bonus
