import os
import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter import Toplevel
from PIL import Image, ImageTk
from tkinter import messagebox
import tensorflow as tf  # Nécessaire pour charger le modèle .keras
import numpy as np

import cv2

# Variables globales pour stocker les coordonnées, la référence du rectangle, et le chemin de l'image
x_start, y_start = None, None
x_end, y_end = None, None
rect_id = None
photo = None  # Image Tkinter
img_original = None  # Image originale
chemin_image = None  # Chemin de l'image sélectionnée
a, b = None, None  # Paramètres a et b
modele = None


def faire_prediction():
    global modele, chemin_image

    if modele is None:
        print("Aucun modèle chargé. Veuillez charger un modèle avant de faire une prédiction.")
        messagebox.showwarning("Attention", "Aucun modèle chargé. Veuillez charger un modèle avant de faire une prédiction.")
        return
    
    if chemin_image is None:
        print("Aucune image disponible pour la prédiction.")
        messagebox.showwarning("Attention", "Aucune image disponible pour la prédiction.")
        return
    
    try:
        # Charger l'image modifiée avec OpenCV
        img = cv2.imread(chemin_image)
        if img is None:
            print("Erreur : impossible de charger l'image modifiée pour la prédiction.")
            return
        
        # Prétraitement de l'image pour le modèle
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convertir en RGB
        img = cv2.resize(img, (128, 128))  # Redimensionner pour correspondre à l'entrée du modèle (ajustez selon votre modèle)
        img = img / 255.0  # Normaliser les pixels entre 0 et 1
        img = img[np.newaxis, ...]  # Ajouter une dimension pour correspondre au batch
        
        # Faire une prédiction avec le modèle
        predictions = modele.predict(img)
        print(f"Prédictions : {predictions}")
        predicted_class = np.argmax(predictions, axis=1)
        predicted_probability = predictions[0][predicted_class[0]]

        # Afficher le message en fonction de la classe prédite
        if predicted_class[0] == 0:
            messagebox.showinfo("Prédictions", f"Classe prédite : Clair {predicted_probability*100:.2f}%")
        elif predicted_class[0] == 1:
            messagebox.showinfo("Prédictions", f"Classe prédite : Distorsion {predicted_probability*100:.2f}%")
        elif predicted_class[0] == 2:
            messagebox.showinfo("Prédictions", f"Classe prédite : Flou Gaussien {predicted_probability*100:.2f}%")
        elif predicted_class[0] == 3:
            messagebox.showinfo("Prédictions", f"Classe prédite : Flou Mouvement {predicted_probability*100:.2f}%")
        elif predicted_class[0] == 4:
            messagebox.showinfo("Prédictions", f"Classe prédite : Pixelisation {predicted_probability*100:.2f}%")
        else:
            messagebox.showinfo("Prédictions", f"Classe prédite : FGSM {predicted_probability*100:.2f}%")
    
        print(f"Classe prédite : {predicted_class[0]} avec une probabilité de {predicted_probability*100:.2f}%")

        
        print(f"Classe prédite : {predicted_class[0]}") 
        
    except Exception as e:
        print(f"Erreur lors de la prédiction : {e}")
        messagebox.showerror("Erreur", f"Erreur lors de la prédiction : {e}")



def charger_modele():
    global modele  # Utiliser une variable globale pour stocker le modèle
    try:
        # Ouvrir une boîte de dialogue pour sélectionner un fichier .keras
        chemin_modele = filedialog.askopenfilename(
            title="Choisir un modèle",
            initialdir="../modeles",  # Répertoire de départ
            filetypes=[("Fichiers Keras", "*.keras"), ("Tous les fichiers", "*.*")]
        )
        
        if chemin_modele:  # Si un fichier est sélectionné
            # Charger le modèle avec TensorFlow/Keras
            modele = tf.keras.models.load_model(chemin_modele)
            print(f"Modèle chargé avec succès depuis : {chemin_modele}")
            messagebox.showinfo("Succès", f"Modèle chargé avec succès depuis : {chemin_modele}")
        else:
            print("Aucun fichier sélectionné.")
    except Exception as e:
        print(f"Erreur lors du chargement du modèle : {e}")
        messagebox.showerror("Erreur", f"Erreur lors du chargement du modèle : {e}")




