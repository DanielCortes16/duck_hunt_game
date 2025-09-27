"""
Script de instalación para Duck Hunt con Control por Cámara
"""

import subprocess
import sys
import os
import platform


def check_python_version():
    """Verifica la versión de Python."""
    if sys.version_info < (3, 8):
        print("Error: Se requiere Python 3.8 o superior")
        print(f"Versión actual: {sys.version}")
        return False
    print(f"✓ Python {sys.version.split()[0]} detectado")
    return True


def install_requirements():
    """Instala las dependencias requeridas."""
    print("\nInstalando dependencias...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error instalando dependencias: {e}")
        return False


def check_camera():
    """Verifica si hay una cámara disponible."""
    print("\nVerificando cámara web...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✓ Cámara web detectada")
            cap.release()
            return True
        else:
            print("⚠ No se pudo acceder a la cámara web")
            return False
    except ImportError:
        print("⚠ OpenCV no está instalado, no se puede verificar la cámara")
        return False


def create_directories():
    """Crea los directorios necesarios."""
    print("\nCreando estructura de directorios...")
    
    directories = [
        "assets",
        "assets/sounds",
        "assets/images",
        "logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Directorio {directory} creado")


def test_imports():
    """Prueba las importaciones principales."""
    print("\nProbando importaciones...")
    
    try:
        import pygame
        print("✓ Pygame importado correctamente")
    except ImportError:
        print("✗ Error importando Pygame")
        return False
    
    try:
        import cv2
        print("✓ OpenCV importado correctamente")
    except ImportError:
        print("✗ Error importando OpenCV")
        return False
    
    try:
        import mediapipe
        print("✓ MediaPipe importado correctamente")
    except ImportError:
        print("✗ Error importando MediaPipe")
        return False
    
    try:
        import numpy
        print("✓ NumPy importado correctamente")
    except ImportError:
        print("✗ Error importando NumPy")
        return False
    
    return True


def create_launcher_script():
    """Crea un script de lanzamiento."""
    print("\nCreando script de lanzamiento...")
    
    if platform.system() == "Windows":
        launcher_content = """@echo off
echo Iniciando Duck Hunt con Control por Camara...
python main.py
pause
"""
        with open("run_game.bat", "w") as f:
            f.write(launcher_content)
        print("✓ Script run_game.bat creado")
    else:
        launcher_content = """#!/bin/bash
echo "Iniciando Duck Hunt con Control por Camara..."
python3 main.py
"""
        with open("run_game.sh", "w") as f:
            f.write(launcher_content)
        os.chmod("run_game.sh", 0o755)
        print("✓ Script run_game.sh creado")


def main():
    """Función principal de instalación."""
    print("=== INSTALADOR DUCK HUNT - CONTROL POR CÁMARA ===")
    print("Este script configurará el juego en tu sistema\n")
    
    # Verificar Python
    if not check_python_version():
        return False
    
    # Crear directorios
    create_directories()
    
    # Instalar dependencias
    if not install_requirements():
        print("\nError: No se pudieron instalar las dependencias")
        print("Intenta ejecutar manualmente: pip install -r requirements.txt")
        return False
    
    # Probar importaciones
    if not test_imports():
        print("\nError: Algunas dependencias no se instalaron correctamente")
        return False
    
    # Verificar cámara
    camera_ok = check_camera()
    if not camera_ok:
        print("\n⚠ Advertencia: No se pudo verificar la cámara web")
        print("Asegúrate de tener una cámara conectada antes de jugar")
    
    # Crear script de lanzamiento
    create_launcher_script()
    
    print("\n" + "="*50)
    print("✓ INSTALACIÓN COMPLETADA")
    print("="*50)
    print("\nPara ejecutar el juego:")
    if platform.system() == "Windows":
        print("  - Ejecuta: run_game.bat")
        print("  - O ejecuta: python main.py")
    else:
        print("  - Ejecuta: ./run_game.sh")
        print("  - O ejecuta: python3 main.py")
    
    print("\nRequisitos del sistema:")
    print("- Cámara web conectada")
    print("- Buena iluminación")
    print("- Espacio libre para mover la mano")
    
    print("\nControles:")
    print("- Mueve tu mano para controlar la mira")
    print("- Junta pulgar e índice para disparar")
    print("- Presiona ESC para salir")
    
    return True


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
