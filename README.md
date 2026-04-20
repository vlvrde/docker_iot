# 🐳 Proyecto Docker – Embedded IoT

> **Materia:** INTERNET DE LAS COSAS|EMBEDDED SYSTEMS  
> **Descripción:** Contenedores Docker para generación de imágenes: uno con C + libjpeg y otro con Python + Pillow.

---

## 📂 Estructura del Repositorio

```
docker-project/
├── contenedor-c/               # Contenedor 1: Programa en C que genera JPG
│   ├── Dockerfile
│   └── src/
│       └── genera_imagen.c
├── contenedor-python/          # Contenedor 2: Programa Python que genera PNG
│   ├── Dockerfile
│   └── src/
│       └── sensor_chart.py
├── evidencia/                  # Capturas y logs de ejecución
│   ├── imagen_generada.jpg
│   ├── sensor_chart.png
│   └── logs.txt
├── .gitignore
└── README.md                   
```

---

## 🐋 ¿Qué es Docker?

Docker es una plataforma de **contenedorización** que permite empaquetar una aplicación junto con todas sus dependencias (librerías, configuraciones, sistema operativo base) en una unidad llamada **contenedor**.

### Conceptos clave

| Término | Descripción |
|---------|-------------|
| **Imagen** | Plantilla de solo lectura con las instrucciones para crear un contenedor |
| **Contenedor** | Instancia ejecutable de una imagen; corre de forma aislada |
| **Dockerfile** | Archivo de texto con los pasos para construir una imagen |
| **Docker Hub** | Registro público de imágenes Docker |
| **Volumen** | Mecanismo para persistir datos entre ejecuciones del contenedor |

### Flujo básico

```
Dockerfile → docker build → Imagen → docker run → Contenedor (en ejecución)
```

---

## Contenedor 1 — Programa en C que genera JPG

### Descripción

Programa en C que dibuja una imagen de 640×480 píxeles con:
- Fondo degradado de colores
- Panel simulando una ventana de IDE
- Barra de título con botones de semáforo (macOS-style)
- Líneas de código simuladas
- Terminal en la parte inferior

La imagen se guarda en formato **JPEG** usando la librería `libjpeg`.

### Construir y ejecutar

```bash
# 1. Entrar al directorio del contenedor
cd contenedor-c

# 2. Construir la imagen Docker
docker build -t imagen-c-jpg .

# 3. Ejecutar el contenedor (montar carpeta local como /output)
docker run --rm -v $(pwd)/output:/output imagen-c-jpg
```

> 💡 La flag `-v $(pwd)/output:/output` monta la carpeta `output/` local
> como `/output` dentro del contenedor, donde el programa guardará el JPG.

### Verificar la salida

```bash
ls output/
# imagen_generada.jpg
```

### Explicación del Dockerfile (multi-stage build)

```dockerfile
# Etapa 1: Compilar con GCC
FROM gcc:13 AS builder
RUN apt-get install -y libjpeg-dev
COPY src/genera_imagen.c .
RUN gcc -O2 -o genera_imagen genera_imagen.c -ljpeg

# Etapa 2: Imagen mínima de ejecución
FROM debian:bookworm-slim
RUN apt-get install -y libjpeg62-turbo
COPY --from=builder /app/genera_imagen .
CMD ["./genera_imagen"]
```

El **multi-stage build** reduce el tamaño final: la imagen de producción no
incluye GCC ni los headers de desarrollo.

---

## Contenedor 2 — Gráfica de Sensores IoT (Python)

### Descripción

Programa en Python 3 que simula 24 horas de lecturas de tres sensores IoT y
genera una gráfica en formato **PNG**:

- 🌡️ **Temperatura** (°C) — curva roja-naranja
- 💧 **Humedad** (%) — curva azul
- 📊 **Presión** (normalizada) — curva verde

Los datos se generan con una función senoidal + ruido aleatorio para simular
comportamiento real de sensores.

### Construir y ejecutar

```bash
# 1. Entrar al directorio del contenedor
cd contenedor-python

# 2. Construir la imagen Docker
docker build -t sensor-chart-py .

# 3. Ejecutar el contenedor
docker run --rm -v $(pwd)/output:/output sensor-chart-py
```

### Verificar la salida

```bash
ls output/
# sensor_chart.png
```

### Explicación del Dockerfile

```dockerfile
FROM python:3.12-slim          # Imagen base oficial de Python ligera
RUN pip install Pillow         # Librería de procesamiento de imágenes
COPY src/sensor_chart.py .
CMD ["python", "sensor_chart.py"]
```

---

## ⚡ Comandos Docker de Referencia

```bash
# Ver imágenes disponibles localmente
docker images

# Ver contenedores en ejecución
docker ps

# Ver todos los contenedores (incluyendo detenidos)
docker ps -a

# Eliminar una imagen
docker rmi imagen-c-jpg

# Ver logs de un contenedor
docker logs <container_id>

# Ejecutar shell interactivo dentro de un contenedor
docker run -it --rm imagen-c-jpg /bin/bash

# Eliminar contenedores detenidos
docker container prune

# Inspeccionar una imagen
docker inspect imagen-c-jpg
```

---

## 📸 Evidencia de Ejecución

Las imágenes generadas y los logs se encuentran en la carpeta [`evidencia/`](./evidencia/).

| Archivo | Descripción |
|---------|-------------|
| `imagen_generada.jpg` | Salida del programa en C (640×480 px) |
| `sensor_chart.png` | Gráfica del programa en Python (900×500 px) |
| `logs.txt` | Salida de consola de ambos contenedores |
| `docker-desktop.png` | Imagenes creadas de ambos programas |

## Imágenes creadas para ambos programas en Docker Desktop
<img width="1579" height="894" alt="image" src="https://github.com/user-attachments/assets/2e92edb7-0ceb-4806-b92d-4dae628e263a" />

## Imágen creada C
<img width="1138" height="49" alt="image" src="https://github.com/user-attachments/assets/31cedf2f-1d02-4e11-9ab8-fd9b70a12b9c" />

## Imágen creada Python
<img width="1182" height="54" alt="image" src="https://github.com/user-attachments/assets/b172aafc-6fa9-4517-9115-de7646c0d1fb" />

---
