import os

dossier_images = "pixel3/"

fichiers = os.listdir(dossier_images)

fichiers.sort()

for i, fichier in enumerate(fichiers):
    extension = os.path.splitext(fichier)[1]
    nouveau_nom = f"pixel3{i+1}{extension}"
    ancien_chemin = os.path.join(dossier_images, fichier)
    nouveau_chemin = os.path.join(dossier_images, nouveau_nom)
    os.rename(ancien_chemin, nouveau_chemin)

print("Renommage terminé.")
