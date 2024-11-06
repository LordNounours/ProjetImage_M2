import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

train_dir = '../Data/Data/train/distorsion2/'

train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    train_dir,
    validation_split=0.2, 
    subset="training",
    seed=123,
    image_size=(224, 224),
    color_mode='rgb',  
    batch_size=32
)

validation_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    train_dir,
    validation_split=0.2,  
    subset="validation",
    seed=123,
    image_size=(224, 224),
    color_mode='rgb',  
    batch_size=32
)

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        tf.config.experimental.set_memory_growth(gpus[0], True)
    except RuntimeError as e:
        print(e)

normalization_layer = tf.keras.layers.Rescaling(1./255)
normalized_train_ds = train_dataset.map(lambda x, y: (normalization_layer(x), y))
normalized_val_ds = validation_dataset.map(lambda x, y: (normalization_layer(x), y))

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

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(normalized_train_ds, validation_data=normalized_val_ds, epochs=10, verbose=True)

score = model.evaluate(normalized_val_ds, verbose=0)
print(f"Test loss: {score[0]:4.4f}")
print(f"Test accuracy: {score[1]:4.4f}")

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

model.save('my_model.keras')

