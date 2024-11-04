import os
from PIL import Image

def crop_bottom(image_path, pixels):
    """
    Recadre une certaine quantité de pixels du bas de l'image.

    Args:
    - image_path (str): Le chemin de l'image à recadrer.
    - pixels (int): Le nombre de pixels à enlever du bas de l'image.

    Returns:
    - Image: L'image recadrée.
    """
    with Image.open(image_path) as img:
        width, height = img.size
        new_height = height - pixels
        if new_height <= 0:
            raise ValueError("Le nombre de pixels à enlever est supérieur ou égal à la hauteur de l'image.")
        
        cropped_img = img.crop((0, 0, width, new_height))
        return cropped_img

def process_images(input_folder, pixels_to_crop):
    """
    Recadre les images dans le dossier spécifié et les enregistre avec un nouveau nom.

    Args:
    - input_folder (str): Le dossier contenant les images à traiter.
    - pixels_to_crop (int): Le nombre de pixels à enlever du bas de chaque image.
    """
    files = os.listdir(input_folder)
    files.sort()

    for i, file in enumerate(files):
        extension = os.path.splitext(file)[1]
        old_path = os.path.join(input_folder, file)
        
        if extension.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
            try:
                cropped_img = crop_bottom(old_path, pixels_to_crop)
                new_name = f"clearcrop{i+1}{extension}"
                new_path = os.path.join(input_folder, new_name)
                cropped_img.save(new_path)
                print(f"Processed {file} -> {new_name}")
            except Exception as e:
                print(f"Could not process {file}: {e}")

if __name__ == "__main__":
    input_folder = 'clear/'  # Changez par le chemin de votre dossier d'entrée
    pixels_to_crop = 300 # Ajustez le nombre de pixels à enlever du bas de chaque image

    process_images(input_folder, pixels_to_crop)
    print("Traitement terminé.")