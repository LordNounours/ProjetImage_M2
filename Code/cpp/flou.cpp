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



void generateGaussianKernel(vector<vector<float>>& kernel, int k, float sigma) {
    float sum = 0.0;
    int half_k = k / 2;
    for (int i = -half_k; i <= half_k; ++i) {
        for (int j = -half_k; j <= half_k; ++j) {
            float value = exp(-(i * i + j * j) / (2 * sigma * sigma)) / (2 * M_PI * sigma * sigma);
            kernel[i + half_k][j + half_k] = value;
            sum += value;
        }
    }
    for (int i = 0; i < k; ++i) {
        for (int j = 0; j < k; ++j) {
            kernel[i][j] /= sum;
        }
    }
}

void flou(unsigned char *ImgIn, unsigned char *ImgOut, int nH, int nW, int k,float sigma) {
    vector<vector<float>> kernel(k, vector<float>(k, 0));
    generateGaussianKernel(kernel, k, sigma);

    int half_k = k / 2;
    for (int y = 0; y < nH; ++y) {
        for (int x = 0; x < nW; ++x) {
            float sumR = 0.0, sumG = 0.0, sumB = 0.0;
            float norm = 0.0;
            for (int ky = -half_k; ky <= half_k; ++ky) {
                for (int kx = -half_k; kx <= half_k; ++kx) {
                    int iy = y + ky;
                    int ix = x + kx;
                    if (iy >= 0 && iy < nH && ix >= 0 && ix < nW) {
                        sumR += ImgIn[(iy * nW + ix) * 3] * kernel[ky + half_k][kx + half_k];
                        sumG += ImgIn[(iy * nW + ix) * 3 + 1] * kernel[ky + half_k][kx + half_k];
                        sumB += ImgIn[(iy * nW + ix) * 3 + 2] * kernel[ky + half_k][kx + half_k];
                        norm += kernel[ky + half_k][kx + half_k];
                    }
                }
            }
            ImgOut[(y * nW + x) * 3] = (unsigned char)min(max(int(sumR / norm), 0), 255);
            ImgOut[(y * nW + x) * 3 + 1] = (unsigned char)min(max(int(sumG / norm), 0), 255);
            ImgOut[(y * nW + x) * 3 + 2] = (unsigned char)min(max(int(sumB / norm), 0), 255);
        }
    }
}

int main(int argc, char* argv[])
{
    char cNomImgLue[250],cNomImgOut[250];
    int nH, nW, nTaille,k;
    float sigma;
  
    if (argc != 5) 
        {
        printf("Usage: ImageIn.png  ImgOut.png k \n"); 
        exit (1) ;
        }

    sscanf (argv[1],"%s",cNomImgLue) ;
    sscanf (argv[2],"%s",cNomImgOut);
    sscanf (argv[3],"%d",&k);
    sscanf (argv[4],"%f",&sigma);


    unsigned char *ImgIn, *ImgConv,*ImgOut;
    int channels;
    ImgIn = stbi_load(cNomImgLue, &nW, &nH, &channels, STBI_rgb);
    if (ImgIn == NULL) {
        std::cerr << "Erreur lors du chargement des images." << std::endl;
        return 1;
    }
    nTaille = nH * nW;
    ImgOut = (unsigned char *)malloc(3 * nTaille * sizeof(unsigned char));
    memset(ImgOut, 0, 3 * nTaille * sizeof(unsigned char));
    flou(ImgIn,ImgOut,nH,nW,k,sigma);
    
     if (!stbi_write_png(cNomImgOut, nW, nH, 3, ImgOut, nW *3)) {
        std::cerr << "Erreur lors de l'enregistrement de l'image." << std::endl;
    }
    stbi_image_free(ImgIn);
    free(ImgOut);
    return 1;
}