#define STB_IMAGE_IMPLEMENTATION
#include "../lib/stb_image.h"

#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "../lib/stb_image_write.h"

#include <iostream>

double psnr(std::uint8_t* inputImage, std::uint8_t* outputImage, int width, int height) {
    double eqm{};
    for (int i{}; i < width * height; ++i) {
        for (int j{}; j < 3; ++j) {
            eqm += (inputImage[i * 3 + j] - outputImage[i * 3 + j]) * (inputImage[i * 3 + j] - outputImage[i * 3 + j]);
        }
    }
    eqm /= (3.0 * width * height);
    return 10.0 * std::log10(65025.0 / eqm);
}

int main(int argc, char** argv) {
    if (argc < 3) {
        std::cout << "Calcul du PSNR entre deux images\nUsage :\n  - Image 1\n  - Image 2\n";
        return 0;
    }

    int width;
    int height;
    int channelsCount;
    std::uint8_t* inputImage1{stbi_load(argv[1], &width, &height, &channelsCount, STBI_rgb)};
    std::uint8_t* inputImage2{stbi_load(argv[2], &width, &height, &channelsCount, STBI_rgb)};
    
    std::cout << "PSNR : " << psnr(inputImage1, inputImage2, width, height) << '\n';

    stbi_image_free(inputImage1);
    stbi_image_free(inputImage2);
}