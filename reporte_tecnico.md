# REPORTE TÉCNICO INDIVIDUAL
## Sistema de Clasificación de Imágenes Basado en Aprendizaje por Transferencia (CNN) y API REST Web

**Asignatura:** Aprendizaje Automático / Inteligencia Artificial  
**Estudiante:** [Tu Nombre Completo]  
**Fecha:** 10 de Julio de 2026  

---

## 1. Introducción y Planteamiento del Problema
El presente proyecto resuelve un problema de clasificación de imágenes multiclase utilizando redes neuronales convolucionales (CNN) profundas. A través de la metodología de **Transfer Learning** (Aprendizaje por Transferencia), se utiliza una red preentrenada en un corpus masivo para especializarla en una tarea de clasificación específica determinada por el conjunto de datos de entrenamiento del usuario. 

Para dotar al sistema de utilidad práctica en el mundo real, el modelo se integra con una interfaz web moderna, responsiva e intuitiva (Frontend) conectada a un servidor de inferencia de alto rendimiento (Backend) a través de una API REST pública y estable.

---

## 2. Justificación Tecnológica (Stack y Herramientas Seleccionadas)

Para el desarrollo del sistema se seleccionó un conjunto de tecnologías modernas que garantizan escalabilidad, rendimiento y facilidad de despliegue:

### A. Núcleo de Inteligencia Artificial (Backend ML): PyTorch y Torchvision
* **PyTorch:** Es el framework del estado del arte preferido en el ámbito académico y de investigación por su gráfico de computación dinámico (eager execution), depuración nativa en Python y rendimiento optimizado.
* **Torchvision:** Permite acceder a pesos optimizados preentrenados en ImageNet para arquitecturas líderes como ResNet.
* **ResNet18 (Arquitectura Base):** Seleccionada por su excelente balance entre número de parámetros (11.7 millones), velocidad de inferencia en CPU/GPU y precisión. Introduce conexiones residuales ("skip connections") que resuelven el problema del gradiente desvanecido en redes profundas.

### B. Servidor API de Inferencia (Backend Web): FastAPI (Python)
* **FastAPI:** Elegido sobre Flask y Django debido a que está diseñado específicamente para APIs REST modernas y de alta velocidad.
* **Rendimiento Asíncrono:** Basado en Starlette y Pydantic, su velocidad de ejecución es comparable a la de entornos en Node.js o Go.
* **Tipado Estático y Validación:** Valida automáticamente los tipos de datos entrantes (como imágenes binarias en peticiones POST multipart).
* **Documentación Automática:** Genera automáticamente la documentación de la API en los estándares OpenAPI y Swagger UI (accesible en `/docs`), agilizando las pruebas y la integración.

### C. Entorno Web de Usuario (Frontend): HTML5, CSS3 Vanilla y JavaScript (ES6)
* **Diseño Personalizado sin Plantillas:** En lugar de utilizar librerías de componentes prediseñadas (que suelen lucir genéricas y repetitivas), se implementó una interfaz nativa desde cero.
* **Estética Premium ("Glassmorphism"):** Se utiliza una paleta de colores oscura, combinando degradados sutiles (azul a morado) y efectos visuales de desenfoque de fondo (`backdrop-filter`) para crear una experiencia de usuario inmersiva, limpia y profesional.
* **Interactividad y Animaciones:** JavaScript maneja eventos nativos de arrastrar y soltar (Drag and Drop), previsualización de imágenes sin recargar la página, llamadas asíncronas (`fetch`) y renderizado interactivo de las probabilidades por clase.

### D. Infraestructura y Despliegue: Docker y Hugging Face Spaces
* **Hugging Face Spaces:** Seleccionado por encima de plataformas tradicionales como Render o Railway para la capa gratuita. PyTorch requiere una cantidad sustancial de memoria RAM para cargar el modelo en memoria y procesar imágenes. Mientras Render limita sus cuentas gratuitas a 512MB de RAM (lo que provoca reinicios del servidor por falta de memoria), Hugging Face ofrece **16GB de RAM y CPU gratuitas**.
* **Contenedores Docker (Dockerfile):** Permite empaquetar de forma exacta el sistema operativo, las dependencias de Python (optimizando PyTorch para CPU a fin de reducir el tamaño de la imagen) y el código de la aplicación. Esto asegura que la aplicación corra exactamente igual en el servidor de producción que en el entorno local.

---

## 3. Arquitectura del Sistema
El flujo de datos del sistema sigue un modelo clásico Cliente-Servidor desacoplado:

