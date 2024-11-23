import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import os

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        tf.config.experimental.set_memory_growth(gpus[0], True)
    except RuntimeError as e:
        print(e)

train_base_dir = '../Data/Data/'
dir = os.path.join(train_base_dir, 'distorsion1')

def verifier_et_lister_contenu(repertoire):
    if os.path.exists(repertoire):
        print(f"Le dossier '{repertoire}' contient les fichiers suivants :")
        for filename in os.listdir(repertoire):
            print(filename)
    else:
        print(f"Le dossier '{repertoire}' n'existe pas. Vérifiez le chemin.")

verifier_et_lister_contenu(dir)


image_size = (128, 128)
batch_size = 64  


def charger_et_preparer_image(img_path):
    img = tf.io.read_file(img_path)
    img = tf.image.decode_jpeg(img, channels=3)  
    img = tf.image.resize(img, image_size)  
    img = img / 255.0  
    return img


def charger_images_et_labels(repertoire, label):
    images_paths = [os.path.join(repertoire, filename) for filename in os.listdir(repertoire)]
    labels = [label] * len(images_paths)
    return images_paths, labels

def create_tf_dataset(image_paths, labels, batch_size, shuffle_data=True):
    dataset = tf.data.Dataset.from_tensor_slices((image_paths, labels))
    dataset = dataset.map(lambda img_path, label: (charger_et_preparer_image(img_path), label), num_parallel_calls=tf.data.AUTOTUNE)
    
    if shuffle_data:
        dataset = dataset.shuffle(buffer_size=1000)
    
    dataset = dataset.batch(batch_size).prefetch(tf.data.AUTOTUNE)
    return dataset


model = tf.keras.models.load_model('../modeles/model_dist1.keras')

def create_adversarial_pattern(model, input_image, input_label):
    input_image = tf.convert_to_tensor(input_image, dtype=tf.float32)
    input_label = tf.convert_to_tensor(input_label, dtype=tf.int64)
    
    with tf.GradientTape() as tape:
        tape.watch(input_image)
        prediction = model(input_image)
        loss = tf.keras.losses.sparse_categorical_crossentropy(input_label, prediction)
    
    # Obtenir le gradient de la perte par rapport à l'image d'entrée
    gradient = tape.gradient(loss, input_image)
    
    # Obtenir le signe du gradient pour créer la perturbation
    signed_grad = tf.sign(gradient)
    return signed_grad

def generate_adversarial_image(model, image, label, epsilon=0.1):
    perturbations = create_adversarial_pattern(model, [image], [label])
    adversarial_image = image + epsilon * perturbations[0]
    adversarial_image = tf.clip_by_value(adversarial_image, 0.0, 1.0)
    return adversarial_image.numpy()


# Charger les images et les labels
images_paths, labels = charger_images_et_labels(dir, label=0)  # Remplacez '0' par l'étiquette correcte si nécessaire

# Sélectionner une image d'entraînement et son label pour la démonstration
index = 0
original_image = charger_et_preparer_image(images_paths[index])
original_label = labels[index]


# Générer l'image adversariale
epsilon = 0.1  # Vous pouvez ajuster cette valeur
adversarial_image = generate_adversarial_image(model, original_image, original_label, epsilon)

# Afficher les images originale et adversariale
def display_images(image1, image2, title1="Original", title2="Adversarial"):
    plt.figure(figsize=(6,3))
    
    plt.subplot(1, 2, 1)
    plt.title(title1)
    plt.imshow(image1)
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.title(title2)
    plt.imshow(image2)
    plt.axis('off')
    
    plt.show()

display_images(original_image, adversarial_image)


# Prédiction sur l'image originale
original_prediction = model.predict(tf.expand_dims(original_image, axis=0))
original_class = tf.argmax(original_prediction[0]).numpy()

# Prédiction sur l'image adversariale
adversarial_prediction = model.predict(tf.expand_dims(adversarial_image, axis=0))
adversarial_class = tf.argmax(adversarial_prediction[0]).numpy()

print(f"Classe originale prédite: {original_class}")
print(f"Classe adversariale prédite: {adversarial_class}")
