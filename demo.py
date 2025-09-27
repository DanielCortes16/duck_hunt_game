"""
Demostración del juego Duck Hunt con Control por Cámara
Muestra las capacidades del sistema
"""

import pygame
import sys
import time
from game.game_engine import GameEngine
from camera.hand_tracker import HandTracker
from camera.gesture_detector import GestureDetector
from utils.config import *


class DuckHuntDemo:
    """Demostración interactiva del juego."""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Duck Hunt Demo - Control por Cámara")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.medium_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Componentes
        self.hand_tracker = HandTracker()
        self.gesture_detector = GestureDetector()
        
        # Estado de la demo
        self.demo_mode = "intro"
        self.demo_start_time = time.time()
        self.current_demo_step = 0
        
        # Pasos de la demo
        self.demo_steps = [
            {
                "title": "Bienvenido a Duck Hunt",
                "description": "Control por cámara web con gestos de mano",
                "duration": 3.0
            },
            {
                "title": "Detección de Manos",
                "description": "Mueve tu mano frente a la cámara",
                "duration": 5.0
            },
            {
                "title": "Gesto de Disparo",
                "description": "Junta pulgar e índice para disparar",
                "duration": 5.0
            },
            {
                "title": "¡Jugar!",
                "description": "Presiona ESPACIO para comenzar el juego",
                "duration": 0
            }
        ]
        
        # Inicializar cámara
        self.camera_ready = False
        if self.hand_tracker.initialize_camera():
            self.camera_ready = True
            print("Cámara inicializada correctamente")
        else:
            print("Advertencia: No se pudo inicializar la cámara")
    
    def draw_demo_screen(self):
        """Dibuja la pantalla de demostración."""
        self.screen.fill((0, 0, 50))
        
        current_time = time.time() - self.demo_start_time
        step = self.demo_steps[self.current_demo_step]
        
        # Título
        title_text = self.font.render(step["title"], True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100))
        self.screen.blit(title_text, title_rect)
        
        # Descripción
        desc_text = self.medium_font.render(step["description"], True, (200, 200, 200))
        desc_rect = desc_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
        self.screen.blit(desc_text, desc_rect)
        
        # Mostrar información de la cámara
        if self.camera_ready:
            hand_pos = self.hand_tracker.get_hand_position()
            if hand_pos:
                # Dibujar posición de la mano
                x, y = int(hand_pos[0]), int(hand_pos[1])
                pygame.draw.circle(self.screen, (0, 255, 0), (x, y), 20, 3)
                pygame.draw.circle(self.screen, (0, 255, 0), (x, y), 5)
                
                # Mostrar coordenadas
                coord_text = f"Posición: ({x}, {y})"
                coord_surface = self.small_font.render(coord_text, True, (255, 255, 255))
                self.screen.blit(coord_surface, (x + 25, y - 25))
                
                # Detectar gesto
                landmarks = self.hand_tracker.get_hand_landmarks()
                if landmarks and self.gesture_detector.is_gesture_ready():
                    is_pinching = self.gesture_detector.detect_pinch_gesture(landmarks)
                    if is_pinching:
                        gesture_text = "¡GESTO DETECTADO!"
                        gesture_surface = self.medium_font.render(gesture_text, True, (255, 0, 0))
                        self.screen.blit(gesture_surface, (WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 + 50))
            else:
                no_hand_text = "Mueve tu mano frente a la cámara"
                no_hand_surface = self.medium_font.render(no_hand_text, True, (255, 255, 0))
                self.screen.blit(no_hand_surface, (WINDOW_WIDTH//2 - 200, WINDOW_HEIGHT//2 + 50))
        else:
            camera_error_text = "Cámara no disponible"
            camera_error_surface = self.medium_font.render(camera_error_text, True, (255, 0, 0))
            self.screen.blit(camera_error_surface, (WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 + 50))
        
        # Mostrar progreso
        progress_text = f"Paso {self.current_demo_step + 1}/{len(self.demo_steps)}"
        progress_surface = self.small_font.render(progress_text, True, (150, 150, 150))
        self.screen.blit(progress_surface, (10, 10))
        
        # Instrucciones
        if self.current_demo_step < len(self.demo_steps) - 1:
            instruction_text = "Presiona ESPACIO para continuar"
        else:
            instruction_text = "Presiona ESPACIO para jugar o ESC para salir"
        
        instruction_surface = self.small_font.render(instruction_text, True, (255, 255, 255))
        self.screen.blit(instruction_surface, (10, WINDOW_HEIGHT - 30))
    
    def update_demo(self):
        """Actualiza la lógica de la demo."""
        current_time = time.time() - self.demo_start_time
        step = self.demo_steps[self.current_demo_step]
        
        # Procesar cámara
        if self.camera_ready:
            frame = self.hand_tracker.process_frame()
            hand_pos = self.hand_tracker.get_hand_position()
            
            if hand_pos:
                self.gesture_detector.update_gesture_history(hand_pos)
        
        # Avanzar automáticamente si hay duración
        if step["duration"] > 0 and current_time >= step["duration"]:
            self.next_demo_step()
    
    def next_demo_step(self):
        """Avanza al siguiente paso de la demo."""
        self.current_demo_step += 1
        self.demo_start_time = time.time()
        
        if self.current_demo_step >= len(self.demo_steps):
            self.current_demo_step = len(self.demo_steps) - 1
    
    def handle_events(self):
        """Maneja los eventos de la demo."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    if self.current_demo_step < len(self.demo_steps) - 1:
                        self.next_demo_step()
                    else:
                        # Iniciar el juego real
                        self.start_game()
                        return False
        return True
    
    def start_game(self):
        """Inicia el juego real."""
        print("Iniciando juego Duck Hunt...")
        
        # Crear y ejecutar el juego
        from main import DuckHuntCamera
        game = DuckHuntCamera()
        game.run()
    
    def run(self):
        """Ejecuta la demostración."""
        print("=== DEMOSTRACIÓN DUCK HUNT ===")
        print("Esta demo te mostrará las capacidades del juego")
        print("Controles: ESPACIO (continuar), ESC (salir)")
        
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0
            
            # Actualizar demo
            self.update_demo()
            
            # Manejar eventos
            running = self.handle_events()
            
            # Dibujar
            self.draw_demo_screen()
            pygame.display.flip()
        
        # Limpiar recursos
        if self.camera_ready:
            self.hand_tracker.release()
        pygame.quit()


def main():
    """Función principal de la demo."""
    print("=== DUCK HUNT - DEMOSTRACIÓN ===")
    print("Esta demostración te mostrará cómo funciona el control por cámara")
    print("Asegúrate de tener una cámara web conectada y buena iluminación")
    
    demo = DuckHuntDemo()
    demo.run()


if __name__ == "__main__":
    main()