```mermaid
graph LR
    subgraph Cliente (Navegador)
        UI[Interfaz HTML/CSS] -- 1. Sube Imagen (Drag & Drop) --> JS[JavaScript ES6]
        JS -- 5. Renderiza Resultados y Gráficos --> UI
    end
    subgraph Servidor (FastAPI + Docker)
        API[FastAPI API Endpoint] -- 2. Valida y Preprocesa --> PIL[PIL Image Loader]
        PIL -- 3. Tensor Normalizado --> CNN[Modelo ResNet18 PyTorch]
        CNN -- 4. Softmax (Probabilidades) --> API
    end
    JS -- POST /api/predict (Multipart) --> API
```

---

## 4. Detalles del Modelo y Entrenamiento

### A. Transfer Learning (Aprendizaje por Transferencia)
El modelo aprovecha las capas de extracción de características convolucionales previamente entrenadas en millones de imágenes de **ImageNet**. Se congelaron todos los parámetros de estas capas (`param.requires_grad = False`) para mantener intacto su conocimiento general de bordes, formas y texturas.

Únicamente se reemplazó la capa final de clasificación (`model.fc`), que originalmente tenía 1000 salidas para ImageNet, por una nueva capa lineal conectada a las neuronas correspondientes a las **N clases específicas** del dataset del proyecto:
$$\text{Capa fc reemplazada: } \text{Linear}(\text{in\_features}=512, \text{out\_features}=N)$$

### B. Hiperparámetros de Entrenamiento
* **Función de Pérdida (Loss Function):** *CrossEntropyLoss*, adecuada para problemas de clasificación multiclase al combinar internamente `LogSoftmax` y la pérdida de entropía cruzada negativa.
* **Optimitzador:** *Adam* con una tasa de aprendizaje (Learning Rate) baja ($\eta = 0.0001$), aplicando descenso de gradiente únicamente a la capa clasificadora no congelada (`model.fc.parameters()`).
* **Tamaño del lote (Batch Size):** 32 imágenes.
* **Épocas:** 38 épocas de entrenamiento.

---

## 5. Integración de LLM y Seguridad de Chatbot (System Prompting)

Para enriquecer la experiencia de usuario y dotar al sistema de capacidades explicativas avanzadas, se integró un **chatbot conversacional** basado en el modelo fundacional de lenguaje **Gemini 1.5 Flash**. 

### A. Seguridad de Acceso y Proxy Backend
El cliente web no realiza llamadas directas a los servidores de Google para evitar la exposición pública del token secreto (`GEMINI_API_KEY`) en el código JavaScript del frontend. En su lugar, el backend de FastAPI actúa como un proxy seguro, interceptando los mensajes del usuario, adjuntando las directivas de seguridad e interactuando con Gemini mediante variables de entorno del sistema de forma confidencial.

### B. Acotamiento mediante System Prompting Dinámico
Para cumplir con la restricción de que el chatbot responda **exclusivamente** sobre la temática del clasificador, el backend construye dinámicamente un **System Prompt** antes de invocar la API de inferencia de Gemini. El script lee la estructura del clasificador (`classes.json`) e inyecta las clases detectadas en las directivas del sistema:

* **Inyección Dinámica:** El prompt del sistema se autoconfigura con la lista literal de clases: `{lista_de_clases}` (ej. *"gato siames, gato persa, gato angora"*).
* **Restricción de Contexto:** Se define una instrucción explícita que instruye al modelo de lenguaje a evaluar si la consulta del usuario pertenece al dominio del clasificador.
* **Manejo de Respuestas Fuera de Tema:** Si la consulta es ajena (ej. matemáticas, geografía, programación), el modelo tiene prohibido generar respuestas informativas. Debe rechazar la solicitud amablemente y reorientar al usuario al tema central.
* **Mitigación de "Jailbreaks":** El prompt de sistema cuenta con una cláusula de precedencia absoluta que anula cualquier intento del usuario de forzar al LLM a ignorar sus directivas base (modos simulador, inyecciones de prompt).

---

## 6. Conclusiones
La combinación de una CNN de PyTorch para el procesamiento inteligente con un frontend web personalizado y reactivo en un servidor FastAPI demuestra el ciclo completo de desarrollo de un producto de software de Inteligencia Artificial (MLOps). El chatbot integrado con Gemini añade una capa de interactividad conversacional robusta, demostrando cómo los modelos fundacionales pueden acotarse de forma segura mediante ingeniería de prompts dinámicos.

El uso de contenedores Docker y el despliegue en Hugging Face Spaces resuelve los retos tradicionales de hosting de modelos pesados de Deep Learning, proporcionando un enlace público estable y de acceso instantáneo para la evaluación académica.
