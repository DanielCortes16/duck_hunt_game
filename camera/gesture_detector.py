"""
Sistema de detección de gestos para Duck Hunt
"""

import numpy as np
import time
from typing import Tuple, Optional
from utils.config import *
from utils.helpers import distance


class GestureDetector:
    """Clase para detectar gestos de mano."""
    
    def __init__(self):
        # Estado del gesto
        self.is_pinching = False
        self.last_pinch_time = 0
        self.pinch_start_time = 0
        
        # Configuración de detección
        self.pinch_threshold = PINCH_THRESHOLD
        self.gesture_debounce = GESTURE_DEBOUNCE_TIME
        self.min_pinch_duration = 0.1  # Duración mínima del gesto
        
        # Historial de gestos
        self.gesture_history = []
        self.max_history = 10
        
    def detect_pinch_gesture(self, landmarks) -> bool:
        """Detecta el gesto de pinza (pulgar e índice juntos)."""
        if not landmarks:
            return False
        
        try:
            # Obtener puntos clave
            thumb_tip = landmarks.landmark[4]  # Pulgar
            index_tip = landmarks.landmark[8]  # Índice
            thumb_ip = landmarks.landmark[3]   # Articulación del pulgar
            index_pip = landmarks.landmark[6]  # Articulación del índice
            
            # Calcular distancia entre pulgar e índice
            thumb_pos = np.array([thumb_tip.x, thumb_tip.y])
            index_pos = np.array([index_tip.x, index_tip.y])
            pinch_distance = np.linalg.norm(thumb_pos - index_pos)
            
            # Verificar si los dedos están doblados (gesto natural de pinza)
            thumb_bent = self._is_finger_bent(landmarks, 4)  # Pulgar
            index_bent = self._is_finger_bent(landmarks, 8)  # Índice
            
            # Detectar pinza
            is_pinching_now = (pinch_distance < self.pinch_threshold and 
                             thumb_bent and index_bent)
            
            # Actualizar estado
            current_time = time.time()
            
            if is_pinching_now and not self.is_pinching:
                # Inicio del gesto
                self.is_pinching = True
                self.pinch_start_time = current_time
                return False  # No disparar inmediatamente
                
            elif is_pinching_now and self.is_pinching:
                # Mantener el gesto
                pinch_duration = current_time - self.pinch_start_time
                if pinch_duration >= self.min_pinch_duration:
                    # Gesto válido
                    if current_time - self.last_pinch_time > self.gesture_debounce:
                        self.last_pinch_time = current_time
                        return True
                        
            elif not is_pinching_now and self.is_pinching:
                # Fin del gesto
                self.is_pinching = False
                
            return False
            
        except Exception as e:
            print(f"Error en detección de gesto: {e}")
            return False
    
    def _is_finger_bent(self, landmarks, finger_tip_id: int) -> bool:
        """Verifica si un dedo está doblado."""
        try:
            # IDs de las articulaciones del dedo
            finger_joints = {
                4: [3, 2, 1],      # Pulgar
                8: [7, 6, 5],      # Índice
                12: [11, 10, 9],   # Medio
                16: [15, 14, 13],  # Anular
                20: [19, 18, 17]   # Meñique
            }
            
            if finger_tip_id not in finger_joints:
                return False
            
            tip = landmarks.landmark[finger_tip_id]
            joints = [landmarks.landmark[joint_id] for joint_id in finger_joints[finger_tip_id]]
            
            # Calcular ángulo entre articulaciones
            if len(joints) >= 2:
                # Vector del tip a la primera articulación
                v1 = np.array([tip.x - joints[0].x, tip.y - joints[0].y])
                # Vector de la primera a la segunda articulación
                v2 = np.array([joints[0].x - joints[1].x, joints[0].y - joints[1].y])
                
                # Calcular ángulo
                cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
                angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
                
                # El dedo está doblado si el ángulo es menor a 90 grados
                return angle < np.pi / 2
                
            return False
            
        except Exception as e:
            print(f"Error verificando dedo doblado: {e}")
            return False
    
    def detect_swipe_gesture(self, landmarks) -> Optional[str]:
        """Detecta gestos de deslizamiento (opcional para futuras funcionalidades)."""
        if not landmarks or len(self.gesture_history) < 5:
            return None
        
        # Analizar movimiento reciente
        recent_positions = self.gesture_history[-5:]
        
        # Calcular dirección del movimiento
        start_pos = recent_positions[0]
        end_pos = recent_positions[-1]
        
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        
        # Determinar dirección
        if abs(dx) > abs(dy):
            return "left" if dx < 0 else "right"
        else:
            return "up" if dy < 0 else "down"
    
    def update_gesture_history(self, position: Tuple[float, float]) -> None:
        """Actualiza el historial de posiciones para detección de gestos."""
        if position:
            self.gesture_history.append(position)
            if len(self.gesture_history) > self.max_history:
                self.gesture_history.pop(0)
    
    def get_gesture_confidence(self) -> float:
        """Retorna la confianza en la detección de gestos."""
        if not self.gesture_history:
            return 0.0
        
        # Calcular estabilidad de la posición
        if len(self.gesture_history) < 3:
            return 0.0
        
        recent_positions = self.gesture_history[-3:]
        distances = []
        
        for i in range(1, len(recent_positions)):
            dist = distance(recent_positions[i-1], recent_positions[i])
            distances.append(dist)
        
        # Menor variación = mayor confianza
        avg_distance = np.mean(distances)
        confidence = max(0.0, 1.0 - avg_distance * 10)  # Ajustar factor según necesidad
        
        return min(1.0, confidence)
    
    def reset_gesture_state(self) -> None:
        """Resetea el estado de detección de gestos."""
        self.is_pinching = False
        self.gesture_history.clear()
    
    def is_gesture_ready(self) -> bool:
        """Verifica si el sistema está listo para detectar gestos."""
        return len(self.gesture_history) >= 3
    
    def get_gesture_statistics(self) -> dict:
        """Retorna estadísticas de los gestos detectados."""
        if not self.gesture_history:
            return {}
        
        positions = np.array(self.gesture_history)
        
        return {
            "position_variance": np.var(positions, axis=0).tolist(),
            "movement_speed": np.mean(np.linalg.norm(np.diff(positions, axis=0), axis=1)),
            "gesture_confidence": self.get_gesture_confidence(),
            "history_length": len(self.gesture_history)
        }
