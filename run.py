import uvicorn
import os
import sys

# Asegurar que el directorio raíz del proyecto esté en el path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def cargar_env_local():
    """Carga variables desde el archivo .env si existe."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(base_dir, '.env')
    
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Ignorar comentarios y líneas vacías
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    # Quitar espacios y comillas si las hay
                    key = key.strip()
                    val = val.strip().strip("'").strip('"')
                    os.environ[key] = val
        print("[INFO] Variables de entorno cargadas desde el archivo .env local.")

if __name__ == "__main__":
    cargar_env_local()
    
    print("--------------------------------------------------")
    print(" Iniciando Servidor CNN NeuralVision Local")
    print("--------------------------------------------------")
    print("Accede a tu frontend en: http://127.0.0.1:8000")
    print("Presiona Ctrl+C para detener el servidor.")
    print("--------------------------------------------------\n")
    
    # Iniciar FastAPI con reload activado para desarrollo
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
