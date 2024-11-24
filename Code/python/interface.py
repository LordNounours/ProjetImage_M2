import os
import subprocess
import tkinter as tk
from tkinter import filedialog, Toplevel, messagebox
from PIL import Image, ImageTk
import tensorflow as tf
import numpy as np
import cv2

# Variables globales
x_start, y_start = None, None
x_end, y_end = None, None
rect_id = None
photo = None
img_original = None
chemin_image = None
a, b = None, None
modele = None

# Fonction pour créer un dossier temporaire
def creer_dossier_temp():
    if not os.path.exists("./temp"):
        os.makedirs("./temp")
    return "./temp"


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
        if(predicted_class.size==2) :
            if predicted_class[0] == 0:
                messagebox.showinfo("Prédictions", f"Classe prédite : Clair {predicted_probability*100:.2f}%")
            elif predicted_class[0] == 1:
                messagebox.showinfo("Prédictions", f"Classe prédite : Obscurcie {predicted_probability*100:.2f}%")
        else :
            # Créer un dictionnaire pour les noms des classes
            nom_classes = ["Clair", "Distorsion", "Flou Gaussien", "Flou Mouvement", "Pixelisation"]
            
            # Construire le message avec toutes les probabilités
            message = "Probabilités des classes :\n"
            for i, prob in enumerate(predictions[0]):
                message += f"{nom_classes[i]} : {prob * 100:.2f}%\n"

            # Afficher le message
            messagebox.showinfo("Prédictions", message)
        
        print(f"Classe prédite : {predicted_class[0]} avec une probabilité de {predicted_probability*100:.2f}%")

        
        print(f"Classe prédite : {predicted_class[0]}") 
        
    except Exception as e:
        print(f"Erreur lors de la prédiction : {e}")
        messagebox.showerror("Erreur", f"Erreur lors de la prédiction : {e}")



# Charger un modèle Keras
def charger_modele():
    global modele
    try:
        chemin_modele = filedialog.askopenfilename(
            title="Choisir un modèle",
            initialdir="../modeles",
            filetypes=[("Fichiers Keras", "*.keras"), ("Tous les fichiers", "*.*")]
        )
        if chemin_modele:
            modele = tf.keras.models.load_model(chemin_modele)
            messagebox.showinfo("Succès", f"Modèle chargé avec succès depuis : {chemin_modele}")
        else:
            messagebox.showwarning("Attention", "Aucun fichier sélectionné.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors du chargement du modèle : {e}")

# Charger une image
def charger_image():
    global photo, img_original, chemin_image
    chemin_temp = creer_dossier_temp()
    chemin_image = None
    chemin_fichier = filedialog.askopenfilename(
        title="Choisir une image",
        initialdir="../Images",
        filetypes=[
            ("Images PNG", "*.png"),
            ("Images JPEG", "*.jpg;*.jpeg"),
            ("Images BMP", "*.bmp"),
            ("Images GIF", "*.gif"),
            ("Tous les fichiers", "*.*")]
    )
    if chemin_fichier:
        try:
            img = cv2.imread(chemin_fichier)
            if img is None:
                raise ValueError("Erreur lors du chargement de l'image.")
            
            img_original = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            hauteur, largeur = img_original.shape[:2]
            max_dim = 800
            if largeur > max_dim or hauteur > max_dim:
                ratio = min(max_dim / largeur, max_dim / hauteur)
                img_original = cv2.resize(img_original, (int(largeur * ratio), int(hauteur * ratio)))
            
            chemin_image = os.path.join(chemin_temp, "Img_original.png")
            cv2.imwrite(chemin_image, cv2.cvtColor(img_original, cv2.COLOR_RGB2BGR))

            # Convertir pour affichage dans Tkinter
            img_pil = Image.fromarray(img_original)
            photo = ImageTk.PhotoImage(img_pil)
            canvas.config(width=img_pil.width, height=img_pil.height)
            canvas.create_image(0, 0, anchor="nw", image=photo)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement de l'image : {e}")
    else:
        messagebox.showwarning("Attention", "Aucune image sélectionnée.")

# Gestion de la sélection de zone
def on_button_press(event):
    global x_start, y_start, rect_id
    x_start, y_start = event.x, event.y
    if rect_id:
        canvas.delete(rect_id)
    rect_id = canvas.create_rectangle(x_start, y_start, x_start, y_start, outline="red", width=2)