def charger_image():
    global photo, img_original, rect_id, chemin_image  # Utiliser les variables globales
    chemin_image = None
    # Ouvrir une boîte de dialogue pour sélectionner un fichier image
    chemin_fichier = filedialog.askopenfilename(
        title="Choisir une image",
        initialdir="../Images",
        filetypes=[
            ("Images PNG", "*.png"),
            ("Images JPEG", "*.jpg;*.jpeg"),
            ("Images BMP", "*.bmp"),
            ("Images GIF", "*.gif"),
            ("Tous les fichiers", "*.*")
        ]
    )
    if chemin_fichier:  # Si un fichier est sélectionné
        chemin_image = chemin_fichier  # Enregistrer le chemin de l'image sélectionnée
        try:
            # Charger l'image avec OpenCV
            img = cv2.imread(chemin_fichier)
            if img is None:
                print("Erreur : impossible de charger l'image.")
                return

            img_original = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Sauvegarder l'image originale pour référence
            
            # Obtenir les dimensions originales
            hauteur_originale, largeur_originale = img_original.shape[:2]

            # Vérifier si l'image dépasse les dimensions de 800x800
            max_dim = 800
            if largeur_originale > max_dim or hauteur_originale > max_dim:
                # Calculer l'échelle de réduction
                ratio = min(max_dim / largeur_originale, max_dim / hauteur_originale)
                nouvelle_largeur = int(largeur_originale * ratio)
                nouvelle_hauteur = int(hauteur_originale * ratio)
                
                # Redimensionner l'image
                img_original = cv2.resize(img_original, (nouvelle_largeur, nouvelle_hauteur), interpolation=cv2.INTER_AREA)
            
            # Convertir en Image PIL
            img_pil = Image.fromarray(img_original)
            
            # Ajuster le canvas aux dimensions de l'image
            largeur, hauteur = img_pil.size
            canvas.config(width=largeur, height=hauteur)
            
            # Convertir en image Tkinter
            photo = ImageTk.PhotoImage(img_pil)
            
            # Afficher l'image dans le canvas
            canvas.image = photo  # Conserver une référence à l'image
            canvas.create_image(0, 0, anchor="nw", image=photo)
        except Exception as e:
            print(f"Erreur lors du chargement de l'image : {e}")
    else:
        messagebox.showerror("Erreur", "Aucune image sélectionnée.")
        
def ouvrir_parametres_obscuration(type_filtre  , panel_obscuration):
    panel_obscuration.destroy()

    # Créer une nouvelle fenêtre pour saisir les paramètres a et b
    fenetre_parametres = Toplevel(fenetre)
    fenetre_parametres.title(f"Paramètres pour {type_filtre}")
    
    # Label pour "a"
    label_a = tk.Label(fenetre_parametres, text="Valeur de a:")
    label_a.pack(pady=5)
    
    # Champ de saisie pour "a"
    entry_a = tk.Entry(fenetre_parametres)
    entry_a.pack(pady=5)
    
    # Label pour "b"
    label_b = tk.Label(fenetre_parametres, text="Valeur de b:")
    label_b.pack(pady=5)
    
    # Champ de saisie pour "b"
    entry_b = tk.Entry(fenetre_parametres)
    entry_b.pack(pady=5)
    
    # Fonction pour appliquer l'obscuration avec les valeurs saisies
    def appliquer_avec_parametres():
        global a, b
        try:
            # Récupérer les valeurs de a et b
            a = int(entry_a.get())
            b = int(entry_b.get())
            # Appliquer l'obscuration
            appliquer_obscuration(type_filtre)
            fenetre_parametres.destroy()  # Fermer la fenêtre de saisie
        except ValueError:
            print("Les valeurs de a et b doivent être des nombres.")
    
    # Bouton pour appliquer avec les paramètres
    btn_appliquer = tk.Button(fenetre_parametres, text="Appliquer", command=appliquer_avec_parametres)
    btn_appliquer.pack(pady=10)
    

    # S'assurer que la fenêtre de paramètres prend suffisamment de place pour tout afficher
    fenetre_parametres.geometry("300x200")  # Taille minimale de la fenêtre


# Ouvrir la fenêtre d'options d'obscuration
def ouvrir_panel_obscuration():
    panel_obscuration = Toplevel(fenetre)
    panel_obscuration.title("Obscuration de l'image")

    # Ajouter les boutons pour chaque effet
    btn_pixelisation = tk.Button(panel_obscuration, text="Pixelisation", command=lambda: ouvrir_parametres_obscuration("floupixel" , panel_obscuration))
    btn_pixelisation.pack(pady=5)

    btn_distorsion = tk.Button(panel_obscuration, text="Distorsion", command=lambda: ouvrir_parametres_obscuration("distorsion" , panel_obscuration))
    btn_distorsion.pack(pady=5)

    btn_gaussien = tk.Button(panel_obscuration, text="Flou Gaussien", command=lambda: ouvrir_parametres_obscuration("flougaussien", panel_obscuration))
    btn_gaussien.pack(pady=5)

    btn_mouvement = tk.Button(panel_obscuration, text="Flou de Mouvement", command=lambda: ouvrir_parametres_obscuration("floumouvement", panel_obscuration))
    btn_mouvement.pack(pady=5)

    btn_fgsm = tk.Button(panel_obscuration, text="FGSM", command=lambda: ouvrir_parametres_obscuration("fgsm" , panel_obscuration))
    btn_fgsm.pack(pady=5)

# Créer un dossier "temp/" s'il n'existe pas
def creer_dossier_temp():
    if not os.path.exists("./temp"):
        os.makedirs("./temp")

