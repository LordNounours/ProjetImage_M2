#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <cmath>
#include <vector>
#define STB_IMAGE_IMPLEMENTATION
#include "../lib/stb_image.h"

using namespace std;

void ssim(unsigned char *ImgIn, unsigned char *ImgIn2, int nH, int nW) {
    double k1 = 0.01;
    double k2 = 0.03;
    int L = 255;
    double c1 = (k1 * L) * (k1 * L);
    double c2 = (k2 * L) * (k2 * L);
    double c3 = c2 / 2;
    double ssim[3] = {0};
    int count = 0;

    // Fenetre de 8 par 8
    for (int i = 0; i < nH - 8; i += 2) {
        for (int j = 0; j < nW - 8; j += 2) {
            count++;
            int pos = i * nW + j;

            double moy1[3] = {0}, moy2[3] = {0};
            double var1[3] = {0}, var2[3] = {0};
            double cov[3] = {0};
            for (int k = 0; k < 8; k++) {
                for (int l = 0; l < 8; l++) {
                    for (int c = 0; c < 3; c++) {
                        moy1[c] += ImgIn[3 * (pos + k + l * nW) + c];
                        moy2[c] += ImgIn2[3 * (pos + k + l * nW) + c];
                    }
                }
            }

            for (int c = 0; c < 3; c++) {
                moy1[c] /= 64;
                moy2[c] /= 64;
            }
            for (int k = 0; k < 8; k++) {
                for (int l = 0; l < 8; l++) {
                    for (int c = 0; c < 3; c++) {
                        var1[c] += pow(ImgIn[3 * (pos + k + l * nW) + c] - moy1[c], 2);
                        var2[c] += pow(ImgIn2[3 * (pos + k + l * nW) + c] - moy2[c], 2);
                        cov[c] += (ImgIn[3 * (pos + k + l * nW) + c] - moy1[c]) * (ImgIn2[3 * (pos + k + l * nW) + c] - moy2[c]);
                    }
                }
            }

            for (int c = 0; c < 3; c++) {
                var1[c] /= 64;
                var2[c] /= 64;
                cov[c] /= 64;
            }
            for (int c = 0; c < 3; c++) {
                double num = (2 * moy1[c] * moy2[c] + c1) * (2 * sqrt(var1[c]) * sqrt(var2[c]) + c2) * (cov[c] + c3);
                double den = (pow(moy1[c], 2) + pow(moy2[c], 2) + c1) * (var1[c] + var2[c] + c2) * (sqrt(var1[c]) * sqrt(var2[c]) + c3);
                ssim[c] += num / den;
            }
        }
    }
    for (int c = 0; c < 3; c++) {
        ssim[c] /= count;
        std::cout << "SSIM entre 2 images (canal " << c << ") : " << ssim[c] << std::endl;
    }
    double ssimf = (ssim[0] + ssim[1] + ssim[2]) / 3;
    std::cout << "SSIM moyen entre 2 images : " << ssimf << std::endl;
}

int main(int argc, char *argv[]) {
    char cNomImgIn[250], cNomImgIn2[250];
    int nH, nW, nTaille;

    if (argc != 3) {
        printf("Usage: ImageIn.ppm ImageIn2.ppm \n");
        exit(1);
    }

    sscanf(argv[1], "%s", cNomImgIn);
    sscanf(argv[2], "%s", cNomImgIn2);

    unsigned char *ImgIn, *ImgIn2;

    // Charger les images avec stbi_load
    ImgIn = stbi_load(cNomImgIn, &nW, &nH, NULL, 3);
    ImgIn2 = stbi_load(cNomImgIn2, &nW, &nH, NULL, 3);

    if (ImgIn == NULL || ImgIn2 == NULL) {
        std::cerr << "Erreur lors du chargement des images." << std::endl;
        return 1;
    }

    ssim(ImgIn, ImgIn2, nH, nW);

    stbi_image_free(ImgIn);
    stbi_image_free(ImgIn2);

    return 0;
}
