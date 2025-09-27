"""
Sistema de calibración para el control por cámara
"""

import pygame
import time
import numpy as np
from typing import Tuple, List, Optional
from utils.config import *
from utils.helpers import normalize_hand_position


class CameraCalibration:
    """Sistema de calibración para optimizar el control por cámara."""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Datos de calibración
        self.calibration_points = []
        self.screen_points = []
        self.calibration_complete = False
        
        # Puntos de calibración en la pantalla
        self.target_points = [
            (screen_width * 0.1, screen_height * 0.1),   # Esquina superior izquierda
            (screen_width * 0.9, screen_height * 0.1),   # Esquina superior derecha
            (screen_width * 0.1, screen_height * 0.9),   # Esquina inferior izquierda
            (screen_width * 0.9, screen_height * 0.9),   # Esquina inferior derecha
            (screen_width * 0.5, screen_height * 0.5),   # Centro
        ]
        
        self.current_calibration_point = 0
        self.calibration_start_time = 0
        
    def start_calibration(self) -> None:
        """Inicia el proceso de calibración."""
        self.calibration_points.clear()
        self.screen_points.clear()
        self.current_calibration_point = 0
        self.calibration_start_time = time.time()
        self.calibration_complete = False
        
    def add_calibration_point(self, hand_pos: Tuple[float, float], 
                             screen_pos: Tuple[float, float]) -> bool:
        """Agrega un punto de calibración."""
        if self.current_calibration_point >= len(self.target_points):
            return False
            
        self.calibration_points.append(hand_pos)
        self.screen_points.append(screen_pos)
        self.current_calibration_point += 1
        
        return self.current_calibration_point >= len(self.target_points)
    
    def get_current_target(self) -> Tuple[float, float]:
        """Retorna el punto objetivo actual para la calibración."""
        if self.current_calibration_point >= len(self.target_points):
            return self.target_points[-1]
        return self.target_points[self.current_calibration_point]
    
    def is_calibration_complete(self) -> bool:
        """Verifica si la calibración está completa."""
        return self.calibration_complete
    
    def calculate_calibration_matrix(self) -> Optional[np.ndarray]:
        """Calcula la matriz de transformación para la calibración."""
        if len(self.calibration_points) < 3:
            return None
        
        try:
            # Convertir a arrays numpy
            hand_points = np.array(self.calibration_points)
            screen_points = np.array(self.screen_points)
            
            # Calcular transformación afín
            # Aplicar transformación de mínimos cuadrados
            n = len(hand_points)
            
            # Matriz de coeficientes
            A = np.column_stack([
                hand_points[:, 0],  # x
                hand_points[:, 1],  # y
                np.ones(n)          # término constante
            ])
            
            # Resolver para x
            x_coeffs = np.linalg.lstsq(A, screen_points[:, 0], rcond=None)[0]
            y_coeffs = np.linalg.lstsq(A, screen_points[:, 1], rcond=None)[0]
            
            # Crear matriz de transformación
            transform_matrix = np.array([
                [x_coeffs[0], x_coeffs[1], x_coeffs[2]],
                [y_coeffs[0], y_coeffs[1], y_coeffs[2]],
                [0, 0, 1]
            ])
            
            self.calibration_complete = True
            return transform_matrix
            
        except Exception as e:
            print(f"Error calculando matriz de calibración: {e}")
            return None
    
    def apply_calibration(self, hand_pos: Tuple[float, float], 
                        transform_matrix: np.ndarray) -> Tuple[float, float]:
        """Aplica la transformación de calibración a una posición de mano."""
        try:
            # Convertir a coordenadas homogéneas
            hand_homogeneous = np.array([hand_pos[0], hand_pos[1], 1])
            
            # Aplicar transformación
            screen_homogeneous = transform_matrix @ hand_homogeneous
            
            # Convertir de vuelta a coordenadas cartesianas
            screen_x = screen_homogeneous[0] / screen_homogeneous[2]
            screen_y = screen_homogeneous[1] / screen_homogeneous[2]
            
            # Limitar a los bordes de la pantalla
            screen_x = max(0, min(self.screen_width, screen_x))
            screen_y = max(0, min(self.screen_height, screen_y))
            
            return (screen_x, screen_y)
            
        except Exception as e:
            print(f"Error aplicando calibración: {e}")
            return hand_pos
    
    def draw_calibration_ui(self, screen: pygame.Surface, 
                          hand_pos: Optional[Tuple[float, float]]) -> None:
        """Dibuja la interfaz de calibración."""
        if self.current_calibration_point >= len(self.target_points):
            return
        
        # Obtener punto objetivo actual
        target_x, target_y = self.get_current_target()
        
        # Dibujar instrucciones
        font = pygame.font.Font(None, 36)
        instruction_text = f"Calibración {self.current_calibration_point + 1}/{len(self.target_points)}"
        text_surface = font.render(instruction_text, True, (0, 0, 0))
        screen.blit(text_surface, (10, 10))
        
        # Dibujar punto objetivo
        pygame.draw.circle(screen, (255, 0, 0), (int(target_x), int(target_y)), 20, 3)
        pygame.draw.circle(screen, (255, 0, 0), (int(target_x), int(target_y)), 5)
        
        # Dibujar posición de la mano si está disponible
        if hand_pos:
            pygame.draw.circle(screen, (0, 255, 0), (int(hand_pos[0]), int(hand_pos[1])), 10)
            
            # Verificar si está cerca del objetivo
            distance_to_target = np.sqrt((hand_pos[0] - target_x)**2 + (hand_pos[1] - target_y)**2)
            if distance_to_target < 30:
                # Mostrar mensaje de confirmación
                confirm_text = "¡Perfecto! Mantén la posición por 2 segundos"
                confirm_surface = font.render(confirm_text, True, (0, 255, 0))
                screen.blit(confirm_surface, (10, 50))
    
    def get_calibration_quality(self) -> float:
        """Evalúa la calidad de la calibración."""
        if len(self.calibration_points) < 3:
            return 0.0
        
        try:
            # Calcular dispersión de los puntos
            hand_points = np.array(self.calibration_points)
            screen_points = np.array(self.screen_points)
            
            # Calcular varianza
            hand_variance = np.var(hand_points, axis=0)
            screen_variance = np.var(screen_points, axis=0)
            
            # Calcular calidad (menor varianza = mejor calibración)
            hand_quality = 1.0 / (1.0 + np.mean(hand_variance))
            screen_quality = 1.0 / (1.0 + np.mean(screen_variance))
            
            return (hand_quality + screen_quality) / 2.0
            
        except Exception as e:
            print(f"Error evaluando calidad de calibración: {e}")
            return 0.0
