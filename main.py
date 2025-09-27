"""
Duck Hunt con Control por Cámara Web
Punto de entrada principal del juego
"""

import pygame
import sys
import threading
import time
from typing import Tuple, Optional

from game.game_engine import GameEngine
from camera.hand_tracker import HandTracker
from camera.gesture_detector import GestureDetector
from utils.config import *


class DuckHuntCamera:
    """Clase principal que integra el juego con el control por cámara."""
    
    def __init__(self):
        # Inicializar componentes
        self.game_engine = GameEngine()
        self.hand_tracker = HandTracker()
        self.gesture_detector = GestureDetector()
        
        # Estado del sistema
        self.camera_active = False
        self.camera_thread = None
        self.running = True
        
        # Control de FPS para la cámara
        self.camera_fps = 30
        self.last_camera_update = 0
        
        # Calibración
        self.calibration_done = False
        self.calibration_start_time = 0
        
    def initialize_camera(self) -> bool:
        """Inicializa el sistema de cámara."""
        print("Inicializando cámara web...")
        
        if not self.hand_tracker.initialize_camera():
            print("Error: No se pudo inicializar la cámara web")
            return False
        
        print("Cámara inicializada correctamente")
        self.camera_active = True
        return True
    
    def start_camera_thread(self) -> None:
        """Inicia el hilo de procesamiento de cámara."""
        if self.camera_thread and self.camera_thread.is_alive():
            return
            
        self.camera_thread = threading.Thread(target=self._camera_loop, daemon=True)
        self.camera_thread.start()
        print("Hilo de cámara iniciado")
    
    def _camera_loop(self) -> None:
        """Bucle principal de procesamiento de cámara."""
        while self.running and self.camera_active:
            current_time = time.time()
            
            # Control de FPS
            if current_time - self.last_camera_update < 1.0 / self.camera_fps:
                continue
                
            self.last_camera_update = current_time
            
            try:
                # Procesar frame de cámara
                frame = self.hand_tracker.process_frame()
                
                if frame is not None:
                    # Obtener posición de la mano
                    hand_position = self.hand_tracker.get_hand_position()
                    
                    # Actualizar historial de gestos
                    if hand_position:
                        self.gesture_detector.update_gesture_history(hand_position)
                    
                    # Detectar gesto de disparo
                    landmarks = self.hand_tracker.get_hand_landmarks()
                    shoot_gesture = False
                    
                    if landmarks and self.gesture_detector.is_gesture_ready():
                        shoot_gesture = self.gesture_detector.detect_pinch_gesture(landmarks)
                    
                    # Enviar datos al motor del juego
                    self._update_game_control(hand_position, shoot_gesture)
                    
            except Exception as e:
                print(f"Error en procesamiento de cámara: {e}")
                continue
    
    def _update_game_control(self, hand_position: Optional[Tuple[float, float]], 
                            shoot_gesture: bool) -> None:
        """Actualiza el control del juego con datos de la cámara."""
        try:
            self.game_engine.handle_camera_control(hand_position, shoot_gesture)
        except Exception as e:
            print(f"Error actualizando control del juego: {e}")
    
    def calibrate_camera(self) -> bool:
        """Realiza calibración inicial de la cámara."""
        print("Iniciando calibración de cámara...")
        print("Mueve tu mano frente a la cámara para calibrar")
        
        self.calibration_start_time = time.time()
        calibration_duration = 3.0  # 3 segundos de calibración
        
        while time.time() - self.calibration_start_time < calibration_duration:
            if not self.camera_active:
                return False
                
            # Procesar frame para calibración
            frame = self.hand_tracker.process_frame()
            
            if frame is not None and self.hand_tracker.is_hand_visible():
                print(f"Calibración: {int(calibration_duration - (time.time() - self.calibration_start_time))}s")
            
            time.sleep(0.1)
        
        self.calibration_done = True
        print("Calibración completada")
        return True
    
    def show_camera_feed(self) -> None:
        """Muestra la alimentación de la cámara (opcional, para debug)."""
        if not self.camera_active:
            return
            
        try:
            frame = self.hand_tracker.process_frame()
            if frame is not None:
                # Redimensionar para mostrar
                import cv2
                display_frame = cv2.resize(frame, (320, 240))
                cv2.imshow('Duck Hunt Camera', display_frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
        except Exception as e:
            print(f"Error mostrando cámara: {e}")
    
    def run(self) -> None:
        """Ejecuta el juego principal."""
        print("=== DUCK HUNT - CONTROL POR CÁMARA ===")
        print("Iniciando sistema...")
        
        # Inicializar cámara
        if not self.initialize_camera():
            print("Error: No se pudo inicializar la cámara")
            print("Asegúrate de que tienes una cámara web conectada")
            return
        
        # Calibrar cámara
        if not self.calibrate_camera():
            print("Error en la calibración")
            return
        
        # Iniciar hilo de cámara
        self.start_camera_thread()
        
        print("Sistema listo. Iniciando juego...")
        print("Controles:")
        print("- Mueve tu mano para controlar la mira")
        print("- Junta pulgar e índice para disparar")
        print("- Presiona ESC para salir")
        
        try:
            # Ejecutar el juego
            self.game_engine.run()
        except KeyboardInterrupt:
            print("\nJuego interrumpido por el usuario")
        except Exception as e:
            print(f"Error en el juego: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self) -> None:
        """Limpia los recursos del sistema."""
        print("Limpiando recursos...")
        
        self.running = False
        self.camera_active = False
        
        if self.camera_thread and self.camera_thread.is_alive():
            self.camera_thread.join(timeout=1.0)
        
        self.hand_tracker.release()
        
        try:
            import cv2
            cv2.destroyAllWindows()
        except:
            pass
        
        print("Recursos liberados")


def main():
    """Función principal."""
    try:
        # Verificar dependencias
        print("Verificando dependencias...")
        
        try:
            import pygame
            import cv2
            import mediapipe
            import numpy
        except ImportError as e:
            print(f"Error: Faltan dependencias: {e}")
            print("Ejecuta: pip install -r requirements.txt")
            return
        
        print("Dependencias verificadas correctamente")
        
        # Crear y ejecutar el juego
        game = DuckHuntCamera()
        game.run()
        
    except Exception as e:
        print(f"Error fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
