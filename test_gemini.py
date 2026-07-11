import os
import google.generativeai as genai

# Cargar .env
env_path = '.env'
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                os.environ[key.strip()] = val.strip().strip("'").strip('"')

api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

modelos_a_probar = [
    "gemini-2.0-flash",
    "gemini-2.5-flash",
    "gemini-flash-latest",
    "gemini-pro-latest"
]

print("Probando modelos...")
for nombre_modelo in modelos_a_probar:
    try:
        print(f"\nIntentando con {nombre_modelo}...")
        model = genai.GenerativeModel(nombre_modelo)
        response = model.generate_content("Dí hola en una palabra")
        print(f"[EXITO] {nombre_modelo} respondió: {response.text.strip()}")
    except Exception as e:
        print(f"[FALLO] {nombre_modelo} falló con error: {e}")
