"""
Lógica de los patos en Duck Hunt
"""

import pygame
import random
import math
from typing import Tuple, List
from utils.config import *
from utils.helpers import distance


class Duck:
    """Clase que representa un pato en el juego."""
    
    def __init__(self, screen_width: int, screen_height: int, sprites=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Posición y movimiento
        self.x = -50  # Empezar fuera de la pantalla
        self.y = random.randint(DUCK_FLIGHT_HEIGHT_MIN, DUCK_FLIGHT_HEIGHT_MAX)
        self.speed = DEFAULT_DUCK_SPEED + random.uniform(-0.5, 1.5)
        self.direction = 1  # 1 para derecha, -1 para izquierda
        
        # Estado del pato
        self.is_alive = True
        self.is_flying_away = False
        self.flight_pattern = random.choice(['straight', 'wave', 'zigzag'])
        self.pattern_offset = 0
        
        # Dimensiones
        self.width = 40
        self.height = 30
        
        # Animación
        self.wing_flap_time = 0
        self.wing_flap_speed = 0.3
        
    # Puntuación
        self.sprites = sprites
        self.base_score = SCORE_PER_DUCK
        self.distance_traveled = 0
        
    def update(self, dt: float) -> None:
        """Actualiza la posición y estado del pato."""
        if not self.is_alive or self.is_flying_away:
            return
            
        # Actualizar posición según el patrón de vuelo
        if self.flight_pattern == 'straight':
            self.x += self.speed * self.direction
        elif self.flight_pattern == 'wave':
            self.x += self.speed * self.direction
            self.y += math.sin(self.pattern_offset) * 2
            self.pattern_offset += 0.1
        elif self.flight_pattern == 'zigzag':
            self.x += self.speed * self.direction
            if int(self.pattern_offset) % 30 == 0:
                self.direction *= -1
            self.pattern_offset += 1
        
        # Actualizar distancia recorrida
        self.distance_traveled += abs(self.speed * dt)
        
        # Actualizar animación de alas
        self.wing_flap_time += dt * self.wing_flap_speed
        
        # Verificar si el pato salió de la pantalla
        if self.x > self.screen_width + 50 or self.x < -50:
            self.is_flying_away = True
    
    def draw(self, screen: pygame.Surface) -> None:
        """Dibuja el pato en la pantalla."""
        if not self.is_alive:
            return
            
        # Calcular posición de dibujo
        draw_x = int(self.x)
        draw_y = int(self.y)
        
        # Usar sprites auténticos del Duck Hunt
        if self.is_flying_away:
            # Pato cayendo
            duck_sprite = pygame.Surface((16, 12), pygame.SRCALPHA)
            self._draw_authentic_duck_sprite(duck_sprite, "falling")
        else:
            # Pato volando - seleccionar color aleatorio
            duck_sprite = pygame.Surface((16, 12), pygame.SRCALPHA)
            color_type = random.choice(["blue", "green", "red"])
            self._draw_authentic_duck_sprite(duck_sprite, "flying", color_type)
        
        # Escalar el sprite para que se vea mejor
        duck_sprite = pygame.transform.scale(duck_sprite, (32, 24))
        
        # Aplicar animación de alas
        wing_offset = math.sin(self.wing_flap_time) * 2
        duck_sprite = pygame.transform.rotate(duck_sprite, wing_offset)
        
        screen.blit(duck_sprite, (draw_x, draw_y))
    
    def _draw_authentic_duck_sprite(self, surface: pygame.Surface, state: str, color_type: str = "blue") -> None:
        """Dibuja un sprite auténtico de pato (estilo NES)."""
        if state == "falling":
            # Pato cayendo
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
        else:
            # Pato volando
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
    
    def hit(self) -> int:
        """Marca el pato como golpeado y retorna la puntuación."""
        if not self.is_alive:
            return 0
            
        self.is_alive = False
        return self.calculate_score()
    
    def calculate_score(self) -> int:
        """Calcula la puntuación basada en la velocidad y distancia."""
        speed_bonus = int(self.speed * 20)
        distance_bonus = int(self.distance_traveled * 0.5)
        return self.base_score + speed_bonus + distance_bonus
    
    def get_rect(self) -> pygame.Rect:
        """Retorna el rectángulo de colisión del pato."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def is_off_screen(self) -> bool:
        """Verifica si el pato está fuera de la pantalla."""
        return self.x > self.screen_width + 50 or self.x < -50


class DuckManager:
    """Gestor de todos los patos en el juego."""
    
    def __init__(self, screen_width: int, screen_height: int, sprites=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.sprites = sprites
        self.ducks: List[Duck] = []
        self.last_spawn_time = 0
        self.spawn_interval = DUCK_SPAWN_INTERVAL
        
    def update(self, dt: float) -> None:
        """Actualiza todos los patos."""
        current_time = pygame.time.get_ticks() / 1000.0
        
        # Generar nuevos patos
        if (current_time - self.last_spawn_time > self.spawn_interval and 
            len(self.ducks) < MAX_DUCKS_ON_SCREEN):
            self.spawn_duck()
            self.last_spawn_time = current_time
        
        # Actualizar patos existentes
        for duck in self.ducks[:]:  # Usar slice para evitar problemas al modificar la lista
            duck.update(dt)
            if duck.is_off_screen():
                self.ducks.remove(duck)
    
    def draw(self, screen: pygame.Surface) -> None:
        """Dibuja todos los patos."""
        for duck in self.ducks:
            duck.draw(screen)
    
    def spawn_duck(self) -> None:
        """Genera un nuevo pato."""
        duck = Duck(self.screen_width, self.screen_height, sprites=self.sprites)
        self.ducks.append(duck)
    
    def check_hit(self, crosshair_pos: Tuple[float, float], 
                  crosshair_radius: float) -> List[int]:
        """Verifica si algún pato fue golpeado y retorna las puntuaciones."""
        scores = []
        for duck in self.ducks[:]:
            if duck.is_alive and not duck.is_flying_away:
                duck_center = (duck.x + duck.width//2, duck.y + duck.height//2)
                if distance(crosshair_pos, duck_center) <= crosshair_radius + duck.width//2:
                    score = duck.hit()
                    scores.append(score)
                    # Remover pato golpeado después de un breve delay
                    pygame.time.set_timer(pygame.USEREVENT + len(self.ducks), 100)
        
        return scores
    
    def get_alive_ducks(self) -> List[Duck]:
        """Retorna la lista de patos vivos."""
        return [duck for duck in self.ducks if duck.is_alive and not duck.is_flying_away]
    
    def clear_all(self) -> None:
        """Elimina todos los patos."""
        self.ducks.clear()
