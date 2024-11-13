import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

tf.config.set_visible_devices([], 'GPU')

clear_dir = '../Data/Data/train/clear/'
train_dir = '../Data/Data/train/distorsion1/'

# Charger les images du dossier clear
clear_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    clear_dir,
    image_size=(224, 224),
    color_mode='rgb',
    batch_size=32,
    seed=123
)

# Charger les images du dossier distorsion
distorsion_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    train_dir,
    image_size=(224, 224),
    color_mode='rgb',
    batch_size=32,
    seed=123
)

# Fusionner les datasets
full_dataset = clear_dataset.concatenate(distorsion_dataset)

# Diviser le dataset complet en train et validation
train_size = int(0.8 * len(full_dataset))
train_dataset = full_dataset.take(train_size)
validation_dataset = full_dataset.skip(train_size)

# Configuration GPU
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        tf.config.experimental.set_memory_growth(gpus[0], True)
    except RuntimeError as e:
        print(e)

# Normalisation des datasets
normalization_layer = tf.keras.layers.Rescaling(1./255)
normalized_train_ds = train_dataset.map(lambda x, y: (normalization_layer(x), y))
normalized_val_ds = validation_dataset.map(lambda x, y: (normalization_layer(x), y))

# Définition du modèle
model = keras.models.Sequential([
    keras.layers.Input((224, 224, 3)),
    keras.layers.Conv2D(32, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(2, activation='softmax')  # 2 classes
])

# Compilation du modèle
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Entraînement du modèle
history = model.fit(normalized_train_ds, validation_data=normalized_val_ds, epochs=10, verbose=True)

# Évaluation du modèle
score = model.evaluate(normalized_val_ds, verbose=0)
print(f"Test loss: {score[0]:4.4f}")
print(f"Test accuracy: {score[1]:4.4f}")

# Affichage de l'accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title("Model accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

# Prédictions et génération de la matrice de confusion
predictions = model.predict(normalized_val_ds)
predictions = np.argmax(predictions, axis=1)
true_labels = np.concatenate([y for x, y in validation_dataset], axis=0)

cm = confusion_matrix(true_labels, predictions)
class_names = [str(i) for i in range(2)]
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
disp.plot(cmap=plt.cm.Blues)
plt.savefig("matrice.png")
plt.show()

# Sauvegarde du modèle
# model.save('my_model.keras')

