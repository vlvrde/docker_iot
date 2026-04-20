# ──────────────────────────────────────────────
# Etapa 1: Compilar el programa en C
# ──────────────────────────────────────────────
FROM gcc:13 AS builder

WORKDIR /app

# Instalar libjpeg
RUN apt-get update && \
    apt-get install -y --no-install-recommends libjpeg-dev && \
    rm -rf /var/lib/apt/lists/*

COPY src/genera_imagen.c .

# Compilar enlazando contra libjpeg
RUN gcc -O2 -Wall -o genera_imagen genera_imagen.c -ljpeg

# ──────────────────────────────────────────────
# Etapa 2: Imagen mínima de ejecución
# ──────────────────────────────────────────────
FROM debian:bookworm-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends libjpeg62-turbo && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar solo el binario compilado
COPY --from=builder /app/genera_imagen .

# Directorio de salida (se montará como volumen)
RUN mkdir /output

CMD ["./genera_imagen"]
