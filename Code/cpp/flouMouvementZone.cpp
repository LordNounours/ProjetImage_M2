#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <cmath>
#include <vector>
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h" 
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"
using namespace std;

void generateMotionBlurKernel(vector<vector<float>>& kernel, int length, int direction) {
    float sum = 0.0;
    int half_length = length / 2;
    //0 horizntal , 1 vertical
    if (direction == 0) {
        for (int i = -half_length; i <= half_length; ++i) {
            kernel[half_length][i + half_length] = 1.0;
            sum += 1.0;
        }
    } else if (direction == 1) {
        for (int i = -half_length; i <= half_length; ++i) {
            kernel[i + half_length][half_length] = 1.0;
            sum += 1.0;
        }
    }

    for (int i = 0; i < length; ++i) {
        for (int j = 0; j < length; ++j) {
            kernel[i][j] = (sum > 0) ? kernel[i][j] / sum : 0;
        }
    }
}

void motionBlur(unsigned char *ImgIn, unsigned char *ImgOut, int nH, int nW, int length, int direction, int x_start, int y_start, int x_end, int y_end) {
    vector<vector<float>> kernel(length, vector<float>(length, 0));
    generateMotionBlurKernel(kernel, length, direction);

    int half_length = length / 2;
    for (int y = 0; y < nH; ++y) {
        for (int x = 0; x < nW; ++x) {
            if (x >= x_start && x < x_end && y >= y_start && y < y_end) {//zone de flou
                float sumR = 0.0, sumG = 0.0, sumB = 0.0;
                float norm = 0.0;
                for (int ky = -half_length; ky <= half_length; ++ky) {
                    for (int kx = -half_length; kx <= half_length; ++kx) {
                        int iy = y + ky;
                        int ix = x + kx;
                        if (direction == 0 && iy >= 0 && iy < nH && ix >= 0 && ix < nW) {
                            sumR += ImgIn[(y * nW + ix) * 3] * kernel[half_length][kx + half_length];
                            sumG += ImgIn[(y * nW + ix) * 3 + 1] * kernel[half_length][kx + half_length];
                            sumB += ImgIn[(y * nW + ix) * 3 + 2] * kernel[half_length][kx + half_length];
                            norm += kernel[half_length][kx + half_length];
                        } else if (direction == 1 && iy >= 0 && iy < nH && ix >= 0 && ix < nW) {
                            sumR += ImgIn[(iy * nW + x) * 3] * kernel[ky + half_length][half_length];
                            sumG += ImgIn[(iy * nW + x) * 3 + 1] * kernel[ky + half_length][half_length];
                            sumB += ImgIn[(iy * nW + x) * 3 + 2] * kernel[ky + half_length][half_length];
                            norm += kernel[ky + half_length][half_length];
                        }
                    }
                }

                ImgOut[(y * nW + x) * 3] = (unsigned char)min(max(int(sumR / norm), 0), 255);
                ImgOut[(y * nW + x) * 3 + 1] = (unsigned char)min(max(int(sumG / norm), 0), 255);
                ImgOut[(y * nW + x) * 3 + 2] = (unsigned char)min(max(int(sumB / norm), 0), 255);
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
    int nH, nW, nTaille, length, direction;
    int x_start, y_start, x_end, y_end;//zone de flou

    if (argc != 9) {
        printf("Usage: ImageIn.png ImgOut.png length direction x_start y_start x_end y_end\n");
        exit(1);
    }

    sscanf(argv[1], "%s", cNomImgLue);
    sscanf(argv[2], "%s", cNomImgOut);
    sscanf(argv[3], "%d", &length);
    sscanf(argv[4], "%d", &direction);
    sscanf(argv[5], "%d", &x_start);
    sscanf(argv[6], "%d", &y_start);
    sscanf(argv[7], "%d", &x_end);
    sscanf(argv[8], "%d", &y_end);

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

    motionBlur(ImgIn, ImgOut, nH, nW, length, direction, x_start, y_start, x_end, y_end);

    if (!stbi_write_png(cNomImgOut, nW, nH, 3, ImgOut, nW * 3)) {
        std::cerr << "Erreur lors de l'enregistrement de l'image." << std::endl;
    }

    stbi_image_free(ImgIn);
    free(ImgOut);
    return 0;
}
