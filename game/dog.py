"""
Sistema de animación del perro en Duck Hunt
"""

import pygame
import random
import math
from typing import Tuple
from utils.config import *


class Dog:
    """Clase que maneja la animación del perro."""
    
    def __init__(self, screen_width: int, screen_height: int, sprites=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Posición del perro
        self.x = screen_width // 2 - 50
        self.y = screen_height - 150
        
        # Estados de animación
        self.is_laughing = False
        self.is_hiding = False
        self.animation_time = 0
        self.laugh_duration = 2.0  # Duración de la risa en segundos
        
        # Configuración visual
        self.width = 100
        self.height = 80
        
        # Movimiento
        self.bob_offset = 0
        self.bob_speed = 0.1
        self.sprites = sprites
        
    def start_laughing(self) -> None:
        """Inicia la animación de risa del perro."""
        if not self.is_laughing:
            self.is_laughing = True
            self.animation_time = 0
            self.is_hiding = False
    
    def hide(self) -> None:
        """Hace que el perro se esconda."""
        self.is_hiding = True
        self.is_laughing = False
    
    def update(self, dt: float) -> None:
        """Actualiza la animación del perro."""
        self.animation_time += dt
        
        # Actualizar movimiento de cabeceo
        self.bob_offset += self.bob_speed * dt
        
        # Finalizar risa después del tiempo especificado
        if self.is_laughing and self.animation_time >= self.laugh_duration:
            self.is_laughing = False
            self.animation_time = 0
    
    def draw(self, screen: pygame.Surface) -> None:
        """Dibuja el perro en la pantalla."""
        if self.is_hiding:
            return
            
        # Calcular posición con movimiento de cabeceo
        draw_y = self.y + math.sin(self.bob_offset) * 3
        
        # Usar sprites auténticos del Duck Hunt
        if self.is_laughing:
            self._draw_authentic_laughing_dog(screen, draw_y)
        else:
            self._draw_authentic_normal_dog(screen, draw_y)
    
    def _draw_authentic_normal_dog(self, screen: pygame.Surface, y: float) -> None:
        """Dibuja el perro normal (estilo NES)."""
        # Crear sprite del perro
        dog_sprite = pygame.Surface((32, 24), pygame.SRCALPHA)
        
        # Cuerpo del perro (marrón)
        body_color = (139, 69, 19)
        pygame.draw.rect(dog_sprite, body_color, (8, 12, 16, 8))
        
        # Cabeza
        head_color = (160, 82, 45)
        pygame.draw.circle(dog_sprite, head_color, (20, 8), 6)
        
        # Orejas
        ear_color = (101, 67, 33)
        pygame.draw.circle(dog_sprite, ear_color, (16, 6), 3)
        pygame.draw.circle(dog_sprite, ear_color, (24, 6), 3)
        
        # Hocico
        muzzle_color = (255, 255, 255)
        pygame.draw.circle(dog_sprite, muzzle_color, (22, 8), 2)
        
        # Ojos
        pygame.draw.circle(dog_sprite, (0, 0, 0), (18, 6), 1)
        pygame.draw.circle(dog_sprite, (0, 0, 0), (22, 6), 1)
        
        # Nariz
        pygame.draw.circle(dog_sprite, (0, 0, 0), (22, 8), 1)
        
        # Cola
        pygame.draw.rect(dog_sprite, body_color, (4, 16, 4, 6))
        
        # Escalar y dibujar
        dog_sprite = pygame.transform.scale(dog_sprite, (64, 48))
        screen.blit(dog_sprite, (int(self.x), int(y)))
    
    def _draw_authentic_laughing_dog(self, screen: pygame.Surface, y: float) -> None:
        """Dibuja el perro riéndose (estilo NES)."""
        # Crear sprite del perro riéndose
        dog_sprite = pygame.Surface((32, 24), pygame.SRCALPHA)
        
        # Cuerpo del perro (más grande cuando se ríe)
        body_color = (139, 69, 19)
        pygame.draw.rect(dog_sprite, body_color, (6, 10, 20, 10))
        
        # Cabeza
        head_color = (160, 82, 45)
        pygame.draw.circle(dog_sprite, head_color, (20, 6), 7)
        
        # Orejas (animadas)
        ear_color = (101, 67, 33)
        pygame.draw.circle(dog_sprite, ear_color, (14, 4), 4)
        pygame.draw.circle(dog_sprite, ear_color, (26, 4), 4)
        
        # Ojos cerrados (risa)
        pygame.draw.arc(dog_sprite, (0, 0, 0), (16, 4, 4, 3), 0, math.pi, 1)
        pygame.draw.arc(dog_sprite, (0, 0, 0), (20, 4, 4, 3), 0, math.pi, 1)
        
        # Boca abierta (risa)
        pygame.draw.arc(dog_sprite, (0, 0, 0), (16, 8, 8, 4), 0, math.pi, 2)
        
        # Lengua
        tongue_color = (255, 192, 203)
        pygame.draw.rect(dog_sprite, tongue_color, (18, 10, 4, 3))
        
        # Cola moviéndose
        pygame.draw.rect(dog_sprite, body_color, (2, 14, 6, 8))
        
        # Escalar y dibujar
        dog_sprite = pygame.transform.scale(dog_sprite, (64, 48))
        screen.blit(dog_sprite, (int(self.x), int(y)))
    
    def _draw_normal_dog(self, screen: pygame.Surface, y: float) -> None:
        """Dibuja el perro en estado normal."""
        # Cuerpo del perro
        body_color = (139, 69, 19)  # Marrón
        pygame.draw.ellipse(screen, body_color,
                          (self.x, y, self.width, self.height))
        
        # Cabeza
        head_size = 40
        head_x = self.x + self.width - 20
        head_y = y + 10
        pygame.draw.circle(screen, body_color,
                          (int(head_x), int(head_y)), head_size//2)
        
        # Orejas
        ear_color = (101, 67, 33)  # Marrón más oscuro
        pygame.draw.circle(screen, ear_color,
                          (int(head_x - 15), int(head_y - 10)), 8)
        pygame.draw.circle(screen, ear_color,
                          (int(head_x + 15), int(head_y - 10)), 8)
        
        # Ojos
        pygame.draw.circle(screen, (0, 0, 0),
                          (int(head_x - 8), int(head_y - 5)), 3)
        pygame.draw.circle(screen, (0, 0, 0),
                          (int(head_x + 8), int(head_y - 5)), 3)
        
        # Nariz
        pygame.draw.circle(screen, (0, 0, 0),
                          (int(head_x), int(head_y + 5)), 2)
        
        # Cola
        tail_x = self.x - 10
        tail_y = y + self.height//2
        pygame.draw.ellipse(screen, body_color,
                          (tail_x, tail_y, 20, 8))
    
    def _draw_laughing_dog(self, screen: pygame.Surface, y: float) -> None:
        """Dibuja el perro riéndose."""
        # Cuerpo del perro (más grande cuando se ríe)
        body_color = (139, 69, 19)
        laugh_scale = 1.2
        laugh_width = int(self.width * laugh_scale)
        laugh_height = int(self.height * laugh_scale)
        
        pygame.draw.ellipse(screen, body_color,
                          (self.x - 10, y - 10, laugh_width, laugh_height))
        
        # Cabeza
        head_size = 45
        head_x = self.x + laugh_width - 15
        head_y = y
        pygame.draw.circle(screen, body_color,
                          (int(head_x), int(head_y)), head_size//2)
        
        # Orejas (más animadas)
        ear_color = (101, 67, 33)
        ear_bob = math.sin(self.animation_time * 10) * 3
        pygame.draw.circle(screen, ear_color,
                          (int(head_x - 15), int(head_y - 10 + ear_bob)), 8)
        pygame.draw.circle(screen, ear_color,
                          (int(head_x + 15), int(head_y - 10 - ear_bob)), 8)
        
        # Ojos cerrados (risa)
        eye_y = head_y - 5
        pygame.draw.arc(screen, (0, 0, 0),
                       (head_x - 12, eye_y - 3, 8, 6), 0, math.pi, 2)
        pygame.draw.arc(screen, (0, 0, 0),
                       (head_x + 4, eye_y - 3, 8, 6), 0, math.pi, 2)
        
        # Boca abierta (risa)
        mouth_y = head_y + 8
        pygame.draw.arc(screen, (0, 0, 0),
                       (head_x - 8, mouth_y - 5, 16, 10), 0, math.pi, 3)
        
        # Lengua
        tongue_color = (255, 192, 203)  # Rosa
        pygame.draw.ellipse(screen, tongue_color,
                          (head_x - 3, mouth_y + 2, 6, 8))
        
        # Cola moviéndose
        tail_x = self.x - 15
        tail_y = y + laugh_height//2
        tail_swing = math.sin(self.animation_time * 8) * 10
        pygame.draw.ellipse(screen, body_color,
                          (tail_x + tail_swing, tail_y, 25, 10))
        
        # Partículas de risa (opcional)
        if random.random() < 0.3:
            for i in range(3):
                particle_x = head_x + random.randint(-20, 20)
                particle_y = head_y - random.randint(10, 30)
                pygame.draw.circle(screen, (255, 255, 0),
                                 (int(particle_x), int(particle_y)), 2)
    
    def is_animating(self) -> bool:
        """Verifica si el perro está en alguna animación."""
        return self.is_laughing or self.is_hiding
    
    def get_rect(self) -> pygame.Rect:
        """Retorna el rectángulo de colisión del perro."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