def on_mouse_drag(event):
    global x_end, y_end, rect_id
    x_end, y_end = event.x, event.y
    canvas.coords(rect_id, x_start, y_start, x_end, y_end)

def on_button_release(event):
    global x_end, y_end
    x_end, y_end = event.x, event.y

# Calculer le PSNR
def calculer_psnr(image1, image2):
    mse = np.mean((image1 - image2) ** 2)
    if mse == 0:
        return 100
    return 20 * np.log10(255.0 / np.sqrt(mse))

# Appliquer un filtre
def appliquer_obscuration(type_filtre):
    global chemin_image, img_original, photo, x_start, y_start, x_end, y_end, a, b

    chemin_temp = creer_dossier_temp()
    chemin_sortie = os.path.join(chemin_temp, "image_modifiee.png")
    chemin_sortie2 = os.path.join(chemin_temp, "image_modifiee2.png")

    if None in [x_start, x_end, y_start, y_end]:
        args = [f"../bin/{type_filtre}", chemin_image, chemin_sortie, str(a), str(b)]

    else:
        args = [f"../bin/{type_filtre}zone", chemin_image, chemin_sortie, str(a), str(b), str(x_start), str(y_start), str(x_end), str(y_end)]

    result = subprocess.run(args)
    if result.returncode != 0:
        messagebox.showerror("Erreur", f"Erreur lors de l'application du filtre {type_filtre}")
        return

    img_modifiee = cv2.imread(chemin_sortie)
    psnr = calculer_psnr(cv2.cvtColor(img_original, cv2.COLOR_RGB2BGR), img_modifiee)
    messagebox.showinfo("PSNR", f"PSNR : {psnr:.2f} dB")
    chemin_image = chemin_sortie

    img_modifiee = cv2.cvtColor(img_modifiee, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_modifiee)
    photo = ImageTk.PhotoImage(img_pil)
    canvas.create_image(0, 0, anchor="nw", image=photo)
    
    x_start, y_start = None, None
    x_end, y_end = None, None   
    rect_id = None
    a, b = None, None
    
    

# Fenêtre des paramètres
def ouvrir_parametres(type_filtre):
    fenetre_param = Toplevel(fenetre)
    fenetre_param.title(f"Paramètres : {type_filtre}")

    tk.Label(fenetre_param, text="Valeur de a:").pack(pady=5)
    entry_a = tk.Entry(fenetre_param)
    entry_a.pack(pady=5)

    tk.Label(fenetre_param, text="Valeur de b:").pack(pady=5)
    entry_b = tk.Entry(fenetre_param)
    entry_b.pack(pady=5)

    def appliquer():
        global a, b
        try:
            a, b = int(entry_a.get()), int(entry_b.get())
            fenetre_param.destroy()
            appliquer_obscuration(type_filtre)
            faire_prediction()
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides pour a et b.")

    tk.Button(fenetre_param, text="Appliquer", command=appliquer).pack(pady=10)
    fenetre_param.geometry("250x150")

# Fenêtre des filtres
def ouvrir_panel_obscuration():
    panel = Toplevel(fenetre)
    panel.title("Filtres d'obscuration")

    filtres = [("Pixelisation", "floupixel"), ("Distorsion", "distorsion"),
               ("Flou Gaussien", "flougaussien"), ("Flou Mouvement", "floumouvement")]
    for nom, filtre in filtres:
        tk.Button(panel, text=nom, command=lambda f=filtre: ouvrir_parametres(f)).pack(pady=5)
    panel.geometry("200x200")

# Interface principale
fenetre = tk.Tk()
fenetre.title("Éditeur d'image")

canvas = tk.Canvas(fenetre)
canvas.pack(fill="both", expand=True)

tk.Button(fenetre, text="Charger une image", command=charger_image).pack(pady=10)
tk.Button(fenetre, text="Filtres d'obscuration", command=ouvrir_panel_obscuration).pack(pady=10)
tk.Button(fenetre, text="Charger un modèle", command=charger_modele).pack(pady=10)

canvas.bind("<ButtonPress-1>", on_button_press)
canvas.bind("<B1-Motion>", on_mouse_drag)
canvas.bind("<ButtonRelease-1>", on_button_release)

fenetre.mainloop()
