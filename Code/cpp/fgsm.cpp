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
            int px = min(max(x + kx, 0), nW - 1);
            int py = min(max(y + ky, 0), nH - 1);
            gradient += ImgIn[(py * nW + px) * 3 + channel] * filter[ky + 1][kx + 1];
        }
    }
    return gradient;
}

void FGSM(unsigned char *ImgIn, unsigned char *ImgOut, int nH, int nW, float epsilon) {
    for (int y = 0; y < nH; ++y) {
        for (int x = 0; x < nW; ++x) {
            for (int c = 0; c < 3; ++c) {
                int gradient_x = calculateSobelGradient(ImgIn, nW, nH, x, y, c, sobel_x);
                int gradient_y = calculateSobelGradient(ImgIn, nW, nH, x, y, c, sobel_y);
                int gradient = sqrt(gradient_x * gradient_x + gradient_y * gradient_y);

                int pixel_val = ImgIn[(y * nW + x) * 3 + c];
                if (gradient != 0) {
                    int sign = gradient > 0 ? 1 : -1;
                    int perturbed_value = pixel_val + epsilon * sign;
                    perturbed_value = min(max(perturbed_value, 0), 255);
                    ImgOut[(y * nW + x) * 3 + c] = perturbed_value;
                } else {
                    ImgOut[(y * nW + x) * 3 + c] = pixel_val;
                }
            }
        }
    }
}

int main(int argc, char* argv[]) {
    char cNomImgLue[250], cNomImgOut[250];
    int nH, nW, nTaille;
    float epsilon;

    if (argc < 4) {
        printf("Usage: ImageIn.png ImgOut.png epsilon \n");
        exit(1);
    }

    sscanf(argv[1], "%s", cNomImgLue);
    sscanf(argv[2], "%s", cNomImgOut);
    sscanf(argv[3], "%f", &epsilon);

    unsigned char *ImgIn, *ImgOut;
    int channels;
    ImgIn = stbi_load(cNomImgLue, &nW, &nH, &channels, STBI_rgb);
    if (ImgIn == NULL) {
        cerr << "Erreur lors du chargement de l'image." << endl;
        return 1;
    }
    nTaille = nH * nW;
    ImgOut = (unsigned char *)malloc(3 * nTaille * sizeof(unsigned char));
    memset(ImgOut, 0, 3 * nTaille * sizeof(unsigned char));

    FGSM(ImgIn, ImgOut, nH, nW, epsilon);

    if (!stbi_write_png(cNomImgOut, nW, nH, 3, ImgOut, nW * 3)) {
        cerr << "Erreur lors de l'enregistrement de l'image." << endl;
    }

    stbi_image_free(ImgIn);
    free(ImgOut);
    return 0;
}
