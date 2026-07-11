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
print(f"API Key cargada: {api_key[:10]}...")

try:
    genai.configure(api_key=api_key)
    models = genai.list_models()
    print("Modelos disponibles:")
    for m in models:
        print(f"- {m.name} (Soporta generateContent: {'generateContent' in m.supported_generation_methods})")
except Exception as e:
    print(f"Error al listar modelos: {e}")