# Appliquer un filtre en appelant un programme C++ et en sauvegardant l'image modifiée
def appliquer_obscuration(type_filtre):
    global photo, img_original, x_start, y_start, x_end, y_end, chemin_image, a, b , result

    # Créer le dossier temp s'il n'existe pas
    temp = creer_dossier_temp()

    # Définir le chemin de l'image de sortie
    chemin_sortie = "./temp/image_modifiee.png"
    chemin_sortie2 = "./temp/image_modifiee2.png"
        
        
    print(f"chemin_image : {chemin_image}, chemin_sortie :{chemin_sortie}\n, a: {a}, b: {b}, x_start: {x_start}, y_start: {y_start}, x_end: {x_end}, y_end: {y_end}\n")
    print(f"appilcation du fitre\n")
    
    # Vérifier s'il y a une sélection
    if None in [x_start, x_end, y_start, y_end]:
        # Si aucune sélection, appliquer le filtre sur toute l'image
        if type_filtre == "distorsion":
            result = subprocess.run([f"../bin/{type_filtre}", chemin_image, chemin_sortie, chemin_sortie2, str(a), str(b)])
        if type_filtre == "fgsm":
            result = subprocess.run([f"../bin/{type_filtre}", chemin_image, chemin_sortie, str(a)])
        else:
            result = subprocess.run([f"../bin/{type_filtre}", chemin_image, chemin_sortie, str(a), str(b)])
    else:
        # Si une zone est sélectionnée, appliquer le filtre uniquement sur cette zone
        if type_filtre == "distorsion":
            result = subprocess.run([f"../bin/{type_filtre}zone", chemin_image, chemin_sortie, chemin_sortie2, str(a), str(b),str(x_start), str(y_start), str(x_end), str(y_end)])
        if type_filtre == "fgsm":
            result = subprocess.run([f"../bin/{type_filtre}zone", chemin_image, chemin_sortie, str(a),str(x_start), str(y_start), str(x_end), str(y_end)])
        else:
            result = subprocess.run([f"../bin/{type_filtre}zone", chemin_image, chemin_sortie, str(a), str(b),str(x_start), str(y_start), str(x_end), str(y_end)])

    # Vérification de l'exécution du subprocess
    if result.returncode != 0:
        print(f"Erreur lors de l'exécution : {result.stderr}")
    else:
        print(f"Sortie : {result.stdout}")

    # Charger l'image modifiée
    img_modifiee = Image.open(chemin_sortie)
    photo = ImageTk.PhotoImage(img_modifiee)
    
    chemin_image = chemin_sortie
    # Afficher l'image modifiée sur le canvas
    canvas.create_image(0, 0, anchor="nw", image=photo)
    canvas.image = photo
    
    
    if modele:
        faire_prediction()
    else:
        messagebox.showwarning("Attention", "Aucune modèle de prediction est chargé.")
    
    a = None
    b = None
    x_start = None
    y_start = None
    x_end = None
    y_end = None
    print(f"chemin_image : {chemin_image}, chemin_sortie :{chemin_sortie}\n, a: {a}, b: {b}, x_start: {x_start}, y_start: {y_start}, x_end: {x_end}, y_end: {y_end}")

    

# Fonction pour gérer la sélection de la zone
def on_button_press(event):
    global x_start, y_start, rect_id
    x_start, y_start = event.x, event.y
    print(f"Point de départ : ({x_start}, {y_start})")
    
    # Si un rectangle est déjà en place, le supprimer
    if rect_id:
        canvas.delete(rect_id)
    
    # Créer un rectangle transparent pour la sélection
    rect_id = canvas.create_rectangle(x_start, y_start, x_start, y_start, outline="red", width=2)

def on_mouse_drag(event):
    global x_end, y_end, rect_id
    x_end, y_end = event.x, event.y
    print(f"Point de fin : ({x_end}, {y_end})")
    
    # Mettre à jour la position du rectangle pendant le déplacement de la souris
    canvas.coords(rect_id, x_start, y_start, x_end, y_end)

def on_button_release(event):
    global x_end, y_end
    x_end, y_end = event.x, event.y
    print(f"Sélection terminée : ({x_start}, {y_start}) à ({x_end}, {y_end})")

# Créer la fenêtre principale Tkinter
fenetre = tk.Tk()
fenetre.title("Éditeur d'image")

# Créer un canvas pour afficher l'image
canvas = tk.Canvas(fenetre)
canvas.pack(fill="both", expand=True)

# Créer un bouton pour charger l'image
btn_charger = tk.Button(fenetre, text="Charger une image", command=charger_image)
btn_charger.pack(pady=10)

# Créer un bouton pour ouvrir le panel de filtres
btn_obscuration = tk.Button(fenetre, text="Appliquer un filtre", command=ouvrir_panel_obscuration)
btn_obscuration.pack(pady=10)


# Ajouter un bouton pour charger un modèle
btn_charger_modele = tk.Button(fenetre, text="Charger un modèle keras", command=charger_modele)
btn_charger_modele.pack(pady=10)

# Lier les événements de la souris pour la sélection de la zone
canvas.bind("<ButtonPress-1>", on_button_press)
canvas.bind("<B1-Motion>", on_mouse_drag)
canvas.bind("<ButtonRelease-1>", on_button_release)

# Lancer la fenêtre Tkinter
fenetre.mainloop()
