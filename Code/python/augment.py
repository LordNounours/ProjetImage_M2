import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img, save_img

# Répertoires d'entrée et de sortie
input_dir = '../Data/Data/train/distorsion2/distorsion/'  # Répertoire contenant les images à augmenter
output_dir = '../Data/Data/train/distorsion2/distorsion/' 

# Créer le répertoire de sortie s'il n'existe pas
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Définition des transformations d'augmentation
datagen = ImageDataGenerator(
    rotation_range=40,  # Rotation aléatoire entre -40 et +40 degrés
    width_shift_range=0.2,  # Décalage horizontal (20% de l'image)
    height_shift_range=0.2,  # Décalage vertical (20% de l'image)
    shear_range=0.2,  # Cisaillement de l'image
    zoom_range=0.2,  # Zoom aléatoire
    horizontal_flip=True,  # Retourner l'image horizontalement
    fill_mode='nearest'  # Mode pour remplir les pixels après transformation
)

# Nombre d'images augmentées par image originale
num_augmented_images = 10

# Processus d'augmentation
for filename in os.listdir(input_dir):
    img_path = os.path.join(input_dir, filename)
    
    if filename.endswith('.jpg') or filename.endswith('.png'):  # Assurez-vous d'avoir bien les bonnes extensions
        # Charger l'image
        img = load_img(img_path)
        x = img_to_array(img)
        x = x.reshape((1,) + x.shape)  # Redimensionner l'image pour qu'elle soit acceptée par flow()

        # Générer et sauvegarder les images augmentées directement dans le répertoire de sortie
        i = 0
        for batch in datagen.flow(x, batch_size=1, save_to_dir=output_dir, save_prefix='aug', save_format='jpg'):
            i += 1
            if i >= num_augmented_images:  # Limiter le nombre d'images augmentées par image originale
                break  # Arrêter après avoir généré num_augmented_images images

print("Augmentation des images terminée.")

