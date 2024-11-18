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

// Fonction pour appliquer l'attaque FGSM
void FGSM(unsigned char *ImgIn, unsigned char *ImgOut, int nH, int nW, float epsilon) {
    // Parcours de chaque pixel de l'image
    for (int y = 0; y < nH; ++y) {
        for (int x = 0; x < nW; ++x) {
            // Calculer le gradient simulé pour chaque composant RGB
            // Ici, nous simulons le gradient comme étant la différence entre les valeurs RGB du pixel
            // et leur moyenne (vous pouvez ajuster cette logique pour un vrai modèle de machine learning)

            // Pour simplifier, on calcule simplement la variation du pixel (c'est une approximation)
            for (int c = 0; c < 3; ++c) {  // Parcours des trois canaux (R, G, B)
                // Simulation du gradient : nous utilisons la différence entre la valeur du pixel et une valeur cible (ici 128)
                int pixel_val = ImgIn[(y * nW + x) * 3 + c];
                int gradient = pixel_val - 128; // Différence par rapport à une valeur centrale (c'est une approximation)

                // Application de la perturbation : ajout du signe du gradient multiplié par epsilon
                int perturbed_value = pixel_val - epsilon * gradient / abs(gradient);  // Simplification du calcul du signe

                // Assurer que la valeur du pixel reste dans les limites [0, 255]
                perturbed_value = std::min(std::max(perturbed_value, 0), 255);

                // Enregistrer la nouvelle valeur perturbée dans ImgOut
                ImgOut[(y * nW + x) * 3 + c] = perturbed_value;
            }
        }
    }
}

int main(int argc, char* argv[]) {
    char cNomImgLue[250], cNomImgOut[250];
    int nH, nW, nTaille;
    float epsilon;  // Facteur d'amplitude de la perturbation (epsilon)

    if (argc < 4) {
        printf("Usage: ImageIn.png ImgOut.png epsilon \n");
        exit(1);
    }

    // Lecture des arguments
    sscanf(argv[1], "%s", cNomImgLue);
    sscanf(argv[2], "%s", cNomImgOut);
    sscanf(argv[3], "%f", &epsilon);

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

    // Appliquer l'attaque FGSM
    FGSM(ImgIn, ImgOut, nH, nW, epsilon);

    // Sauvegarder l'image modifiée
    if (!stbi_write_png(cNomImgOut, nW, nH, 3, ImgOut, nW * 3)) {
        std::cerr << "Erreur lors de l'enregistrement de l'image." << std::endl;
    }

    stbi_image_free(ImgIn);
    free(ImgOut);
    return 0;
}
