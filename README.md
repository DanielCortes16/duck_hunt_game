# 🦆 Duck Hunt con Control por Cámara

Un clon del clásico juego **Duck Hunt** desarrollado en **Python con Pygame**, donde el control se realiza mediante **gestos de mano** detectados por cámara web usando **MediaPipe**.

---

## ✨ Características
- 🎮 Control de mira con movimiento de la mano  
- 👆 Disparo con gesto de pinza (pulgar e índice)  
- 🦆 Patos con diferentes patrones de vuelo  
- 🐕 Perro que se ríe cuando fallas  
- 📊 Sistema de puntuación y vidas  
- 🎯 Dificultad progresiva  

---

## ⚙️ Instalación

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Ejecuta el juego:
   ```bash
   python main.py
   ```

---

## 🎮 Controles
- **Mover la mira** → Mueve tu mano frente a la cámara  
- **Disparar** → Haz el gesto de pinza juntando pulgar e índice  
- **Salir** → Presiona `ESC` o cierra la ventana  

---

## 🖥️ Requisitos del Sistema
- Python **3.8+**  
- Cámara web  
- Buena iluminación para la detección de manos  

---

## 📂 Estructura del Proyecto
```text
duck_hunt_game/
├── main.py                 # Punto de entrada principal
├── game/
│   ├── __init__.py
│   ├── game_engine.py      # Motor principal del juego
│   ├── duck.py             # Lógica de los patos
│   ├── crosshair.py        # Sistema de mira
│   └── dog.py              # Animación del perro
├── camera/
│   ├── __init__.py
│   ├── hand_tracker.py     # Seguimiento de manos
│   └── gesture_detector.py # Detección de gestos
├── utils/
│   ├── __init__.py
│   ├── config.py           # Configuraciones
│   └── helpers.py          # Funciones auxiliares
└── assets/                 # Recursos gráficos
```

---

## 🔧 Configuración
Puedes ajustar la **sensibilidad** y otros parámetros en:  
```text
utils/config.py
```
