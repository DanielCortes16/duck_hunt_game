# Guía de Solución de Problemas - Duck Hunt

## Problemas Comunes y Soluciones

### 1. Error de Cámara No Detectada

**Síntoma:** El juego no puede acceder a la cámara web.

**Soluciones:**
- Verifica que la cámara esté conectada y funcionando
- Cierra otras aplicaciones que puedan estar usando la cámara (Skype, Zoom, etc.)
- En Windows, verifica los permisos de cámara en Configuración > Privacidad
- Prueba ejecutar el juego como administrador

### 2. Detección de Manos Pobre

**Síntoma:** El sistema no detecta bien la mano o es impreciso.

**Soluciones:**
- Mejora la iluminación de la habitación
- Usa un fondo contrastante (evita fondos muy claros o muy oscuros)
- Mantén la mano a una distancia adecuada de la cámara (30-60 cm)
- Evita movimientos muy rápidos
- Asegúrate de que la mano esté completamente visible

### 3. Gestos de Disparo No Detectados

**Síntoma:** El gesto de pinza no se detecta correctamente.

**Soluciones:**
- Haz el gesto más lento y deliberado
- Asegúrate de que el pulgar e índice estén claramente juntos
- Mantén el gesto por al menos 0.1 segundos
- Verifica que la mano esté bien iluminada
- Ajusta la sensibilidad en `utils/config.py`

### 4. Rendimiento Bajo

**Síntoma:** El juego va lento o con lag.

**Soluciones:**
- Reduce la resolución de la cámara en `utils/config.py`
- Cierra otras aplicaciones que consuman recursos
- Reduce la calidad de los gráficos
- Ajusta el FPS objetivo
- Usa un sistema con mejor hardware

### 5. Movimiento de Mira Errático

**Síntoma:** La mira se mueve de forma impredecible.

**Soluciones:**
- Aumenta el factor de suavizado en `utils/config.py`
- Mejora la iluminación
- Usa un fondo más contrastante
- Calibra el sistema nuevamente
- Verifica que no haya interferencias en la cámara

### 6. Error de Dependencias

**Síntoma:** Error al importar módulos.

**Soluciones:**
```bash
# Reinstalar dependencias
pip uninstall pygame opencv-python mediapipe numpy
pip install -r requirements.txt

# O instalar individualmente
pip install pygame==2.5.2
pip install opencv-python==4.8.1.78
pip install mediapipe==0.10.7
pip install numpy==1.24.3
```

### 7. Problemas de Calibración

**Síntoma:** La calibración no funciona correctamente.

**Soluciones:**
- Asegúrate de tener buena iluminación durante la calibración
- Mueve la mano lentamente a cada punto de calibración
- Mantén la mano estable en cada punto por 2 segundos
- Reinicia el juego si la calibración falla
- Verifica que la cámara esté funcionando correctamente

## Configuración Avanzada

### Ajustar Sensibilidad de Gestos

Edita `utils/config.py`:
```python
PINCH_THRESHOLD = 0.05  # Reducir para mayor sensibilidad
GESTURE_DEBOUNCE_TIME = 0.3  # Aumentar para evitar disparos accidentales
```

### Mejorar Rendimiento

Edita `utils/config.py`:
```python
CAMERA_WIDTH = 320  # Reducir resolución
CAMERA_HEIGHT = 240
SMOOTHING_FACTOR = 0.8  # Aumentar suavizado
```

### Ajustar Dificultad

Edita `config_advanced.py`:
```python
DIFFICULTY_LEVELS = {
    "easy": {
        "duck_speed": 1.0,  # Patos más lentos
        "spawn_interval": 5.0,  # Menos patos
        "max_ducks": 1,
        "lives": 5
    }
}
```

## Logs y Debugging

### Habilitar Modo Debug

Edita `config_advanced.py`:
```python
DEBUG_SETTINGS = {
    "show_fps": True,
    "show_hand_landmarks": True,
    "show_gesture_confidence": True,
    "log_performance": True
}
```

### Verificar Rendimiento

El juego incluye un monitor de rendimiento que puedes activar:
```python
from utils.performance_monitor import PerformanceMonitor
monitor = PerformanceMonitor()
monitor.start_monitoring()
```

## Contacto y Soporte

Si sigues teniendo problemas:

1. Verifica que cumples con los requisitos del sistema
2. Revisa los logs de error en la consola
3. Prueba con diferentes configuraciones
4. Asegúrate de tener la última versión de Python y las dependencias

## Requisitos del Sistema

- **Python:** 3.8 o superior
- **RAM:** Mínimo 4GB recomendado
- **CPU:** Procesador de 2GHz o superior
- **Cámara:** Webcam USB estándar
- **Iluminación:** Buena iluminación ambiente
- **Espacio:** Área libre de 1x1 metro para mover la mano
