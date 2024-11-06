import os
from PIL import Image

def resize_images(input_folder, output_folder, size):
    """
    Redimensionne les images dans le dossier d'entrée et sauvegarde les images redimensionnées dans le dossier de sortie.
    
    :param input_folder: Dossier contenant les images à redimensionner.
    :param output_folder: Dossier où sauvegarder les images redimensionnées.
    :param size: Tuple (largeur, hauteur) pour redimensionner les images.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif")):
            try:
                img = Image.open(os.path.join(input_folder, filename))
                img = img.resize(size, Image.ANTIALIAS)
                img.save(os.path.join(output_folder, filename))
                print(f"Image {filename} redimensionnée et sauvegardée dans {output_folder}")
            except Exception as e:
                print(f"Erreur lors du traitement de l'image {filename}: {e}")


input_folder = '../Data/Data/train/gauss3/'  
output_folder = '../Data/Data/train/gauss3/' 
size = (224, 224)  

resize_images(input_folder, output_folder, size)
