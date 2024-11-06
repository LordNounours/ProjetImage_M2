import os
import shutil

# Chemin vers le dossier principal
base_path = 'archive'

# Parcourir tous les sous-dossiers
for root, dirs, files in os.walk(base_path, topdown=False):
    for name in files:
        file_path = os.path.join(root, name)
        new_location = os.path.join(base_path, name)
        
        # Déplacer le fichier vers le dossier principal
        shutil.move(file_path, new_location)
    
    for name in dirs:
        dir_path = os.path.join(root, name)
        
        # Supprimer le sous-dossier une fois qu'il est vide
        os.rmdir(dir_path)

print("Toutes les images ont été déplacées et les sous-dossiers ont été supprimés.")

