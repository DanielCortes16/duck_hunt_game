"""
Sistema de seguimiento de manos usando MediaPipe
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Tuple, Optional, List
from utils.config import *
from utils.helpers import normalize_hand_position


class HandTracker:
    """Clase para el seguimiento de manos con MediaPipe."""
    
    def __init__(self):
        # Inicializar MediaPipe
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Configurar detección de manos
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,  # Solo una mano para el control
            min_detection_confidence=HAND_DETECTION_CONFIDENCE,
            min_tracking_confidence=HAND_DETECTION_CONFIDENCE
        )
        
        # Cámara
        self.cap = None
        self.camera_width = CAMERA_WIDTH
        self.camera_height = CAMERA_HEIGHT
        
        # Estado de la mano
        self.hand_landmarks = None
        self.hand_position = None
        self.is_hand_detected = False
        
        # Historial para suavizado
        self.position_history = []
        self.max_history = 5
        
    def initialize_camera(self) -> bool:
        """Inicializa la cámara web."""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                return False
                
            # Configurar resolución
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_height)
            
            return True
        except Exception as e:
            print(f"Error al inicializar la cámara: {e}")
            return False
    
    def get_hand_position(self) -> Optional[Tuple[float, float]]:
        """Obtiene la posición actual de la mano."""
        return self.hand_position
    
    def is_hand_visible(self) -> bool:
        """Verifica si hay una mano visible."""
        return self.is_hand_detected
    
    def process_frame(self) -> Optional[np.ndarray]:
        """Procesa un frame de la cámara y detecta la mano."""
        if not self.cap or not self.cap.isOpened():
            return None
            
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        # Voltear la imagen horizontalmente para efecto espejo
        frame = cv2.flip(frame, 1)
        
        # Convertir BGR a RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Procesar con MediaPipe
        results = self.hands.process(rgb_frame)
        
        # Resetear estado
        self.is_hand_detected = False
        self.hand_position = None
        
        if results.multi_hand_landmarks:
            # Tomar la primera mano detectada
            hand_landmarks = results.multi_hand_landmarks[0]
            self.hand_landmarks = hand_landmarks
            self.is_hand_detected = True
            
            # Obtener posición del dedo índice
            index_finger = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            
            # Convertir a coordenadas de píxeles
            x = int(index_finger.x * self.camera_width)
            y = int(index_finger.y * self.camera_height)
            
            # Normalizar a coordenadas de pantalla
            screen_width = WINDOW_WIDTH
            screen_height = WINDOW_HEIGHT
            self.hand_position = normalize_hand_position(
                x, y, self.camera_width, self.camera_height,
                screen_width, screen_height
            )
            
            # Agregar al historial para suavizado
            self.position_history.append(self.hand_position)
            if len(self.position_history) > self.max_history:
                self.position_history.pop(0)
            
            # Aplicar suavizado
            if len(self.position_history) > 1:
                self.hand_position = self._smooth_position()
            
            # Dibujar landmarks en el frame
            self._draw_hand_landmarks(frame, hand_landmarks)
        
        return frame
    
    def _smooth_position(self) -> Tuple[float, float]:
        """Aplica suavizado a la posición de la mano."""
        if len(self.position_history) < 2:
            return self.hand_position
        
        # Promedio ponderado (más peso a posiciones recientes)
        weights = np.linspace(0.1, 1.0, len(self.position_history))
        weights = weights / np.sum(weights)
        
        x = sum(pos[0] * w for pos, w in zip(self.position_history, weights))
        y = sum(pos[1] * w for pos, w in zip(self.position_history, weights))
        
        return (x, y)
    
    def _draw_hand_landmarks(self, frame: np.ndarray, landmarks) -> None:
        """Dibuja los landmarks de la mano en el frame."""
        # Dibujar conexiones
        self.mp_drawing.draw_landmarks(
            frame,
            landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_drawing_styles.get_default_hand_landmarks_style(),
            self.mp_drawing_styles.get_default_hand_connections_style()
        )
        
        # Resaltar el dedo índice
        index_finger = landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        x = int(index_finger.x * self.camera_width)
        y = int(index_finger.y * self.camera_height)
        
        cv2.circle(frame, (x, y), 8, (0, 255, 0), -1)
        cv2.circle(frame, (x, y), 12, (255, 255, 255), 2)
    
    def get_hand_landmarks(self) -> Optional[List]:
        """Retorna los landmarks de la mano actual."""
        return self.hand_landmarks
    
    def get_hand_side(self) -> Optional[str]:
        """Determina si es mano izquierda o derecha."""
        if not self.hand_landmarks:
            return None
        
        # MediaPipe puede determinar la lateralidad
        # Por simplicidad, asumimos que es la mano dominante
        return "right"  # Puedes implementar detección más sofisticada
    
    def release(self) -> None:
        """Libera los recursos de la cámara."""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
    
    def get_camera_info(self) -> dict:
        """Retorna información sobre la cámara."""
        if not self.cap:
            return {}
        
        return {
            "width": int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "fps": int(self.cap.get(cv2.CAP_PROP_FPS))
        }
