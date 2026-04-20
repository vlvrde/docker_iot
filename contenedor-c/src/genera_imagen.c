#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <jpeglib.h>

#define WIDTH    640
#define HEIGHT   480
#define CHANNELS 3

typedef unsigned char u8;

void set_pixel(u8 *img, int x, int y, u8 r, u8 g, u8 b) {
    if (x < 0 || x >= WIDTH || y < 0 || y >= HEIGHT) return;
    int idx = (y * WIDTH + x) * CHANNELS;
    img[idx] = r; img[idx+1] = g; img[idx+2] = b;
}

void draw_rect(u8 *img, int x0, int y0, int w, int h, u8 r, u8 g, u8 b) {
    for (int y = y0; y < y0+h; y++)
        for (int x = x0; x < x0+w; x++)
            set_pixel(img, x, y, r, g, b);
}

void draw_circle(u8 *img, int cx, int cy, int rad, u8 r, u8 g, u8 b) {
    for (int y = cy-rad; y <= cy+rad; y++)
        for (int x = cx-rad; x <= cx+rad; x++)
            if ((x-cx)*(x-cx)+(y-cy)*(y-cy) <= rad*rad)
                set_pixel(img, x, y, r, g, b);
}

void draw_gradient(u8 *img) {
    for (int y = 0; y < HEIGHT; y++)
        for (int x = 0; x < WIDTH; x++) {
            int idx = (y*WIDTH+x)*CHANNELS;
            img[idx]   = (u8)(30 + x*60/WIDTH);
            img[idx+1] = (u8)(10 + y*80/HEIGHT);
            img[idx+2] = (u8)(80 + x*100/WIDTH);
        }
}

int save_jpg(const char *path, u8 *img, int quality) {
    FILE *f = fopen(path, "wb");
    if (!f) { perror("fopen"); return 0; }

    struct jpeg_compress_struct cinfo;
    struct jpeg_error_mgr jerr;
    cinfo.err = jpeg_std_error(&jerr);
    jpeg_create_compress(&cinfo);
    jpeg_stdio_dest(&cinfo, f);

    cinfo.image_width      = WIDTH;
    cinfo.image_height     = HEIGHT;
    cinfo.input_components = CHANNELS;
    cinfo.in_color_space   = JCS_RGB;
    jpeg_set_defaults(&cinfo);
    jpeg_set_quality(&cinfo, quality, TRUE);
    jpeg_start_compress(&cinfo, TRUE);

    JSAMPROW row;
    while (cinfo.next_scanline < cinfo.image_height) {
        row = img + cinfo.next_scanline * WIDTH * CHANNELS;
        jpeg_write_scanlines(&cinfo, &row, 1);
    }
    jpeg_finish_compress(&cinfo);
    jpeg_destroy_compress(&cinfo);
    fclose(f);
    return 1;
}

int main(void) {
    u8 *img = calloc(WIDTH * HEIGHT * CHANNELS, 1);
    if (!img) { fprintf(stderr, "Error: memoria insuficiente\n"); return 1; }

    draw_gradient(img);

    /* Panel blanco */
    draw_rect(img,  80,  60, 480, 360, 255,255,255);
    /* Barra azul de titulo */
    draw_rect(img,  80,  60, 480,  50,  41,128,185);
    /* Botones de ventana */
    draw_circle(img, 108, 85, 10, 255, 95,  86);
    draw_circle(img, 136, 85, 10, 255,189,  46);
    draw_circle(img, 164, 85, 10,  40,201,  64);
    /* Lineas de codigo simuladas */
    int widths[] = {200,280,160,240,180,260,140,220};
    for (int i = 0; i < 8; i++)
        draw_rect(img, 110, 140+i*28, widths[i], 10, 180,180,180);
    /* Terminal en la parte inferior */
    draw_rect(img,  80, 330, 480, 90,  30, 30, 30);
    draw_rect(img, 100, 350, 180,  8,  50,205, 50);
    draw_rect(img, 100, 368, 120,  8, 255,165,  0);
    draw_rect(img, 100, 386, 220,  8,  50,205, 50);
    /* Circulo decorativo esquina superior derecha */
    draw_circle(img, 520, 230, 60, 230, 240, 255);
    draw_circle(img, 520, 230, 45, 41, 128, 185);

    const char *out = "/output/imagen_generada.jpg";
    if (save_jpg(out, img, 90))
        printf("✔ Imagen guardada en %s (%dx%d, %d canales)\n", out, WIDTH, HEIGHT, CHANNELS);
    else {
        fprintf(stderr, "Error al guardar la imagen\n");
        free(img); return 1;
    }
    free(img);
    return 0;
}
