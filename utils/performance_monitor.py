"""
Monitor de rendimiento para optimizar el juego
"""

import time
import threading
from collections import deque
from typing import Dict, List, Optional


class PerformanceMonitor:
    """Monitor de rendimiento del sistema."""
    
    def __init__(self, max_samples: int = 100):
        self.max_samples = max_samples
        
        # Métricas de rendimiento
        self.fps_history = deque(maxlen=max_samples)
        self.camera_fps_history = deque(maxlen=max_samples)
        self.gesture_detection_time = deque(maxlen=max_samples)
        self.hand_tracking_time = deque(maxlen=max_samples)
        
        # Estado del monitor
        self.monitoring = False
        self.monitor_thread = None
        
        # Tiempos de referencia
        self.last_fps_time = time.time()
        self.last_camera_time = time.time()
        self.frame_count = 0
        self.camera_frame_count = 0
        
    def start_monitoring(self) -> None:
        """Inicia el monitoreo de rendimiento."""
        if self.monitoring:
            return
            
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("Monitor de rendimiento iniciado")
    
    def stop_monitoring(self) -> None:
        """Detiene el monitoreo de rendimiento."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)
        print("Monitor de rendimiento detenido")
    
    def _monitor_loop(self) -> None:
        """Bucle principal del monitor."""
        while self.monitoring:
            current_time = time.time()
            
            # Calcular FPS del juego
            if current_time - self.last_fps_time >= 1.0:
                fps = self.frame_count / (current_time - self.last_fps_time)
                self.fps_history.append(fps)
                self.frame_count = 0
                self.last_fps_time = current_time
            
            # Calcular FPS de la cámara
            if current_time - self.last_camera_time >= 1.0:
                camera_fps = self.camera_frame_count / (current_time - self.last_camera_time)
                self.camera_fps_history.append(camera_fps)
                self.camera_frame_count = 0
                self.last_camera_time = current_time
            
            time.sleep(0.1)
    
    def record_frame(self) -> None:
        """Registra un frame del juego."""
        self.frame_count += 1
    
    def record_camera_frame(self) -> None:
        """Registra un frame de la cámara."""
        self.camera_frame_count += 1
    
    def record_gesture_detection_time(self, detection_time: float) -> None:
        """Registra el tiempo de detección de gestos."""
        self.gesture_detection_time.append(detection_time)
    
    def record_hand_tracking_time(self, tracking_time: float) -> None:
        """Registra el tiempo de seguimiento de manos."""
        self.hand_tracking_time.append(tracking_time)
    
    def get_current_fps(self) -> float:
        """Retorna el FPS actual del juego."""
        if not self.fps_history:
            return 0.0
        return self.fps_history[-1]
    
    def get_average_fps(self) -> float:
        """Retorna el FPS promedio."""
        if not self.fps_history:
            return 0.0
        return sum(self.fps_history) / len(self.fps_history)
    
    def get_camera_fps(self) -> float:
        """Retorna el FPS de la cámara."""
        if not self.camera_fps_history:
            return 0.0
        return self.camera_fps_history[-1]
    
    def get_average_camera_fps(self) -> float:
        """Retorna el FPS promedio de la cámara."""
        if not self.camera_fps_history:
            return 0.0
        return sum(self.camera_fps_history) / len(self.camera_fps_history)
    
    def get_gesture_detection_performance(self) -> Dict[str, float]:
        """Retorna métricas de rendimiento de detección de gestos."""
        if not self.gesture_detection_time:
            return {"average": 0.0, "min": 0.0, "max": 0.0}
        
        times = list(self.gesture_detection_time)
        return {
            "average": sum(times) / len(times),
            "min": min(times),
            "max": max(times)
        }
    
    def get_hand_tracking_performance(self) -> Dict[str, float]:
        """Retorna métricas de rendimiento de seguimiento de manos."""
        if not self.hand_tracking_time:
            return {"average": 0.0, "min": 0.0, "max": 0.0}
        
        times = list(self.hand_tracking_time)
        return {
            "average": sum(times) / len(times),
            "min": min(times),
            "max": max(times)
        }
    
    def get_performance_summary(self) -> Dict[str, any]:
        """Retorna un resumen completo del rendimiento."""
        return {
            "game_fps": {
                "current": self.get_current_fps(),
                "average": self.get_average_fps()
            },
            "camera_fps": {
                "current": self.get_camera_fps(),
                "average": self.get_average_camera_fps()
            },
            "gesture_detection": self.get_gesture_detection_performance(),
            "hand_tracking": self.get_hand_tracking_performance(),
            "samples_collected": len(self.fps_history)
        }
    
    def is_performance_acceptable(self) -> bool:
        """Verifica si el rendimiento es aceptable."""
        game_fps = self.get_average_fps()
        camera_fps = self.get_average_camera_fps()
        
        # Criterios de rendimiento aceptable
        min_game_fps = 30
        min_camera_fps = 15
        
        return game_fps >= min_game_fps and camera_fps >= min_camera_fps
    
    def get_performance_recommendations(self) -> List[str]:
        """Retorna recomendaciones para mejorar el rendimiento."""
        recommendations = []
        
        game_fps = self.get_average_fps()
        camera_fps = self.get_average_camera_fps()
        
        if game_fps < 30:
            recommendations.append("Reducir la resolución de la ventana del juego")
            recommendations.append("Disminuir la calidad de los gráficos")
        
        if camera_fps < 15:
            recommendations.append("Reducir la resolución de la cámara")
            recommendations.append("Cerrar otras aplicaciones que usen la cámara")
        
        gesture_perf = self.get_gesture_detection_performance()
        if gesture_perf["average"] > 0.1:  # Más de 100ms
            recommendations.append("Optimizar la detección de gestos")
            recommendations.append("Reducir la frecuencia de detección de gestos")
        
        return recommendations
    
    def reset_metrics(self) -> None:
        """Resetea todas las métricas."""
        self.fps_history.clear()
        self.camera_fps_history.clear()
        self.gesture_detection_time.clear()
        self.hand_tracking_time.clear()
        self.frame_count = 0
        self.camera_frame_count = 0
