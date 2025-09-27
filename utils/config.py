"""
Configuraciones del juego Duck Hunt
"""

# Configuración de la ventana
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

# Configuración del juego
INITIAL_LIVES = 3
SCORE_PER_DUCK = 100
DEFAULT_DUCK_SPEED = 2
MAX_DUCKS_ON_SCREEN = 3

# Configuración de la mira
CROSSHAIR_SIZE = 30
CROSSHAIR_COLOR = (255, 0, 0)  # Rojo
CROSSHAIR_THICKNESS = 3

# Configuración de la cámara
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
HAND_DETECTION_CONFIDENCE = 0.7
GESTURE_DETECTION_CONFIDENCE = 0.8

# Configuración de gestos
PINCH_THRESHOLD = 0.05  # Distancia mínima para detectar pinza
GESTURE_DEBOUNCE_TIME = 0.3  # Tiempo en segundos para evitar disparos accidentales

# Configuración de suavizado
SMOOTHING_FACTOR = 0.7  # Factor de suavizado para el movimiento de la mira (0-1)

# Colores
BACKGROUND_COLOR = (135, 206, 235)  # Azul cielo
GRASS_COLOR = (34, 139, 34)  # Verde
DUCK_COLOR = (255, 165, 0)  # Naranja
BUSH_COLOR = (0, 100, 0)  # Verde oscuro

# Configuración de patos
DUCK_SPAWN_INTERVAL = 3.0  # Segundos entre aparición de patos
DUCK_FLIGHT_HEIGHT_MIN = 200
DUCK_FLIGHT_HEIGHT_MAX = 400
