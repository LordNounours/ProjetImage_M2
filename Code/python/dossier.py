import os
import shutil
import uuid

# Chemin vers le dossier principal
base_path = 'archive'

# Fonction pour générer un nom de fichier unique
def generate_unique_filename(base_path, filename):
    name, ext = os.path.splitext(filename)
    unique_name = f"{name}_{uuid.uuid4().hex}{ext}"
    return os.path.join(base_path, unique_name)

# Parcourir tous les sous-dossiers
for root, dirs, files in os.walk(base_path, topdown=False):
    print(f"Traitement du dossier: {root}")
    for name in files:
        file_path = os.path.join(root, name)
        new_location = generate_unique_filename(base_path, name)
        
        # Déplacer et renommer le fichier vers le dossier principal
        print(f"Déplacement du fichier {file_path} vers {new_location}")
        shutil.move(file_path, new_location)
    
    for name in dirs:
        dir_path = os.path.join(root, name)
        
        # Vérifier si le sous-dossier est vide avant de le supprimer
        if not os.listdir(dir_path):
            print(f"Suppression du dossier vide: {dir_path}")
            os.rmdir(dir_path)
        else:
            print(f"Le dossier {dir_path} n'est pas vide et ne sera pas supprimé.")

print("Toutes les images ont été déplacées et les sous-dossiers ont été supprimés.")

