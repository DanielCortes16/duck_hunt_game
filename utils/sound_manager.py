"""
Sistema de sonidos para Duck Hunt
"""

import pygame
import os
import numpy as np
from typing import Dict, Optional


class SoundManager:
    """Gestor de sonidos del juego."""
    
    def __init__(self):
        # Inicializar mixer de pygame
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        
        # Diccionario de sonidos
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.sfx_volume = 0.8
        
        # Cargar sonidos
        self.load_sounds()
    
    def load_sounds(self) -> None:
        """Carga todos los sonidos del juego."""
        sound_files = {
            'shot': 'assets/sounds/shot.wav',
            'hit': 'assets/sounds/hit.wav',
            'miss': 'assets/sounds/miss.wav',
            'dog_laugh': 'assets/sounds/dog_laugh.wav',
            'duck_quack': 'assets/sounds/duck_quack.wav',
            'game_start': 'assets/sounds/game_start.wav',
            'game_over': 'assets/sounds/game_over.wav',
            'level_complete': 'assets/sounds/level_complete.wav'
        }
        
        for sound_name, file_path in sound_files.items():
            try:
                if os.path.exists(file_path):
                    self.sounds[sound_name] = pygame.mixer.Sound(file_path)
                    self.sounds[sound_name].set_volume(self.sfx_volume)
                else:
                    # Crear sonidos sintéticos si no existen los archivos
                    self.sounds[sound_name] = self.create_synthetic_sound(sound_name)
            except Exception as e:
                print(f"Error cargando sonido {sound_name}: {e}")
                self.sounds[sound_name] = self.create_synthetic_sound(sound_name)
    
    def create_synthetic_sound(self, sound_name: str) -> pygame.mixer.Sound:
        """Crea sonidos sintéticos para el juego."""
        # Configuración de audio
        sample_rate = 22050
        duration = 0.5
        
        if sound_name == 'shot':
            # Sonido de disparo - ruido blanco con decay
            samples = int(sample_rate * duration)
            t = np.linspace(0, duration, samples)
            # Ruido blanco con decay exponencial
            noise = np.random.normal(0, 0.1, samples)
            envelope = np.exp(-t * 8)  # Decay rápido
            sound_data = (noise * envelope * 32767).astype(np.int16)
            
        elif sound_name == 'hit':
            # Sonido de impacto - tono con decay
            samples = int(sample_rate * 0.3)
            t = np.linspace(0, 0.3, samples)
            # Frecuencia descendente
            freq = 800 * np.exp(-t * 3)
            sound_data = (np.sin(2 * np.pi * freq * t) * np.exp(-t * 5) * 16383).astype(np.int16)
            
        elif sound_name == 'miss':
            # Sonido de fallo - tono bajo
            samples = int(sample_rate * 0.4)
            t = np.linspace(0, 0.4, samples)
            sound_data = (np.sin(2 * np.pi * 200 * t) * np.exp(-t * 2) * 8191).astype(np.int16)
            
        elif sound_name == 'dog_laugh':
            # Risa del perro - múltiples tonos
            samples = int(sample_rate * 1.0)
            t = np.linspace(0, 1.0, samples)
            # Múltiples frecuencias para simular risa
            freq1 = 300 + 100 * np.sin(2 * np.pi * 3 * t)
            freq2 = 600 + 200 * np.sin(2 * np.pi * 5 * t)
            sound_data = ((np.sin(2 * np.pi * freq1 * t) + 
                          np.sin(2 * np.pi * freq2 * t)) * 0.3 * np.exp(-t * 0.5) * 16383).astype(np.int16)
            
        elif sound_name == 'duck_quack':
            # Graznido de pato
            samples = int(sample_rate * 0.2)
            t = np.linspace(0, 0.2, samples)
            # Frecuencia modulada
            freq = 400 + 200 * np.sin(2 * np.pi * 20 * t)
            sound_data = (np.sin(2 * np.pi * freq * t) * np.exp(-t * 3) * 12287).astype(np.int16)
            
        elif sound_name == 'game_start':
            # Sonido de inicio de juego
            samples = int(sample_rate * 0.8)
            t = np.linspace(0, 0.8, samples)
            # Melodía ascendente
            freq = 200 + 400 * t
            sound_data = (np.sin(2 * np.pi * freq * t) * np.exp(-t * 0.5) * 12287).astype(np.int16)
            
        elif sound_name == 'game_over':
            # Sonido de game over
            samples = int(sample_rate * 1.0)
            t = np.linspace(0, 1.0, samples)
            # Frecuencia descendente
            freq = 400 * np.exp(-t * 2)
            sound_data = (np.sin(2 * np.pi * freq * t) * np.exp(-t * 1.5) * 12287).astype(np.int16)
            
        elif sound_name == 'level_complete':
            # Sonido de nivel completado
            samples = int(sample_rate * 0.6)
            t = np.linspace(0, 0.6, samples)
            # Melodía ascendente
            freq = 300 + 300 * t
            sound_data = (np.sin(2 * np.pi * freq * t) * np.exp(-t * 0.3) * 12287).astype(np.int16)
            
        else:
            # Sonido por defecto
            samples = int(sample_rate * 0.1)
            sound_data = np.zeros(samples, dtype=np.int16)
        
        # Crear sonido desde array (convertir a formato estéreo)
        if len(sound_data.shape) == 1:
            # Convertir mono a estéreo
            sound_data = np.column_stack((sound_data, sound_data))
        
        sound = pygame.sndarray.make_sound(sound_data)
        sound.set_volume(self.sfx_volume)
        return sound
    
    def play_sound(self, sound_name: str, volume: Optional[float] = None) -> None:
        """Reproduce un sonido."""
        if sound_name in self.sounds:
            if volume is not None:
                self.sounds[sound_name].set_volume(volume)
            self.sounds[sound_name].play()
    
    def play_shot(self) -> None:
        """Reproduce sonido de disparo."""
        self.play_sound('shot')
    
    def play_hit(self) -> None:
        """Reproduce sonido de impacto."""
        self.play_sound('hit')
    
    def play_miss(self) -> None:
        """Reproduce sonido de fallo."""
        self.play_sound('miss')
    
    def play_dog_laugh(self) -> None:
        """Reproduce risa del perro."""
        self.play_sound('dog_laugh')
    
    def play_duck_quack(self) -> None:
        """Reproduce graznido de pato."""
        self.play_sound('duck_quack')
    
    def play_game_start(self) -> None:
        """Reproduce sonido de inicio de juego."""
        self.play_sound('game_start')
    
    def play_game_over(self) -> None:
        """Reproduce sonido de game over."""
        self.play_sound('game_over')
    
    def play_level_complete(self) -> None:
        """Reproduce sonido de nivel completado."""
        self.play_sound('level_complete')
    
    def set_volume(self, volume: float) -> None:
        """Establece el volumen general."""
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
    
    def stop_all_sounds(self) -> None:
        """Detiene todos los sonidos."""
        pygame.mixer.stop()
    
    def cleanup(self) -> None:
        """Limpia los recursos de sonido."""
        pygame.mixer.quit()
