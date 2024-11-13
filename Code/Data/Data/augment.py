import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img, save_img


input_dir = '../Data/Data/train/distorsion2/distorsion/'  
output_dir = '../Data/Data/train/distorsion2/distorsion/' 


if not os.path.exists(output_dir):
    os.makedirs(output_dir)

datagen = ImageDataGenerator(
    rotation_range=40,  
    width_shift_range=0.2,  
    height_shift_range=0.2,  
    shear_range=0.2,  
    zoom_range=0.2,  
    horizontal_flip=True,  
    fill_mode='nearest'  
)

num_augmented_images = 10

for filename in os.listdir(input_dir):
    img_path = os.path.join(input_dir, filename)
    
    if filename.endswith('.jpg') or filename.endswith('.png'):  
        img = load_img(img_path)
        x = img_to_array(img)
        x = x.reshape((1,) + x.shape)  

        i = 0
        for batch in datagen.flow(x, batch_size=1, save_to_dir=output_dir, save_prefix='aug', save_format='jpg'):
            i += 1
            if i >= num_augmented_images:  
                break  

print("Augmentation des images terminée.")

