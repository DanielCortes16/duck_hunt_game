"""
Configuración avanzada para Duck Hunt
Permite personalizar el comportamiento del juego
"""

# Configuración de dificultad
DIFFICULTY_LEVELS = {
    "easy": {
        "duck_speed": 1.5,
        "spawn_interval": 4.0,
        "max_ducks": 2,
        "lives": 5
    },
    "normal": {
        "duck_speed": 2.0,
        "spawn_interval": 3.0,
        "max_ducks": 3,
        "lives": 3
    },
    "hard": {
        "duck_speed": 3.0,
        "spawn_interval": 2.0,
        "max_ducks": 4,
        "lives": 2
    }
}

# Configuración de la cámara
CAMERA_SETTINGS = {
    "resolution": {
        "low": (320, 240),
        "medium": (640, 480),
        "high": (1280, 720)
    },
    "fps": {
        "low": 15,
        "medium": 30,
        "high": 60
    }
}

# Configuración de gestos
GESTURE_SETTINGS = {
    "pinch_threshold": {
        "sensitive": 0.03,
        "normal": 0.05,
        "strict": 0.08
    },
    "debounce_time": {
        "fast": 0.2,
        "normal": 0.3,
        "slow": 0.5
    }
}

# Configuración de suavizado
SMOOTHING_SETTINGS = {
    "none": 1.0,
    "light": 0.8,
    "medium": 0.6,
    "heavy": 0.4
}

# Configuración de colores personalizados
CUSTOM_COLORS = {
    "crosshair": {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "white": (255, 255, 255)
    },
    "background": {
        "sky_blue": (135, 206, 235),
        "sunset": (255, 165, 0),
        "forest": (34, 139, 34),
        "night": (25, 25, 112)
    }
}

# Configuración de sonido (para futuras implementaciones)
SOUND_SETTINGS = {
    "enabled": True,
    "volume": 0.7,
    "sounds": {
        "shot": "assets/sounds/shot.wav",
        "hit": "assets/sounds/hit.wav",
        "miss": "assets/sounds/miss.wav",
        "dog_laugh": "assets/sounds/dog_laugh.wav"
    }
}

# Configuración de calibración
CALIBRATION_SETTINGS = {
    "auto_calibrate": True,
    "calibration_points": 5,
    "calibration_time": 3.0,
    "quality_threshold": 0.7
}

# Configuración de rendimiento
PERFORMANCE_SETTINGS = {
    "target_fps": 60,
    "camera_fps": 30,
    "enable_vsync": True,
    "reduce_quality_on_low_fps": True,
    "low_fps_threshold": 30
}

# Configuración de debug
DEBUG_SETTINGS = {
    "show_fps": False,
    "show_hand_landmarks": False,
    "show_gesture_confidence": False,
    "log_performance": False,
    "save_camera_feed": False
}

# Configuración de accesibilidad
ACCESSIBILITY_SETTINGS = {
    "high_contrast": False,
    "large_crosshair": False,
    "slow_motion": False,
    "audio_cues": False
}

# Configuración por defecto
DEFAULT_CONFIG = {
    "difficulty": "normal",
    "camera_resolution": "medium",
    "camera_fps": "medium",
    "gesture_sensitivity": "normal",
    "smoothing": "medium",
    "crosshair_color": "red",
    "background_theme": "sky_blue",
    "sound_enabled": True,
    "auto_calibrate": True,
    "debug_mode": False
}

def get_config_value(category: str, setting: str, value: str = None):
    """Obtiene un valor de configuración."""
    configs = {
        "difficulty": DIFFICULTY_LEVELS,
        "camera": CAMERA_SETTINGS,
        "gesture": GESTURE_SETTINGS,
        "smoothing": SMOOTHING_SETTINGS,
        "colors": CUSTOM_COLORS,
        "sound": SOUND_SETTINGS,
        "calibration": CALIBRATION_SETTINGS,
        "performance": PERFORMANCE_SETTINGS,
        "debug": DEBUG_SETTINGS,
        "accessibility": ACCESSIBILITY_SETTINGS
    }
    
    if category in configs and setting in configs[category]:
        if value and value in configs[category][setting]:
            return configs[category][setting][value]
        return configs[category][setting]
    
    return None

def load_user_config():
    """Carga la configuración del usuario desde archivo."""
    import json
    import os
    
    config_file = "user_config.json"
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error cargando configuración: {e}")
    
    return DEFAULT_CONFIG.copy()

def save_user_config(config: dict):
    """Guarda la configuración del usuario."""
    import json
    
    try:
        with open("user_config.json", 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error guardando configuración: {e}")
        return False

def reset_to_defaults():
    """Resetea la configuración a los valores por defecto."""
    import os
    
    config_file = "user_config.json"
    if os.path.exists(config_file):
        try:
            os.remove(config_file)
            return True
        except Exception as e:
            print(f"Error reseteando configuración: {e}")
            return False
    return True
