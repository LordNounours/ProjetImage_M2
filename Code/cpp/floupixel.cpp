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
void floupixel(unsigned char *ImgIn , unsigned char *ImgOut, int nH , int nW , int taillePixel)
{
    int pas = sqrt(taillePixel);
    
    for(int i = 0 ; i < nH ; i+=pas)
    {
        for (int j = 0 ; j < nW * 3 ; j+=pas*3)
        {
            
            int moypixelR = 0;
            int moypixelV = 0;
            int moypixelB = 0;
            
            for (int k = i ; k < i + pas ; k++)
            {
                for (int l = j ; l < j + pas*3 ; l+=3)
                {
                    
                    int indiceR =  min(nH * nW *3 , k * nW * 3 + l);
                    int indiceV =  min(nH * nW *3 , k * nW * 3 + l + 1);
                    int indiceB =  min(nH * nW *3 , k * nW * 3 + l + 2);
                    
                    std::cout<<indiceR << " " << indiceV << " "<< indiceB<<std::endl;
                    moypixelR += ImgIn[indiceR];
                    moypixelV += ImgIn[indiceV];
                    moypixelB += ImgIn[indiceB];
                    
                }
            } 

            moypixelR /= taillePixel;
            moypixelV /= taillePixel;
            moypixelB /= taillePixel;
            
            for (int k = i ; k < i + pas ; k++)
            {
                for (int l = j ; l < j + pas*3 ; l+=3)
                {
                    
                    int indiceR =  min(nH * nW *3 ,k * nW * 3 + l);
                    int indiceV =  min(nH * nW *3 ,k * nW * 3 + l + 1);
                    int indiceB =  min(nH * nW *3 ,k * nW * 3 + l + 2);
                    
                    ImgOut[indiceR] = moypixelR;
                    ImgOut[indiceV] = moypixelV;
                    ImgOut[indiceB] = moypixelB;

                }
            }
        }
        
    }
    
    
    
}


int main(int argc, char* argv[])
{
    char cNomImgLue[250],cNomImgOut[250];
    int nH, nW, nTaille,taillePixel;
  
    if (argc != 4) 
        {
        printf("Usage: ImageIn.png  ImgOut.png tailledespixels \n"); 
        exit (1) ;
        }

    sscanf (argv[1],"%s",cNomImgLue) ;
    sscanf (argv[2],"%s",cNomImgOut);
    sscanf (argv[3],"%d",&taillePixel); //n²

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
    floupixel(ImgIn,ImgOut,nH,nW,taillePixel);
    
     if (!stbi_write_png(cNomImgOut, nW, nH, 3, ImgOut, nW *3)) {
        std::cerr << "Erreur lors de l'enregistrement de l'image." << std::endl;
    }
    stbi_image_free(ImgIn);
    free(ImgOut);
    return 1;
}
