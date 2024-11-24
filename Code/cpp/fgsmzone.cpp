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

const int sobel_x[3][3] = {
    {-1, 0, 1},
    {-2, 0, 2},
    {-1, 0, 1}
};

const int sobel_y[3][3] = {
    {-1, -2, -1},
    { 0,  0,  0},
    { 1,  2,  1}
};

int calculateSobelGradient(const unsigned char* ImgIn, int nW, int nH, int x, int y, int channel, const int filter[3][3]) {
    int gradient = 0;
    for (int ky = -1; ky <= 1; ++ky) {
        for (int kx = -1; kx <= 1; ++kx) {
            int px = std::min(std::max(x + kx, 0), nW - 1);
            int py = std::min(std::max(y + ky, 0), nH - 1);
            gradient += ImgIn[(py * nW + px) * 3 + channel] * filter[ky + 1][kx + 1];
        }
    }
    return gradient;
}

void FGSM(unsigned char *ImgIn, unsigned char *ImgOut, int nH, int nW, int epsilon, int x_start, int y_start, int x_end, int y_end) {
    for (int y = 0; y < nH; ++y) {
        for (int x = 0; x < nW; ++x) {
            if (x >= x_start && x < x_end && y >= y_start && y < y_end) {
                for (int c = 0; c < 3; ++c) {
                    int gradient_x = calculateSobelGradient(ImgIn, nW, nH, x, y, c, sobel_x);
                    int gradient_y = calculateSobelGradient(ImgIn, nW, nH, x, y, c, sobel_y);
                    int gradient = std::sqrt(gradient_x * gradient_x + gradient_y * gradient_y);

                    if (gradient != 0) {
                        int sign = gradient > 0 ? 1 : -1;
                        int perturbed_value = ImgIn[(y * nW + x) * 3 + c] + epsilon * sign;
                        perturbed_value = std::min(std::max(perturbed_value, 0), 255);
                        ImgOut[(y * nW + x) * 3 + c] = perturbed_value;
                    } else {
                        ImgOut[(y * nW + x) * 3 + c] = ImgIn[(y * nW + x) * 3 + c];
                    }
                }
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
    int nH, nW, nTaille, x_start, y_start, x_end, y_end;
    int epsilon;

    if (argc < 8) {
        printf("Usage: ImageIn.png ImgOut.png epsilon x_start y_start x_end y_end \n");
        exit(1);
    }

    sscanf(argv[1], "%s", cNomImgLue);
    sscanf(argv[2], "%s", cNomImgOut);
    sscanf(argv[3], "%d", &epsilon);
    sscanf(argv[4], "%d", &x_start);
    sscanf(argv[5], "%d", &y_start);
    sscanf(argv[6], "%d", &x_end);
    sscanf(argv[7], "%d", &y_end);

    unsigned char *ImgIn, *ImgOut;
    int channels;
    ImgIn = stbi_load(cNomImgLue, &nW, &nH, &channels, STBI_rgb);
    if (ImgIn == NULL) {
        std::cerr << "Erreur lors du chargement de l'image." << std::endl;
        return 1;
    }
    nTaille = nH * nW;
    ImgOut = (unsigned char *)malloc(3 * nTaille * sizeof(unsigned char));
    memset(ImgOut, 0, 3 * nTaille * sizeof(unsigned char));

    FGSM(ImgIn, ImgOut, nH, nW, epsilon, x_start, y_start, x_end, y_end);

    if (!stbi_write_png(cNomImgOut, nW, nH, 3, ImgOut, nW * 3)) {
        std::cerr << "Erreur lors de l'enregistrement de l'image." << std::endl;
    }

    stbi_image_free(ImgIn);
    free(ImgOut);
    return 0;
}
