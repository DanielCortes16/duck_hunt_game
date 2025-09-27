"""
Motor principal del juego Duck Hunt
"""

import pygame
import sys
import time
import random
from typing import Tuple, List
from utils.config import *
from utils.helpers import create_gradient_background, draw_text
from utils.sound_manager import SoundManager
from .duck import DuckManager
from .crosshair import Crosshair
from .dog import Dog
from .authentic_sprites import AuthenticDuckHuntSprites


class GameEngine:
    """Motor principal del juego Duck Hunt."""
    
    def __init__(self):
        # Inicializar Pygame
        pygame.init()
        
        # Configurar ventana
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Duck Hunt - Control por Cámara")
        
        # Reloj para control de FPS
        self.clock = pygame.time.Clock()
        
        # Fuentes
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Estado del juego
        self.running = True
        self.game_state = "menu"  # menu, playing, game_over
        self.score = 0
        self.lives = INITIAL_LIVES
        self.level = 1
        
        # Componentes del juego
        self.sprites = AuthenticDuckHuntSprites()
        self.duck_manager = DuckManager(WINDOW_WIDTH, WINDOW_HEIGHT, sprites=self.sprites)
        self.crosshair = Crosshair(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.dog = Dog(WINDOW_WIDTH, WINDOW_HEIGHT, sprites=self.sprites)
        
        # Sistema de sonidos
        self.sound_manager = SoundManager()
        
        # Sprites auténticos
        self.sprites = AuthenticDuckHuntSprites()
        
        # Fondo auténtico
        self.background = self.sprites.create_authentic_background(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.bushes = self._create_bushes()
        
        # Control de tiempo
        self.last_shot_time = 0
        self.shot_cooldown = 0.5  # Tiempo mínimo entre disparos
        
        # Estadísticas
        self.shots_fired = 0
        self.shots_hit = 0
        self.ducks_missed = 0
        
    def _create_bushes(self) -> List[pygame.Rect]:
        """Crea los arbustos en el fondo."""
        bushes = []
        bush_width = 80
        bush_height = 60
        
        # Crear varios arbustos en la parte inferior
        for i in range(5):
            x = i * (WINDOW_WIDTH // 5) + random.randint(-20, 20)
            y = WINDOW_HEIGHT - bush_height - random.randint(0, 20)
            bushes.append(pygame.Rect(x, y, bush_width, bush_height))
        
        return bushes
    
    def handle_events(self) -> None:
        """Maneja los eventos del juego."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "playing":
                        self.game_state = "menu"
                    else:
                        self.running = False
                elif event.key == pygame.K_SPACE:
                    if self.game_state == "menu":
                        self.start_new_game()
                    elif self.game_state == "game_over":
                        self.start_new_game()
                elif event.key == pygame.K_r:
                    if self.game_state == "playing":
                        self.start_new_game()
    
    def handle_camera_control(self, hand_position: Tuple[float, float], 
                            shoot_gesture: bool) -> None:
        """Maneja el control por cámara."""
        if self.game_state != "playing":
            return
            
        # Actualizar posición de la mira
        if hand_position:
            self.crosshair.update_position(hand_position[0], hand_position[1])
        
        # Manejar disparo
        if shoot_gesture and self.crosshair.is_ready_to_shoot():
            current_time = time.time()
            if current_time - self.last_shot_time > self.shot_cooldown:
                self.shoot()
                self.last_shot_time = current_time
    
    def shoot(self) -> None:
        """Ejecuta un disparo."""
        self.shots_fired += 1
        
        # Sonido de disparo
        self.sound_manager.play_shot()
        
        # Animar la mira
        self.crosshair.shoot()
        
        # Verificar colisiones con patos
        crosshair_pos = self.crosshair.get_position()
        crosshair_radius = self.crosshair.get_radius()
        
        scores = self.duck_manager.check_hit(crosshair_pos, crosshair_radius)
        
        if scores:
            # Pato golpeado
            self.shots_hit += 1
            total_score = sum(scores)
            self.score += total_score
            
            # Sonidos de impacto
            self.sound_manager.play_hit()
            self.sound_manager.play_duck_quack()
            
            # Hacer reír al perro
            self.dog.start_laughing()
            self.sound_manager.play_dog_laugh()
            
            # Verificar si se completó el nivel
            if len(self.duck_manager.get_alive_ducks()) == 0:
                self.next_level()
        else:
            # Disparo fallido
            self.ducks_missed += 1
            self.sound_manager.play_miss()
            if self.ducks_missed >= 3:  # Perder vida después de 3 fallos
                self.lose_life()
    
    def lose_life(self) -> None:
        """El jugador pierde una vida."""
        self.lives -= 1
        self.ducks_missed = 0
        
        if self.lives <= 0:
            self.game_over()
        else:
            # Hacer reír al perro por fallar
            self.dog.start_laughing()
    
    def next_level(self) -> None:
        """Avanza al siguiente nivel."""
        self.level += 1
        self.ducks_missed = 0
        
        # Sonido de nivel completado
        self.sound_manager.play_level_complete()
        
        # Aumentar dificultad
        global DEFAULT_DUCK_SPEED
        DEFAULT_DUCK_SPEED += 0.5
        
        # Limpiar patos actuales
        self.duck_manager.clear_all()
    
    def start_new_game(self) -> None:
        """Inicia una nueva partida."""
        self.game_state = "playing"
        self.score = 0
        self.lives = INITIAL_LIVES
        self.level = 1
        self.shots_fired = 0
        self.shots_hit = 0
        self.ducks_missed = 0
        
        # Sonido de inicio de juego
        self.sound_manager.play_game_start()
        
        # Resetear componentes
        self.duck_manager.clear_all()
        self.crosshair = Crosshair(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.dog = Dog(WINDOW_WIDTH, WINDOW_HEIGHT, sprites=self.sprites)
        
        # Resetear dificultad
        global DEFAULT_DUCK_SPEED
        DEFAULT_DUCK_SPEED = 2
    
    def game_over(self) -> None:
        """Termina el juego."""
        self.game_state = "game_over"
        self.dog.start_laughing()
        self.sound_manager.play_game_over()
    
    def update(self, dt: float) -> None:
        """Actualiza la lógica del juego."""
        if self.game_state != "playing":
            return
            
        # Actualizar componentes
        self.duck_manager.update(dt)
        self.crosshair.update(dt)
        self.dog.update(dt)
    
    def draw(self) -> None:
        """Dibuja todos los elementos del juego."""
        # Limpiar pantalla
        self.screen.blit(self.background, (0, 0))
        
        # Dibujar arbustos con sprites auténticos
        for bush in self.bushes:
            bush_sprite = self.sprites.get_sprite('bush_large')
            self.screen.blit(bush_sprite, (bush.x, bush.y))
        
        if self.game_state == "menu":
            self._draw_menu()
        elif self.game_state == "playing":
            self._draw_game()
        elif self.game_state == "game_over":
            self._draw_game_over()
        
        # Actualizar pantalla
        pygame.display.flip()
    
    def _draw_menu(self) -> None:
        """Dibuja el menú principal."""
        # Título
        title_text = self.font_large.render("DUCK HUNT", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100))
        self.screen.blit(title_text, title_rect)
        
        # Instrucciones
        instructions = [
            "Control por Cámara Web",
            "Mueve tu mano para controlar la mira",
            "Junta pulgar e índice para disparar",
            "",
            "Presiona ESPACIO para comenzar",
            "Presiona ESC para salir"
        ]
        
        for i, instruction in enumerate(instructions):
            color = (0, 0, 0) if instruction else (100, 100, 100)
            text = self.font_medium.render(instruction, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + i * 40))
            self.screen.blit(text, text_rect)
    
    def _draw_game(self) -> None:
        """Dibuja el juego en curso."""
        # Dibujar patos
        self.duck_manager.draw(self.screen)
        
        # Dibujar perro
        self.dog.draw(self.screen)
        
        # Dibujar mira
        self.crosshair.draw(self.screen)
        
        # Dibujar HUD
        self._draw_hud()
    
    def _draw_game_over(self) -> None:
        """Dibuja la pantalla de game over."""
        # Fondo semi-transparente
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Dibujar perro riéndose
        self.dog.draw(self.screen)
        
        # Texto de game over
        game_over_text = self.font_large.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Estadísticas finales
        stats = [
            f"Puntuación Final: {self.score}",
            f"Precisión: {(self.shots_hit/max(1, self.shots_fired)*100):.1f}%",
            f"Nivel Alcanzado: {self.level}",
            "",
            "Presiona ESPACIO para jugar de nuevo",
            "Presiona ESC para salir"
        ]
        
        for i, stat in enumerate(stats):
            color = (255, 255, 255) if stat else (150, 150, 150)
            text = self.font_medium.render(stat, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + i * 40))
            self.screen.blit(text, text_rect)
    
    def _draw_hud(self) -> None:
        """Dibuja la interfaz de usuario."""
        # Puntuación
        score_text = self.font_medium.render(f"Puntuación: {self.score}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))
        
        # Vidas
        lives_text = self.font_medium.render(f"Vidas: {self.lives}", True, (0, 0, 0))
        self.screen.blit(lives_text, (10, 50))
        
        # Nivel
        level_text = self.font_medium.render(f"Nivel: {self.level}", True, (0, 0, 0))
        self.screen.blit(level_text, (10, 90))
        
        # Precisión
        if self.shots_fired > 0:
            accuracy = (self.shots_hit / self.shots_fired) * 100
            accuracy_text = self.font_small.render(f"Precisión: {accuracy:.1f}%", True, (0, 0, 0))
            self.screen.blit(accuracy_text, (10, 130))
        
        # Patos restantes
        alive_ducks = len(self.duck_manager.get_alive_ducks())
        ducks_text = self.font_small.render(f"Patos: {alive_ducks}", True, (0, 0, 0))
        self.screen.blit(ducks_text, (10, 160))
    
    def run(self) -> None:
        """Bucle principal del juego."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time en segundos
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()
        sys.exit()
