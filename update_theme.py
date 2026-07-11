import os

css_path = os.path.join('frontend', 'style.css')
if not os.path.exists(css_path):
    print("Error: frontend/style.css no encontrado.")
    exit(1)

with open(css_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Reemplazar el bloque :root
old_root = """:root {
    --bg-color: #08090d;
    --card-bg: rgba(17, 19, 31, 0.65);
    --border-color: rgba(255, 255, 255, 0.08);
    --border-hover: rgba(59, 130, 246, 0.4);
    
    --text-primary: #f3f4f6;
    --text-secondary: #9ca3af;
    
    --accent-blue: #3b82f6;
    --accent-purple: #8b5cf6;
    --accent-cyan: #06b6d4;
    --accent-gradient: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
    
    --error: #ef4444;
    --success: #10b981;
    --warning: #f59e0b;
}"""

new_root = """:root {
    --bg-color: #0a0908;
    --card-bg: rgba(20, 18, 17, 0.82);
    --border-color: rgba(212, 175, 55, 0.15);
    --border-hover: rgba(212, 175, 55, 0.55);
    
    --text-primary: #f5f5f4;
    --text-secondary: #a8a29e;
    
    --accent-blue: #d4af37; /* Oro metálico */
    --accent-purple: #10b981; /* Verde esmeralda */
    --accent-cyan: #f59e0b; /* Ámbar */
    --accent-gradient: linear-gradient(135deg, #d4af37 0%, #b45309 100%);
    
    --error: #f43f5e;
    --success: #10b981;
    --warning: #f59e0b;
}"""

content = content.replace(old_root, new_root)

# 2. Reemplazar el cuerpo body para agregar textura de mina / cueva
old_body = """body {
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    overflow-x: hidden;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
}"""

new_body = """body {
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background-color: var(--bg-color);
    background-image: 
        radial-gradient(circle at 15% 15%, rgba(212, 175, 55, 0.05) 0%, transparent 60%),
        radial-gradient(circle at 85% 85%, rgba(16, 185, 129, 0.05) 0%, transparent 60%),
        linear-gradient(rgba(212, 175, 55, 0.007) 1px, transparent 1px),
        linear-gradient(90deg, rgba(212, 175, 55, 0.007) 1px, transparent 1px);
    background-size: 100% 100%, 100% 100%, 50px 50px, 50px 50px;
    color: var(--text-primary);
    min-height: 100vh;
    overflow-x: hidden;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
}"""

content = content.replace(old_body, new_body)

# 3. Reemplazar los colores de sombra/resplandor hardcodeados en RGBA (Azul y Púrpura -> Oro y Esmeralda)
content = content.replace("rgba(59, 130, 246,", "rgba(212, 175, 55,")
content = content.replace("rgba(139, 92, 246,", "rgba(16, 185, 129,")

# Guardar los cambios
with open(css_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("CSS de frontend/style.css actualizado con éxito.")
