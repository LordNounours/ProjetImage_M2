#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <cmath>
#include <vector>
#include <limits>
#define STB_IMAGE_IMPLEMENTATION
#include "../lib/stb_image.h" 
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "../lib/stb_image_write.h"
using namespace std;

int luminance(int R , int G , int B)
{
    return 0.299*(float)R + 0.587*(float)G + 0.114*(float)B;
}

void floupixelzone(unsigned char *ImgIn , unsigned char *ImgOut, int nH , int nW , int taillePixel ,int mode ,int x_start, int y_start, int x_end, int y_end)
{
    int pas = sqrt(taillePixel);
    
    for(int i = 0 ; i < nH ; i+=pas)
    {
        for (int j = 0 ; j < nW * 3 ; j+=pas*3)
        {
            if (i >= y_start && i < y_end && j >= x_start * 3  && j < x_end * 3) {
                int colpixelR = 0;
                int colpixelV = 0;
                int colpixelB = 0;
                int Y = 0;
                if (mode == 1)//MIN
                {
                    Y = std::numeric_limits<int>::max();
                    colpixelR = colpixelV = colpixelB = std::numeric_limits<int>::max();
                }
                
                for (int k = i ; k < i + pas ; k++)
                {
                    for (int l = j ; l < j + pas*3 ; l+=3)
                    {
                        
                        int indiceR =  min(nH * nW *3 , k * nW * 3 + l);
                        int indiceV =  min(nH * nW *3 , k * nW * 3 + l + 1);
                        int indiceB =  min(nH * nW *3 , k * nW * 3 + l + 2);
                        
                        if (mode == 0){//AVG
                            colpixelR += ImgIn[indiceR];
                            colpixelV += ImgIn[indiceV];
                            colpixelB += ImgIn[indiceB];
                        }
                        if (mode == 1){//MIN
//                             if (colpixelR > ImgIn[indiceR]) colpixelR = ImgIn[indiceR];
//                             if (colpixelV > ImgIn[indiceV]) colpixelV = ImgIn[indiceV];   composantes séparées
//                             if (colpixelB > ImgIn[indiceB]) colpixelB = ImgIn[indiceB];
                            if (Y > luminance(ImgIn[indiceR] , ImgIn[indiceV] , ImgIn[indiceB]))
                            {
                                
                                colpixelR = ImgIn[indiceR];
                                colpixelV = ImgIn[indiceV];
                                colpixelB = ImgIn[indiceB];
                            }
                        }
                        if (mode == 2){//MAX
//                             if (colpixelR < ImgIn[indiceR]) colpixelR = ImgIn[indiceR];
//                             if (colpixelV < ImgIn[indiceV]) colpixelV = ImgIn[indiceV];   composantes séparées
//                             if (colpixelB < ImgIn[indiceB]) colpixelB = ImgIn[indiceB];
                            if (Y < luminance(ImgIn[indiceR] , ImgIn[indiceV] , ImgIn[indiceB]))
                            {
                                colpixelR = ImgIn[indiceR];
                                colpixelV = ImgIn[indiceV];
                                colpixelB = ImgIn[indiceB];
                            }
                            
                            
                        }
                        
                    }
                }
                if (mode == 0){//AVG
                    colpixelR /= taillePixel;
                    colpixelV /= taillePixel;
                    colpixelB /= taillePixel;
                }
                
                for (int k = i ; k < i + pas ; k++)
                {
                    for (int l = j ; l < j + pas*3 ; l+=3)
                    {
                        
                        int indiceR =  min(nH * nW *3 ,k * nW * 3 + l);
                        int indiceV =  min(nH * nW *3 ,k * nW * 3 + l + 1);
                        int indiceB =  min(nH * nW *3 ,k * nW * 3 + l + 2);
                        

                        ImgOut[indiceR] = colpixelR;
                        ImgOut[indiceV] = colpixelV;
                        ImgOut[indiceB] = colpixelB;
                        
                    }
                }
                
                
            }
            else
            {
                for (int k = i ; k < i + pas ; k++)
                {
                    for (int l = j ; l < j + pas * 3 ; l+=3)
                    {
                        int indiceR =  min(nH * nW *3 ,k * nW * 3 + l);
                        int indiceV =  min(nH * nW *3 ,k * nW * 3 + l + 1);
                        int indiceB =  min(nH * nW *3 ,k * nW * 3 + l + 2);
                        ImgOut[indiceR] = ImgIn[indiceR];
                        ImgOut[indiceV] = ImgIn[indiceV];
                        ImgOut[indiceB] = ImgIn[indiceB];
                    }
                }
            }


        }
        
    }
}



int main(int argc, char* argv[])
{
    char cNomImgLue[250],cNomImgOut[250];
    int nH, nW, nTaille,taillePixel,mode;
    int x_start, y_start, x_end, y_end;//zone de flou
     if (argc != 9) {
        printf("Usage: ImageIn.png ImgOut.png tailledespixels x_start y_start x_end y_end\n");
        exit(1);
    }

    sscanf(argv[1], "%s", cNomImgLue);
    sscanf(argv[2], "%s", cNomImgOut);
    sscanf(argv[3], "%d", &taillePixel);
    sscanf(argv[4], "%d", &mode);
    sscanf(argv[5], "%d", &x_start);
    sscanf(argv[6], "%d", &y_start);
    sscanf(argv[7], "%d", &x_end);
    sscanf(argv[8], "%d", &y_end);

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

    floupixelzone(ImgIn,ImgOut, nH, nW, taillePixel,mode , x_start, y_start, x_end, y_end);
    
     if (!stbi_write_png(cNomImgOut, nW, nH, 3, ImgOut, nW *3)) {
        std::cerr << "Erreur lors de l'enregistrement de l'image." << std::endl;
    }
    stbi_image_free(ImgIn);
    free(ImgOut);
    return 1;
}
