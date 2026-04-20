"""
sensor_chart.py
Genera una gráfica PNG que simula datos de sensores IoT:
  - Temperatura (°C)
  - Humedad (%)
  - Presión (hPa, escalada para comparación)
Los datos se generan con ruido aleatorio para simular lecturas reales.
"""

import os
import random
import math

# ── Parámetros de generación ──────────────────────────────────────────────────
N       = 48           # puntos de datos (cada 30 min → 24 horas)
OUTFILE = "/output/sensor_chart.png"
SEED    = 42
random.seed(SEED)

# ── Generación de datos simulados ─────────────────────────────────────────────
hours = [i * 0.5 for i in range(N)]

def gen_series(base, amplitude, noise, phase=0):
    return [
        base + amplitude * math.sin(2 * math.pi * (i / N) + phase)
        + random.uniform(-noise, noise)
        for i in range(N)
    ]

temp     = gen_series(22.0, 6.0,  0.8, phase=0.0)     # temperatura °C
humidity = gen_series(55.0, 15.0, 1.5, phase=1.2)     # humedad %
pressure = gen_series(50.0, 8.0,  1.0, phase=2.5)     # presión escalada

# ── Dibujo manual con PIL / Pillow ────────────────────────────────────────────
from PIL import Image, ImageDraw, ImageFont

W, H       = 900, 500
PAD_L      = 80
PAD_R      = 30
PAD_T      = 60
PAD_B      = 70
PLOT_W     = W - PAD_L - PAD_R
PLOT_H     = H - PAD_T - PAD_B

BG         = (18, 18, 35)
GRID_COLOR = (50, 50, 80)
COLORS     = [(255, 100,  80),   # temp   → rojo-naranja
              ( 60, 180, 255),   # hum    → azul
              ( 80, 220, 120)]   # pres   → verde

img  = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# Título
draw.rectangle([0, 0, W, PAD_T - 5], fill=(28, 28, 55))
draw.text((W // 2, PAD_T // 2), "Monitoreo de Sensores IoT – 24 h",
          fill=(220, 220, 255), anchor="mm")

# Líneas de cuadrícula horizontales (5 divisiones)
y_min, y_max = 20.0, 90.0
for k in range(6):
    vy  = y_min + (y_max - y_min) * k / 5
    py  = PAD_T + PLOT_H - int((vy - y_min) / (y_max - y_min) * PLOT_H)
    draw.line([(PAD_L, py), (W - PAD_R, py)], fill=GRID_COLOR, width=1)
    draw.text((PAD_L - 8, py), f"{vy:.0f}", fill=(150, 150, 200), anchor="rm")

# Líneas de cuadrícula verticales (cada 6 h)
for h_tick in range(0, 25, 6):
    ix = int(h_tick / 24 * (N - 1))
    px = PAD_L + int(ix / (N - 1) * PLOT_W)
    draw.line([(px, PAD_T), (px, PAD_T + PLOT_H)], fill=GRID_COLOR, width=1)
    draw.text((px, PAD_T + PLOT_H + 12), f"{h_tick:02d}:00",
              fill=(150, 150, 200), anchor="mt")

# Ejes
draw.rectangle([PAD_L, PAD_T, W - PAD_R, PAD_T + PLOT_H],
               outline=(100, 100, 160), width=2)

def to_px(val, vmin=y_min, vmax=y_max):
    """Convierte un valor al pixel Y correspondiente."""
    return PAD_T + PLOT_H - int((val - vmin) / (vmax - vmin) * PLOT_H)

def series_to_points(series):
    pts = []
    for i, v in enumerate(series):
        px = PAD_L + int(i / (N - 1) * PLOT_W)
        py = max(PAD_T, min(PAD_T + PLOT_H, to_px(v)))
        pts.append((px, py))
    return pts

# Dibujar series
for series, color in zip([temp, humidity, pressure], COLORS):
    pts = series_to_points(series)
    draw.line(pts, fill=color, width=2)
    for px, py in pts[::6]:          # puntos cada 6 muestras
        draw.ellipse([(px-3, py-3), (px+3, py+3)], fill=color)

# Leyenda
labels = ["Temperatura (°C)", "Humedad (%)", "Presión (norm.)"]
for i, (lbl, col) in enumerate(zip(labels, COLORS)):
    lx = PAD_L + i * 260
    ly = H - PAD_B + 28
    draw.rectangle([(lx, ly), (lx + 20, ly + 10)], fill=col)
    draw.text((lx + 26, ly), lbl, fill=(200, 200, 230), anchor="lt")

# Etiqueta eje X
draw.text((W // 2, H - 15), "Hora del día (hh:mm)",
          fill=(160, 160, 200), anchor="mb")

# Guardar
os.makedirs("/output", exist_ok=True)
img.save(OUTFILE)
print(f"✔ Gráfica guardada en {OUTFILE}  ({W}×{H} px)")
