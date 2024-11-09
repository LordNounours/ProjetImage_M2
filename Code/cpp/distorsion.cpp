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

void distortion(unsigned char *ImgIn, unsigned char *ImgOut, int nH, int nW, float amplitude, float frequency) {
    for (int y = 0; y < nH; ++y) {
        for (int x = 0; x < nW; ++x) {
            int newX = x + amplitude * sin(2 * M_PI * y / frequency);
            int newY = y + amplitude * sin(2 * M_PI * x / frequency);
            newX = std::min(std::max(newX, 0), nW - 1);
            newY = std::min(std::max(newY, 0), nH - 1);
            ImgOut[(y * nW + x) * 3] = ImgIn[(newY * nW + newX) * 3];
            ImgOut[(y * nW + x) * 3 + 1] = ImgIn[(newY * nW + newX) * 3 + 1];
            ImgOut[(y * nW + x) * 3 + 2] = ImgIn[(newY * nW + newX) * 3 + 2];
        }
    }
}

void inverse_distortion(unsigned char *ImgIn, unsigned char *ImgOut, int nH, int nW, float amplitude, float frequency) {
    for (int y = 0; y < nH; ++y) {
        for (int x = 0; x < nW; ++x) {
            int originalX = x - amplitude * sin(2 * M_PI * y / frequency);
            int originalY = y - amplitude * sin(2 * M_PI * x / frequency);
            
            int origX = std::min(std::max(originalX, 0), nW - 1);
            int origY = std::min(std::max(originalY, 0), nH - 1);
            
            ImgOut[(y * nW + x) * 3] = ImgIn[(origY * nW + origX) * 3];
            ImgOut[(y * nW + x) * 3 + 1] = ImgIn[(origY * nW + origX) * 3 + 1];
            ImgOut[(y * nW + x) * 3 + 2] = ImgIn[(origY * nW + origX) * 3 + 2];
        }
    }
}
int main(int argc, char* argv[]) {
    char cNomImgLue[250], cNomImgOut[250],cNomImgRev[250];
    int nH, nW, nTaille;
    float amplitude, frequency;
    bool useBlur = true;

    if (argc < 6) {
        printf("Usage: ImageIn.png ImgOut.png ImgRev.png  amplitude frequency \n");
        exit(1);
    }

    sscanf(argv[1], "%s", cNomImgLue);
    sscanf(argv[2], "%s", cNomImgOut);
    sscanf(argv[3], "%s", cNomImgRev);
    sscanf(argv[4], "%f", &amplitude);
    sscanf(argv[5], "%f", &frequency);

    unsigned char *ImgIn, *ImgOut,*ImgRev;
    int channels;
    ImgIn = stbi_load(cNomImgLue, &nW, &nH, &channels, STBI_rgb);
    if (ImgIn == NULL) {
        std::cerr << "Erreur lors du chargement des images." << std::endl;
        return 1;
    }
    nTaille = nH * nW;
    ImgOut = (unsigned char *)malloc(3 * nTaille * sizeof(unsigned char));
    memset(ImgOut, 0, 3 * nTaille * sizeof(unsigned char));

   
    distortion(ImgIn, ImgOut, nH, nW, amplitude, frequency);

    ImgRev = (unsigned char *)malloc(3 * nTaille * sizeof(unsigned char));
    memset(ImgRev, 0, 3 * nTaille * sizeof(unsigned char));
    if (!stbi_write_png(cNomImgOut, nW, nH, 3, ImgOut, nW * 3)) {
        std::cerr << "Erreur lors de l'enregistrement de l'image distordue." << std::endl;
    } else {
        std::cout << "Image distordue enregistrée avec succès : " << cNomImgOut << std::endl;
    }
    
    inverse_distortion(ImgOut,ImgRev,nH,nW,amplitude,frequency);
    if (!stbi_write_png(cNomImgRev, nW, nH, 3, ImgRev, nW * 3)) {
        std::cerr << "Erreur lors de l'enregistrement de l'image inversée." << std::endl;
    } else {
        std::cout << "Image inversée enregistrée avec succès : " << cNomImgRev << std::endl;
    }

    stbi_image_free(ImgIn);
    free(ImgOut);
    free(ImgRev);
    return 0;
}