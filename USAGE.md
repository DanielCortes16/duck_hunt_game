# Guía de Uso - Duck Hunt con Control por Cámara

## Instalación Rápida

1. **Instalar dependencias:**
   ```bash
   python install.py
   ```

2. **Ejecutar el juego:**
   ```bash
   python main.py
   ```

## Estructura del Proyecto

```
duck_hunt_game/
├── main.py                 # Punto de entrada principal
├── demo.py                 # Demostración interactiva
├── install.py              # Script de instalación
├── requirements.txt        # Dependencias
├── README.md              # Documentación principal
├── TROUBLESHOOTING.md     # Solución de problemas
├── USAGE.md               # Esta guía
├── config_advanced.py     # Configuración avanzada
├── game/                  # Motor del juego
│   ├── game_engine.py    # Motor principal
│   ├── duck.py           # Lógica de patos
│   ├── crosshair.py      # Sistema de mira
│   └── dog.py            # Animación del perro
├── camera/                # Control por cámara
│   ├── hand_tracker.py  # Seguimiento de manos
│   └── gesture_detector.py # Detección de gestos
├── utils/                 # Utilidades
│   ├── config.py         # Configuración básica
│   ├── helpers.py        # Funciones auxiliares
│   ├── calibration.py    # Sistema de calibración
│   └── performance_monitor.py # Monitor de rendimiento
└── examples/             # Ejemplos y herramientas
    ├── custom_game.py    # Juego personalizado
    └── gesture_training.py # Entrenador de gestos
```

## Modos de Ejecución

### 1. Juego Principal
```bash
python main.py
```
- Juego completo con control por cámara
- Calibración automática
- Sistema de puntuación y vidas

### 2. Demostración
```bash
python demo.py
```
- Demostración interactiva
- Muestra las capacidades del sistema
- Ideal para probar la cámara

### 3. Entrenador de Gestos
```bash
python examples/gesture_training.py
```
- Herramienta para practicar gestos
- Calibración manual
- Estadísticas de precisión

### 4. Juego Personalizado
```bash
python examples/custom_game.py
```
- Versión con características adicionales
- Power-ups y sistema de combo
- Modos especiales (nocturno, arcoíris)

## Controles del Juego

### Control por Cámara
- **Mover la mira**: Mueve tu mano frente a la cámara
- **Disparar**: Haz el gesto de pinza (pulgar + índice)
- **Calibración**: Sigue las instrucciones en pantalla

### Controles de Teclado
- **ESPACIO**: Iniciar juego / Continuar
- **ESC**: Salir / Volver al menú
- **R**: Reiniciar juego (durante la partida)

## Configuración

### Configuración Básica (`utils/config.py`)
```python
# Resolución de la ventana
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

# Configuración de la cámara
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Sensibilidad de gestos
PINCH_THRESHOLD = 0.05  # Reducir para mayor sensibilidad
GESTURE_DEBOUNCE_TIME = 0.3  # Tiempo entre disparos

# Suavizado del movimiento
SMOOTHING_FACTOR = 0.7  # 0-1, mayor = más suave
```

### Configuración Avanzada (`config_advanced.py`)
```python
# Dificultades personalizadas
DIFFICULTY_LEVELS = {
    "easy": {"duck_speed": 1.5, "lives": 5},
    "normal": {"duck_speed": 2.0, "lives": 3},
    "hard": {"duck_speed": 3.0, "lives": 2}
}

# Configuración de colores
CUSTOM_COLORS = {
    "crosshair": {"red": (255, 0, 0), "green": (0, 255, 0)},
    "background": {"sky_blue": (135, 206, 235)}
}
```

## Optimización de Rendimiento

### Para Sistemas Lentos
1. Reducir resolución de cámara:
   ```python
   CAMERA_WIDTH = 320
   CAMERA_HEIGHT = 240
   ```

2. Reducir FPS objetivo:
   ```python
   FPS = 30  # En lugar de 60
   ```

3. Aumentar suavizado:
   ```python
   SMOOTHING_FACTOR = 0.9
   ```

### Para Mejor Precisión
1. Aumentar resolución de cámara:
   ```python
   CAMERA_WIDTH = 1280
   CAMERA_HEIGHT = 720
   ```

2. Reducir suavizado:
   ```python
   SMOOTHING_FACTOR = 0.5
   ```

3. Ajustar sensibilidad:
   ```python
   PINCH_THRESHOLD = 0.03  # Más sensible
   ```

## Solución de Problemas Comunes

### Cámara No Detectada
- Verificar que la cámara esté conectada
- Cerrar otras aplicaciones que usen la cámara
- Ejecutar como administrador (Windows)

### Detección Pobre de Manos
- Mejorar iluminación
- Usar fondo contrastante
- Mantener mano a 30-60 cm de la cámara

### Gestos No Detectados
- Hacer gestos más lentos y claros
- Asegurar buena iluminación
- Ajustar `PINCH_THRESHOLD` en config.py

### Rendimiento Bajo
- Reducir resolución de cámara
- Cerrar otras aplicaciones
- Usar configuración de rendimiento bajo

## Desarrollo y Personalización

### Agregar Nuevos Tipos de Patos
```python
# En game/duck.py
class SpecialDuck(Duck):
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.special_ability = "golden"
        self.score_multiplier = 2
```

### Crear Nuevos Gestos
```python
# En camera/gesture_detector.py
def detect_custom_gesture(self, landmarks):
    # Implementar detección de gesto personalizado
    pass
```

### Agregar Efectos de Sonido
```python
# En game/game_engine.py
def play_sound(self, sound_name):
    if hasattr(self, 'sounds'):
        self.sounds[sound_name].play()
```

## Requisitos del Sistema

### Mínimos
- Python 3.8+
- 4GB RAM
- Cámara web USB
- Procesador 2GHz

### Recomendados
- Python 3.9+
- 8GB RAM
- Cámara web HD
- Procesador 3GHz+
- Buena iluminación

## Soporte y Contribuciones

Para reportar problemas o sugerir mejoras:
1. Revisar `TROUBLESHOOTING.md`
2. Verificar configuración
3. Probar con diferentes configuraciones
4. Documentar el problema

## Licencia

Este proyecto es de código abierto. Puedes modificarlo y distribuirlo libremente.
