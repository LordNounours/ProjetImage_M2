import os
import subprocess

def apply_distorsion(input_folder, output_folder, amplitude, frequence, x_start, y_start, x_end, y_end):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    files = os.listdir(input_folder)
    files.sort()

    for file in files:
        extension = os.path.splitext(file)[1].lower()
        if extension in ['.png', '.jpg', '.jpeg', '.bmp']:
            input_path = os.path.join(input_folder, file)
            output_path = os.path.join(output_folder, file)
            command = [
                'Code/bin/distorsionzone',  # exe
                input_path,
                output_path,
                str(amplitude),
                str(frequence),
                str(x_start),
                str(y_start),
                str(x_end),
                str(y_end)
            ]
            try:
                subprocess.run(command, check=True)
                print(f"Processed {file}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to process {file}: {e}")

if __name__ == "__main__":
    input_folder = 'archive/'  
    output_folder = 'distorsion3/'
    amplitude = 10   
    frequence = 5
    x_start = 5  
    y_start = 30
    x_end = 120  
    y_end = 110  

    apply_distorsion(input_folder, output_folder, amplitude, frequence, x_start, y_start, x_end, y_end)
    print("Traitement terminé.")
