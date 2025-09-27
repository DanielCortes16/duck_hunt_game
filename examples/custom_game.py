"""
Ejemplo de personalización del juego Duck Hunt
Muestra cómo crear variaciones del juego
"""

import pygame
import sys
import random
import math
from game.game_engine import GameEngine
from camera.hand_tracker import HandTracker
from camera.gesture_detector import GestureDetector
from utils.config import *


class CustomDuckHunt(GameEngine):
    """Versión personalizada de Duck Hunt con características adicionales."""
    
    def __init__(self):
        super().__init__()
        
        # Características personalizadas
        self.power_ups = []
        self.combo_multiplier = 1
        self.combo_timer = 0
        self.max_combo_time = 2.0
        
        # Nuevos tipos de patos
        self.special_ducks = []
        
    def add_power_up(self, x: float, y: float, power_type: str):
        """Agrega un power-up al juego."""
        power_up = {
            "x": x,
            "y": y,
            "type": power_type,
            "collected": False,
            "timer": 0
        }
        self.power_ups.append(power_up)
    
    def update_power_ups(self, dt: float):
        """Actualiza los power-ups."""
        for power_up in self.power_ups[:]:
            power_up["timer"] += dt
            
            # Remover power-ups expirados
            if power_up["timer"] > 10.0:  # 10 segundos de vida
                self.power_ups.remove(power_up)
    
    def draw_power_ups(self):
        """Dibuja los power-ups en pantalla."""
        for power_up in self.power_ups:
            if not power_up["collected"]:
                x, y = int(power_up["x"]), int(power_up["y"])
                
                # Dibujar según el tipo
                if power_up["type"] == "rapid_fire":
                    pygame.draw.circle(self.screen, (255, 0, 0), (x, y), 15)
                    # Dibujar icono de fuego rápido
                    pygame.draw.polygon(self.screen, (255, 255, 0), [
                        (x-5, y-10), (x+5, y-10), (x+8, y), (x+5, y+10), (x-5, y+10), (x-8, y)
                    ])
                elif power_up["type"] == "extra_life":
                    pygame.draw.circle(self.screen, (0, 255, 0), (x, y), 15)
                    # Dibujar icono de corazón
                    pygame.draw.circle(self.screen, (255, 255, 255), (x-3, y-3), 3)
                    pygame.draw.circle(self.screen, (255, 255, 255), (x+3, y-3), 3)
                    pygame.draw.polygon(self.screen, (255, 255, 255), [
                        (x, y+5), (x-5, y-2), (x+5, y-2)
                    ])
    
    def check_power_up_collision(self, crosshair_pos, crosshair_radius):
        """Verifica colisiones con power-ups."""
        for power_up in self.power_ups[:]:
            if not power_up["collected"]:
                power_up_pos = (power_up["x"], power_up["y"])
                distance = ((crosshair_pos[0] - power_up_pos[0])**2 + 
                           (crosshair_pos[1] - power_up_pos[1])**2)**0.5
                
                if distance <= crosshair_radius + 15:
                    self.collect_power_up(power_up)
    
    def collect_power_up(self, power_up):
        """Recolecta un power-up."""
        power_up["collected"] = True
        
        if power_up["type"] == "rapid_fire":
            # Activar fuego rápido por 5 segundos
            self.shot_cooldown = 0.1
            pygame.time.set_timer(pygame.USEREVENT + 100, 5000)  # Timer para desactivar
            
        elif power_up["type"] == "extra_life":
            # Dar vida extra
            self.lives += 1
            
        self.power_ups.remove(power_up)
    
    def update_combo_system(self, dt: float):
        """Actualiza el sistema de combo."""
        if self.combo_timer > 0:
            self.combo_timer -= dt
            if self.combo_timer <= 0:
                self.combo_multiplier = 1
    
    def add_combo(self):
        """Agrega combo por golpe consecutivo."""
        self.combo_timer = self.max_combo_time
        self.combo_multiplier = min(5, self.combo_multiplier + 1)
    
    def reset_combo(self):
        """Resetea el combo."""
        self.combo_multiplier = 1
        self.combo_timer = 0
    
    def draw_combo(self):
        """Dibuja el indicador de combo."""
        if self.combo_multiplier > 1:
            combo_text = f"COMBO x{self.combo_multiplier}"
            color = (255, 255, 0) if self.combo_multiplier < 3 else (255, 0, 0)
            
            text = self.font_medium.render(combo_text, True, color)
            self.screen.blit(text, (WINDOW_WIDTH - 200, 10))
    
    def update(self, dt: float):
        """Actualiza la lógica del juego personalizada."""
        super().update(dt)
        
        # Actualizar sistemas personalizados
        self.update_power_ups(dt)
        self.update_combo_system(dt)
        
        # Generar power-ups aleatoriamente
        if len(self.power_ups) < 2 and pygame.time.get_ticks() % 10000 < 100:
            import random
            x = random.randint(50, WINDOW_WIDTH - 50)
            y = random.randint(100, WINDOW_HEIGHT - 200)
            power_type = random.choice(["rapid_fire", "extra_life"])
            self.add_power_up(x, y, power_type)
    
    def draw(self):
        """Dibuja el juego personalizado."""
        super().draw()
        
        if self.game_state == "playing":
            self.draw_power_ups()
            self.draw_combo()
    
    def shoot(self):
        """Disparo personalizado con sistema de combo."""
        super().shoot()
        
        # Verificar colisiones con power-ups
        crosshair_pos = self.crosshair.get_position()
        crosshair_radius = self.crosshair.get_radius()
        self.check_power_up_collision(crosshair_pos, crosshair_radius)
        
        # Actualizar combo
        if self.shots_hit > 0 and (self.shots_hit % 3) == 0:
            self.add_combo()


