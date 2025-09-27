"""
Herramienta de entrenamiento de gestos para Duck Hunt
Ayuda a calibrar y mejorar la detección de gestos
"""

import pygame
import cv2
import time
import numpy as np
from camera.hand_tracker import HandTracker
from camera.gesture_detector import GestureDetector
from utils.config import *


class GestureTrainer:
    """Herramienta para entrenar y calibrar gestos."""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Entrenador de Gestos - Duck Hunt")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Componentes de detección
        self.hand_tracker = HandTracker()
        self.gesture_detector = GestureDetector()
        
        # Estado del entrenamiento
        self.training_mode = "calibration"
        self.gesture_count = 0
        self.successful_gestures = 0
        self.training_start_time = time.time()
        
        # Historial de gestos
        self.gesture_history = []
        self.confidence_history = []
        
        # Inicializar cámara
        if not self.hand_tracker.initialize_camera():
            print("Error: No se pudo inicializar la cámara")
            self.running = False
        else:
            self.running = True
    
    def draw_instructions(self):
        """Dibuja las instrucciones en pantalla."""
        instructions = {
            "calibration": [
                "MODO CALIBRACIÓN",
                "Mueve tu mano por toda la pantalla",
                "Asegúrate de que la cámara te detecte bien",
                "Presiona ESPACIO cuando termines"
            ],
            "gesture_training": [
                "MODO ENTRENAMIENTO DE GESTOS",
                "Haz el gesto de pinza (pulgar + índice)",
                f"Gestos exitosos: {self.successful_gestures}/{self.gesture_count}",
                "Presiona R para reiniciar, ESC para salir"
            ],
            "precision_test": [
                "MODO PRUEBA DE PRECISIÓN",
                "Apunta a los círculos que aparecen",
                "Haz el gesto de pinza para 'disparar'",
                "Presiona ESPACIO para comenzar"
            ]
        }
        
        current_instructions = instructions.get(self.training_mode, [])
        
        for i, instruction in enumerate(current_instructions):
            color = (255, 255, 255) if i == 0 else (200, 200, 200)
            text = self.font.render(instruction, True, color)
            self.screen.blit(text, (50, 50 + i * 40))
    
    def draw_hand_position(self, hand_pos):
        """Dibuja la posición de la mano."""
        if hand_pos:
            x, y = int(hand_pos[0]), int(hand_pos[1])
            
            # Dibujar círculo de la mano
            pygame.draw.circle(self.screen, (0, 255, 0), (x, y), 20, 3)
            pygame.draw.circle(self.screen, (0, 255, 0), (x, y), 5)
            
            # Dibujar coordenadas
            coord_text = f"({x}, {y})"
            text = self.small_font.render(coord_text, True, (255, 255, 255))
            self.screen.blit(text, (x + 25, y - 25))
    
    def draw_gesture_feedback(self):
        """Dibuja feedback sobre los gestos detectados."""
        if self.training_mode == "gesture_training":
            # Mostrar estado del gesto
            landmarks = self.hand_tracker.get_hand_landmarks()
            if landmarks:
                is_pinching = self.gesture_detector.detect_pinch_gesture(landmarks)
                
                if is_pinching:
                    pygame.draw.circle(self.screen, (255, 0, 0), 
                                      (WINDOW_WIDTH - 100, 100), 30)
                    text = self.font.render("¡GESTO!", True, (255, 0, 0))
                    self.screen.blit(text, (WINDOW_WIDTH - 200, 150))
                else:
                    pygame.draw.circle(self.screen, (0, 0, 255), 
                                      (WINDOW_WIDTH - 100, 100), 30)
                    text = self.font.render("Esperando...", True, (0, 0, 255))
                    self.screen.blit(text, (WINDOW_WIDTH - 200, 150))
    
    def draw_precision_targets(self):
        """Dibuja objetivos para la prueba de precisión."""
        if self.training_mode == "precision_test":
            # Generar objetivos aleatorios
            targets = [
                (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 4),
                (3 * WINDOW_WIDTH // 4, WINDOW_HEIGHT // 4),
                (WINDOW_WIDTH // 4, 3 * WINDOW_HEIGHT // 4),
                (3 * WINDOW_WIDTH // 4, 3 * WINDOW_HEIGHT // 4),
                (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
            ]
            
            for i, (x, y) in enumerate(targets):
                color = (255, 255, 0) if i < 3 else (255, 0, 255)
                pygame.draw.circle(self.screen, color, (x, y), 25, 3)
                pygame.draw.circle(self.screen, color, (x, y), 5)
    
    def draw_statistics(self):
        """Dibuja estadísticas del entrenamiento."""
        if self.training_mode == "gesture_training":
            # Calcular precisión
            accuracy = (self.successful_gestures / max(1, self.gesture_count)) * 100
            
            stats = [
                f"Precisión: {accuracy:.1f}%",
                f"Tiempo: {int(time.time() - self.training_start_time)}s",
                f"Confianza: {self.gesture_detector.get_gesture_confidence():.2f}"
            ]
            
            for i, stat in enumerate(stats):
                text = self.small_font.render(stat, True, (255, 255, 255))
                self.screen.blit(text, (50, WINDOW_HEIGHT - 100 + i * 25))
    
    def handle_events(self):
        """Maneja los eventos del entrenador."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    if self.training_mode == "calibration":
                        self.training_mode = "gesture_training"
                        self.training_start_time = time.time()
                    elif self.training_mode == "precision_test":
                        self.training_mode = "gesture_training"
                elif event.key == pygame.K_r:
                    if self.training_mode == "gesture_training":
                        self.gesture_count = 0
                        self.successful_gestures = 0
                        self.training_start_time = time.time()
                elif event.key == pygame.K_p:
                    self.training_mode = "precision_test"
    
    def update_gesture_training(self):
        """Actualiza el entrenamiento de gestos."""
        landmarks = self.hand_tracker.get_hand_landmarks()
        if landmarks and self.gesture_detector.is_gesture_ready():
            is_pinching = self.gesture_detector.detect_pinch_gesture(landmarks)
            
            if is_pinching:
                self.gesture_count += 1
                self.successful_gestures += 1
                
                # Registrar en historial
                confidence = self.gesture_detector.get_gesture_confidence()
                self.gesture_history.append(time.time())
                self.confidence_history.append(confidence)
    
    def run(self):
        """Ejecuta el entrenador de gestos."""
        print("=== ENTRENADOR DE GESTOS DUCK HUNT ===")
        print("Instrucciones:")
        print("1. Calibración: Mueve tu mano por toda la pantalla")
        print("2. Entrenamiento: Practica el gesto de pinza")
        print("3. Precisión: Apunta a objetivos específicos")
        print("Controles: ESPACIO (siguiente), R (reiniciar), ESC (salir)")
        
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            
            # Procesar cámara
            frame = self.hand_tracker.process_frame()
            hand_pos = self.hand_tracker.get_hand_position()
            
            # Actualizar historial de gestos
            if hand_pos:
                self.gesture_detector.update_gesture_history(hand_pos)
            
            # Actualizar entrenamiento
            if self.training_mode == "gesture_training":
                self.update_gesture_training()
            
            # Manejar eventos
            self.handle_events()
            
            # Dibujar
            self.screen.fill((0, 0, 0))
            
            self.draw_instructions()
            self.draw_hand_position(hand_pos)
            self.draw_gesture_feedback()
            self.draw_precision_targets()
            self.draw_statistics()
            
            pygame.display.flip()
        
        # Limpiar recursos
        self.hand_tracker.release()
        pygame.quit()
        
        # Mostrar resultados finales
        if self.gesture_count > 0:
            final_accuracy = (self.successful_gestures / self.gesture_count) * 100
            print(f"\n=== RESULTADOS DEL ENTRENAMIENTO ===")
            print(f"Gestos intentados: {self.gesture_count}")
            print(f"Gestos exitosos: {self.successful_gestures}")
            print(f"Precisión final: {final_accuracy:.1f}%")
            print(f"Confianza promedio: {np.mean(self.confidence_history):.2f}")
            
            if final_accuracy >= 80:
                print("¡Excelente! Tu precisión es muy buena.")
            elif final_accuracy >= 60:
                print("Buen trabajo. Sigue practicando para mejorar.")
            else:
                print("Necesitas más práctica. Asegúrate de hacer el gesto claramente.")


def main():
    """Función principal."""
    trainer = GestureTrainer()
    trainer.run()


if __name__ == "__main__":
    main()
