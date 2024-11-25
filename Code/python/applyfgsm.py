import tensorflow as tf
from tensorflow import keras
import numpy as np
import os

# Configuration GPU
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        tf.config.experimental.set_memory_growth(gpus[0], True)
    except RuntimeError as e:
        print(e)

# Chemins des fichiers
model_path = '../modeles/model_dist1.keras'
image_path = '../Data/Data/distorsion1/image_test.jpg'  # Remplacez par le chemin de l'image
output_path = '../Data/Data/fgsmdist1_/image_adversariale.jpg'

# Vérification des chemins
if not os.path.isfile(model_path):
    raise FileNotFoundError(f"Le fichier modèle '{model_path}' est introuvable.")

if not os.path.isfile(image_path):
    raise FileNotFoundError(f"L'image '{image_path}' est introuvable.")

output_dir = os.path.dirname(output_path)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Charger le modèle
model = tf.keras.models.load_model(model_path)
print(f"Modèle chargé depuis : {model_path}")

# Préparation de l'image
image_size = (128, 128)

def charger_et_preparer_image(img_path):
    img = tf.io.read_file(img_path)
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.resize(img, image_size)
    img = img / 255.0
    return img

# Création du motif adversarial
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

def generate_adversarial_image(model, image, label, epsilon=0.1):
    perturbations = create_adversarial_pattern(model, [image], [label])
    adversarial_image = image + epsilon * perturbations[0]
    adversarial_image = tf.clip_by_value(adversarial_image, 0.0, 1.0)
    return adversarial_image.numpy()

# Charger l'image
original_image = charger_et_preparer_image(image_path)
original_label = 1  # Exemple : 1 = obscur, 0 = clair (à ajuster selon le cas)

# Générer l'image adversariale
adversarial_image = generate_adversarial_image(model, original_image, original_label, epsilon=0.1)

# Sauvegarder l'image adversariale
adversarial_image_uint8 = (adversarial_image * 255).astype(np.uint8)
tf.keras.preprocessing.image.save_img(output_path, adversarial_image_uint8)
print(f"Image adversariale sauvegardée : {output_path}")