def create_night_mode():
    """Crea una versión nocturna del juego."""
    # Modificar colores para modo nocturno
    global BACKGROUND_COLOR, GRASS_COLOR, DUCK_COLOR
    BACKGROUND_COLOR = (25, 25, 112)  # Azul noche
    GRASS_COLOR = (0, 50, 0)  # Verde oscuro
    DUCK_COLOR = (255, 140, 0)  # Naranja más brillante


def create_rainbow_mode():
    """Crea un modo arcoíris con colores cambiantes."""
    import math
    
    class RainbowDuckHunt(CustomDuckHunt):
        def __init__(self):
            super().__init__()
            self.rainbow_time = 0
        
        def update(self, dt: float):
            super().update(dt)
            self.rainbow_time += dt
        
        def draw(self):
            # Aplicar efecto arcoíris a los colores
            rainbow_factor = math.sin(self.rainbow_time * 2) * 0.5 + 0.5
            
            # Modificar colores dinámicamente
            original_bg = (135, 206, 235)
            rainbow_bg = (
                int(original_bg[0] * rainbow_factor),
                int(original_bg[1] * rainbow_factor),
                int(original_bg[2] * rainbow_factor)
            )
            
            # Crear fondo con gradiente arcoíris
            for y in range(WINDOW_HEIGHT):
                color_intensity = y / WINDOW_HEIGHT
                r = int(255 * color_intensity * rainbow_factor)
                g = int(255 * (1 - color_intensity) * rainbow_factor)
                b = int(255 * rainbow_factor)
                pygame.draw.line(self.screen, (r, g, b), (0, y), (WINDOW_WIDTH, y))
            
            # Dibujar resto del juego
            super().draw()
    
    return RainbowDuckHunt()


def main():
    """Función principal para probar el juego personalizado."""
    print("=== DUCK HUNT PERSONALIZADO ===")
    print("Características adicionales:")
    print("- Power-ups (fuego rápido, vidas extra)")
    print("- Sistema de combo")
    print("- Modo nocturno")
    print("- Modo arcoíris")
    
    # Crear juego personalizado
    game = CustomDuckHunt()
    
    # Activar modo nocturno (opcional)
    # create_night_mode()
    
    # O activar modo arcoíris (opcional)
    # game = create_rainbow_mode()
    
    # Ejecutar juego
    game.run()


if __name__ == "__main__":
    main()
