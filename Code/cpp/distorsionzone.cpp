#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <cmath>
#include <vector>
#define STB_IMAGE_IMPLEMENTATION
#include "../lib/stb_image.h" 
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "../lib/stb_image_write.h"
using namespace std;

void distortion(unsigned char *ImgIn, unsigned char *ImgOut, int nH, int nW, float amplitude, float frequency, int x_start, int y_start, int x_end, int y_end) {
    for (int y = 0; y < nH; ++y) {
        for (int x = 0; x < nW; ++x) {
            if (x >= x_start && x < x_end && y >= y_start && y < y_end) { 
                int newX = x + amplitude * sin(2 * M_PI * y / frequency);
                int newY = y + amplitude * sin(2 * M_PI * x / frequency);
                newX = std::min(std::max(newX, 0), nW - 1);
                newY = std::min(std::max(newY, 0), nH - 1);
                ImgOut[(y * nW + x) * 3] = ImgIn[(newY * nW + newX) * 3];
                ImgOut[(y * nW + x) * 3 + 1] = ImgIn[(newY * nW + newX) * 3 + 1];
                ImgOut[(y * nW + x) * 3 + 2] = ImgIn[(newY * nW + newX) * 3 + 2];
            } else {
                ImgOut[(y * nW + x) * 3] = ImgIn[(y * nW + x) * 3];
                ImgOut[(y * nW + x) * 3 + 1] = ImgIn[(y * nW + x) * 3 + 1];
                ImgOut[(y * nW + x) * 3 + 2] = ImgIn[(y * nW + x) * 3 + 2];
            }
        }
    }
}

int main(int argc, char* argv[]) {
    char cNomImgLue[250], cNomImgOut[250];
    int nH, nW, nTaille,x_start,x_end,y_start,y_end;
    float amplitude, frequency;
    bool useBlur = true;

    if (argc < 9) {
        printf("Usage: ImageIn.png ImgOut.png  amplitude frequency \n");
        exit(1);
    }

    sscanf(argv[1], "%s", cNomImgLue);
    sscanf(argv[2], "%s", cNomImgOut);
    sscanf(argv[3], "%f", &amplitude);
    sscanf(argv[4], "%f", &frequency);
    sscanf(argv[5], "%d", &x_start);
    sscanf(argv[6], "%d", &x_end);
    sscanf(argv[7], "%d", &y_start);
    sscanf(argv[8], "%d", &y_end);

    unsigned char *ImgIn, *ImgOut;
    int channels;
    ImgIn = stbi_load(cNomImgLue, &nW, &nH, &channels, STBI_rgb);
    if (ImgIn == NULL) {
        std::cerr << "Erreur lors du chargement des images." << std::endl;
        return 1;
    }
    nTaille = nH * nW;
    ImgOut = (unsigned char *)malloc(3 * nTaille * sizeof(unsigned char));
    memset(ImgOut, 0, 3 * nTaille * sizeof(unsigned char));

   
    distortion(ImgIn, ImgOut, nH, nW, amplitude, frequency,x_start,y_start,x_end,y_end);
    

    if (!stbi_write_png(cNomImgOut, nW, nH, 3, ImgOut, nW * 3)) {
        std::cerr << "Erreur lors de l'enregistrement de l'image." << std::endl;
    }

    stbi_image_free(ImgIn);
    free(ImgOut);
    return 0;
}