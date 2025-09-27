"""
Sprites auténticos del Duck Hunt original
Basados en los sprites del NES
"""

import pygame
import math
from typing import Tuple, List
from utils.config import *


class AuthenticDuckHuntSprites:
    """Sprites auténticos del Duck Hunt original."""
    
    def __init__(self):
        self.sprites = {}
        self.assets_path = 'assets/images/'
        self.sprite_sheet = pygame.image.load(self.assets_path + 'duck-hunt-sprites.png').convert_alpha()
        self.background_img = pygame.image.load(self.assets_path + 'background.png').convert()
        self.crosshair_img = pygame.image.load(self.assets_path + 'cursor.png').convert_alpha()
        self.create_authentic_sprites()
    
    def create_authentic_sprites(self) -> None:
        """Carga los sprites auténticos del Duck Hunt desde los assets."""
        self.create_dog_sprites()
        self.create_duck_sprites()
        self.create_background_sprites()
        self.create_crosshair_sprites()
    
    def create_dog_sprites(self) -> None:
        """Recorta los sprites del perro desde el sprite sheet."""
        # Coordenadas y tamaños de los sprites del perro en duck-hunt-sprites.png
        self.sprites['dog_normal'] = self._get_sprite((0, 0, 32, 24))
        self.sprites['dog_laughing'] = self._get_sprite((32, 0, 32, 24))
        self.sprites['dog_with_duck'] = self._get_sprite((64, 0, 32, 24))
        self.sprites['dog_running'] = self._get_sprite((96, 0, 32, 24))
    
    def draw_authentic_dog_normal(self, surface: pygame.Surface) -> None:
        """Dibuja el perro en estado normal (estilo NES)."""
        # Cuerpo del perro (marrón)
        body_color = (139, 69, 19)
        pygame.draw.rect(surface, body_color, (8, 12, 16, 8))
        
        # Cabeza
        head_color = (160, 82, 45)
        pygame.draw.circle(surface, head_color, (20, 8), 6)
        
        # Orejas
        ear_color = (101, 67, 33)
        pygame.draw.circle(surface, ear_color, (16, 6), 3)
        pygame.draw.circle(surface, ear_color, (24, 6), 3)
        
        # Hocico
        muzzle_color = (255, 255, 255)
        pygame.draw.circle(surface, muzzle_color, (22, 8), 2)
        
        # Ojos
        pygame.draw.circle(surface, (0, 0, 0), (18, 6), 1)
        pygame.draw.circle(surface, (0, 0, 0), (22, 6), 1)
        
        # Nariz
        pygame.draw.circle(surface, (0, 0, 0), (22, 8), 1)
        
        # Cola
        pygame.draw.rect(surface, body_color, (4, 16, 4, 6))
    
    def draw_authentic_dog_laughing(self, surface: pygame.Surface) -> None:
        """Dibuja el perro riéndose (estilo NES)."""
        # Cuerpo del perro (más grande cuando se ríe)
        body_color = (139, 69, 19)
        pygame.draw.rect(surface, body_color, (6, 10, 20, 10))
        
        # Cabeza
        head_color = (160, 82, 45)
        pygame.draw.circle(surface, head_color, (20, 6), 7)
        
        # Orejas (animadas)
        ear_color = (101, 67, 33)
        pygame.draw.circle(surface, ear_color, (14, 4), 4)
        pygame.draw.circle(surface, ear_color, (26, 4), 4)
        
        # Ojos cerrados (risa)
        pygame.draw.arc(surface, (0, 0, 0), (16, 4, 4, 3), 0, math.pi, 1)
        pygame.draw.arc(surface, (0, 0, 0), (20, 4, 4, 3), 0, math.pi, 1)
        
        # Boca abierta (risa)
        pygame.draw.arc(surface, (0, 0, 0), (16, 8, 8, 4), 0, math.pi, 2)
        
        # Lengua
        tongue_color = (255, 192, 203)
        pygame.draw.rect(surface, tongue_color, (18, 10, 4, 3))
        
        # Cola moviéndose
        pygame.draw.rect(surface, body_color, (2, 14, 6, 8))
    
    def draw_authentic_dog_with_duck(self, surface: pygame.Surface) -> None:
        """Dibuja el perro con pato en la boca."""
        # Cuerpo del perro
        body_color = (139, 69, 19)
        pygame.draw.rect(surface, body_color, (8, 12, 16, 8))
        
        # Cabeza
        head_color = (160, 82, 45)
        pygame.draw.circle(surface, head_color, (20, 8), 6)
        
        # Pato en la boca
        duck_color = (255, 255, 255)
        pygame.draw.circle(surface, duck_color, (24, 8), 3)
        pygame.draw.circle(surface, (0, 255, 0), (25, 7), 1)  # Cabeza del pato
        
        # Ojos del perro
        pygame.draw.circle(surface, (0, 0, 0), (18, 6), 1)
        pygame.draw.circle(surface, (0, 0, 0), (22, 6), 1)
    
    def draw_authentic_dog_running(self, surface: pygame.Surface) -> None:
        """Dibuja el perro corriendo."""
        # Cuerpo del perro (estirado)
        body_color = (139, 69, 19)
        pygame.draw.ellipse(surface, body_color, (6, 14, 20, 8))
        
        # Cabeza
        head_color = (160, 82, 45)
        pygame.draw.circle(surface, head_color, (22, 10), 5)
        
        # Patas (en movimiento)
        pygame.draw.rect(surface, body_color, (8, 20, 2, 4))
        pygame.draw.rect(surface, body_color, (12, 20, 2, 4))
        pygame.draw.rect(surface, body_color, (18, 20, 2, 4))
        pygame.draw.rect(surface, body_color, (22, 20, 2, 4))
    
    def create_duck_sprites(self) -> None:
        """Recorta los sprites de los patos desde el sprite sheet."""
        self.sprites['duck_blue_flying'] = self._get_sprite((0, 24, 32, 24))
        self.sprites['duck_green_flying'] = self._get_sprite((32, 24, 32, 24))
        self.sprites['duck_red_flying'] = self._get_sprite((64, 24, 32, 24))
        self.sprites['duck_falling'] = self._get_sprite((96, 24, 32, 24))
    
    def draw_authentic_duck_flying(self, surface: pygame.Surface, color_type: str) -> None:
        """Dibuja un pato volando (estilo NES)."""
        # Colores según el tipo
        if color_type == "blue":
            body_color = (0, 0, 255)
            head_color = (255, 0, 255)
        elif color_type == "green":
            body_color = (0, 255, 0)
            head_color = (0, 0, 0)
        else:  # red
            body_color = (255, 0, 0)
            head_color = (0, 255, 0)
        
        # Cuerpo del pato
        pygame.draw.ellipse(surface, body_color, (2, 4, 12, 8))
        
        # Cabeza
        pygame.draw.circle(surface, head_color, (12, 6), 3)
        
        # Pico
        pygame.draw.polygon(surface, (255, 165, 0), [
            (14, 6), (16, 5), (16, 7)
        ])
        
        # Ojo
        pygame.draw.circle(surface, (0, 0, 0), (13, 5), 1)
        
        # Alas (animadas)
        wing_color = (255, 255, 255)
        pygame.draw.polygon(surface, wing_color, [
            (6, 6), (10, 4), (8, 8)
        ])
    
    def draw_authentic_duck_falling(self, surface: pygame.Surface) -> None:
        """Dibuja un pato cayendo (estilo NES)."""
        # Cuerpo del pato (marrón)
        body_color = (139, 69, 19)
        pygame.draw.ellipse(surface, body_color, (2, 4, 12, 8))
        
        # Cabeza (inclinada)
        head_color = (160, 82, 45)
        pygame.draw.circle(surface, head_color, (10, 6), 3)
        
        # Pico (hacia abajo)
        pygame.draw.polygon(surface, (255, 165, 0), [
            (10, 8), (9, 10), (11, 10)
        ])
        
        # Ojo (cerrado)
        pygame.draw.arc(surface, (0, 0, 0), (9, 5, 2, 2), 0, math.pi, 1)
        
        # Alas (extendidas)
        wing_color = (255, 255, 255)
        pygame.draw.polygon(surface, wing_color, [
            (4, 6), (8, 4), (6, 10)
        ])
        pygame.draw.polygon(surface, wing_color, [
            (12, 6), (8, 4), (10, 10)
        ])
    
    def create_background_sprites(self) -> None:
        """Recorta los sprites de arbustos y árbol desde el sprite sheet."""
        self.sprites['bush_small'] = self._get_sprite((0, 48, 32, 24))
        self.sprites['bush_large'] = self._get_sprite((32, 48, 32, 24))
        self.sprites['tree'] = self._get_sprite((64, 48, 32, 48))
    
    def draw_authentic_bush(self, surface: pygame.Surface) -> None:
        """Dibuja un arbusto pequeño (estilo NES)."""
        bush_color = (0, 128, 0)
        # Múltiples círculos para formar el arbusto
        pygame.draw.circle(surface, bush_color, (8, 8), 4)
        pygame.draw.circle(surface, bush_color, (4, 6), 3)
        pygame.draw.circle(surface, bush_color, (12, 6), 3)
        pygame.draw.circle(surface, bush_color, (8, 4), 3)
    
    def draw_authentic_bush_large(self, surface: pygame.Surface) -> None:
        """Dibuja un arbusto grande (estilo NES)."""
        bush_color = (0, 128, 0)
        # Múltiples círculos más grandes
        pygame.draw.circle(surface, bush_color, (12, 12), 6)
        pygame.draw.circle(surface, bush_color, (6, 9), 4)
        pygame.draw.circle(surface, bush_color, (18, 9), 4)
        pygame.draw.circle(surface, bush_color, (12, 6), 4)
        pygame.draw.circle(surface, bush_color, (9, 3), 3)
        pygame.draw.circle(surface, bush_color, (15, 3), 3)
    
    def draw_authentic_tree(self, surface: pygame.Surface) -> None:
        """Dibuja un árbol (estilo NES)."""
        # Tronco
        trunk_color = (101, 67, 33)
        pygame.draw.rect(surface, trunk_color, (8, 16, 4, 8))
        
        # Copa del árbol
        tree_color = (0, 128, 0)
        pygame.draw.circle(surface, tree_color, (10, 12), 8)
        pygame.draw.circle(surface, tree_color, (6, 10), 5)
        pygame.draw.circle(surface, tree_color, (14, 10), 5)
    
    def create_crosshair_sprites(self) -> None:
        """Carga la imagen de la mira desde el asset."""
        self.sprites['crosshair'] = self.crosshair_img
    def _get_sprite(self, rect: Tuple[int, int, int, int]) -> pygame.Surface:
        """Recorta un sprite del sprite sheet."""
        x, y, w, h = rect
        sprite = pygame.Surface((w, h), pygame.SRCALPHA)
        sprite.blit(self.sprite_sheet, (0, 0), rect)
        return sprite
    
    def draw_authentic_crosshair(self, surface: pygame.Surface) -> None:
        """Dibuja la mira normal (estilo NES)."""
        center_x, center_y = 8, 8
        
        # Cruz de la mira (píxeles individuales)
        # Línea horizontal
        for x in range(2, 15):
            surface.set_at((x, center_y), (255, 0, 0))
            surface.set_at((x, center_y + 1), (255, 0, 0))
        
        # Línea vertical
        for y in range(2, 15):
            surface.set_at((center_x, y), (255, 0, 0))
            surface.set_at((center_x + 1, y), (255, 0, 0))
        
        # Punto central
        surface.set_at((center_x, center_y), (255, 255, 255))
        surface.set_at((center_x + 1, center_y), (255, 255, 255))
        surface.set_at((center_x, center_y + 1), (255, 255, 255))
        surface.set_at((center_x + 1, center_y + 1), (255, 255, 255))
    
    def draw_authentic_crosshair_shooting(self, surface: pygame.Surface) -> None:
        """Dibuja la mira disparando (estilo NES)."""
        center_x, center_y = 10, 10
        
        # Cruz más grande
        # Línea horizontal
        for x in range(2, 19):
            surface.set_at((x, center_y), (255, 0, 0))
            surface.set_at((x, center_y + 1), (255, 0, 0))
        
        # Línea vertical
        for y in range(2, 19):
            surface.set_at((center_x, y), (255, 0, 0))
            surface.set_at((center_x + 1, y), (255, 0, 0))
        
        # Punto central más grande
        for x in range(center_x - 1, center_x + 3):
            for y in range(center_y - 1, center_y + 3):
                surface.set_at((x, y), (255, 255, 255))
    
    def create_authentic_background(self, width: int, height: int) -> pygame.Surface:
        """Devuelve el fondo original escalado al tamaño de la ventana."""
        return pygame.transform.scale(self.background_img, (width, height))
    
    def draw_authentic_background_bushes(self, surface: pygame.Surface, width: int, height: int) -> None:
        """Dibuja arbustos del fondo (estilo NES)."""
        bush_color = (0, 100, 0)
        horizon_y = height // 2
        
        # Múltiples arbustos
        for i in range(8):
            x = i * (width // 8) + 20
            y = horizon_y - 15
            
            # Arbusto con píxeles individuales
            for j in range(3):
                for k in range(3):
                    surface.set_at((x + j, y + k), bush_color)
                    surface.set_at((x + j + 1, y + k), bush_color)
                    surface.set_at((x + j, y + k + 1), bush_color)
    
    def get_sprite(self, name: str) -> pygame.Surface:
        """Obtiene un sprite por nombre."""
        return self.sprites.get(name, pygame.Surface((1, 1)))
    
    def get_duck_sprite(self, color_type: str, state: str) -> pygame.Surface:
        """Obtiene un sprite de pato específico."""
        if state == "flying":
            return self.sprites.get(f'duck_{color_type}_flying', self.sprites['duck_blue_flying'])
        elif state == "falling":
            return self.sprites['duck_falling']
        else:
            return self.sprites['duck_blue_flying']
    
    def get_dog_sprite(self, state: str) -> pygame.Surface:
        """Obtiene un sprite del perro específico."""
        return self.sprites.get(f'dog_{state}', self.sprites['dog_normal'])
