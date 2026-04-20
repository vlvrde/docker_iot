# ──────────────────────────────────────────────
# Contenedor adicional: Gráfica de sensores IoT
# Lenguaje: Python 3.12 + Pillow
# ──────────────────────────────────────────────
FROM python:3.12-slim

WORKDIR /app

# Instalar Pillow (procesamiento de imágenes)
RUN pip install --no-cache-dir Pillow==10.3.0

COPY src/sensor_chart.py .

RUN mkdir /output

CMD ["python", "sensor_chart.py"]
