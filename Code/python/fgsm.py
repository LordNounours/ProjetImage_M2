import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import os

# Configuration du GPU
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        tf.config.experimental.set_memory_growth(gpus[0], True)
    except RuntimeError as e:
        print(e)

# Chemins des répertoires
train_base_dir = '../Data/Data/'
dir = os.path.join(train_base_dir, 'mvt1')
output_dir = os.path.join(train_base_dir, 'fgsmmvt1')

# Vérifier et lister le contenu d'un répertoire
def verifier_et_lister_contenu(repertoire):
    if os.path.exists(repertoire):
        print(f"Le dossier '{repertoire}' contient les fichiers suivants :")
        for filename in os.listdir(repertoire):
            print(filename)
    else:
        print(f"Le dossier '{repertoire}' n'existe pas. Vérifiez le chemin.")

verifier_et_lister_contenu(dir)

# Créer le répertoire de sortie s'il n'existe pas
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

image_size = (128, 128)
batch_size = 64  

# Charger et préparer une image
def charger_et_preparer_image(img_path):
    img = tf.io.read_file(img_path)
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.resize(img, image_size)
    img = img / 255.0
    return img

# Charger les chemins des images et les labels
def charger_images_et_labels(repertoire, label):
    images_paths = [os.path.join(repertoire, filename) for filename in os.listdir(repertoire)]
    labels = [label] * len(images_paths)
    return images_paths, labels

# Créer un dataset TensorFlow
def create_tf_dataset(image_paths, labels, batch_size, shuffle_data=True):
    dataset = tf.data.Dataset.from_tensor_slices((image_paths, labels))
    dataset = dataset.map(lambda img_path, label: (charger_et_preparer_image(img_path), label), num_parallel_calls=tf.data.AUTOTUNE)
    if shuffle_data:
        dataset = dataset.shuffle(buffer_size=1000)
    dataset = dataset.batch(batch_size).prefetch(tf.data.AUTOTUNE)
    return dataset

# Chemin complet vers le fichier modèle
model_path = os.path.join('../modeles', 'model_mvt1.keras')

# Vérifiez si le fichier modèle existe
if os.path.isfile(model_path):
    print(f"Le fichier modèle '{model_path}' existe.")
else:
    print(f"Le fichier modèle '{model_path}' est introuvable. Vérifiez le chemin ou le nom du fichier.")

# Charger le modèle Keras
model = tf.keras.models.load_model(model_path)

# Créer le pattern adversarial
def create_adversarial_pattern(model, input_image, input_label):
    input_image = tf.convert_to_tensor(input_image, dtype=tf.float32)
    input_label = tf.convert_to_tensor(input_label, dtype=tf.int64)
    
    with tf.GradientTape() as tape:
        tape.watch(input_image)
        prediction = model(input_image)
        loss = tf.keras.losses.sparse_categorical_crossentropy(input_label, prediction)
    
    gradient = tape.gradient(loss, input_image)
    signed_grad = tf.sign(gradient)
    return signed_grad

# Générer une image adversariale
def generate_adversarial_image(model, image, label, epsilon=0.1):
    perturbations = create_adversarial_pattern(model, [image], [label])
    adversarial_image = image + epsilon * perturbations[0]
    adversarial_image = tf.clip_by_value(adversarial_image, 0.0, 1.0)
    return adversarial_image.numpy()

# Charger les images et les labels
images_paths, labels = charger_images_et_labels(dir, label=1)  # Remplacez '0' par l'étiquette correcte si nécessaire

# Itérer sur toutes les images, générer et sauvegarder les images adversariales
for index, img_path in enumerate(images_paths):
    original_image = charger_et_preparer_image(img_path)
    original_label = labels[index]
    
    adversarial_image = generate_adversarial_image(model, original_image, original_label, epsilon=0.1)
    
    # Convertir l'image en uint8 pour la sauvegarde
    adversarial_image_uint8 = (adversarial_image * 255).astype(np.uint8)
    
    # Sauvegarder l'image adversariale
    output_path = os.path.join(output_dir, os.path.basename(img_path))
    tf.keras.preprocessing.image.save_img(output_path, adversarial_image_uint8)
    print(f"Image adversariale sauvegardée : {output_path}")

print("Toutes les images adversariales ont été générées et sauvegardées.")
