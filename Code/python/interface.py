import os
import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter import Toplevel
from PIL import Image, ImageTk
import cv2

# Variables globales pour stocker les coordonnées, la référence du rectangle, et le chemin de l'image
x_start, y_start = None, None
x_end, y_end = None, None
rect_id = None
photo = None  # Image Tkinter
img_original = None  # Image originale
chemin_image = None  # Chemin de l'image sélectionnée
a, b = None, None  # Paramètres a et b

# Fonction pour charger l'image
def charger_image():
    global photo, img_original, rect_id, chemin_image  # Utiliser les variables globales

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
            img_original = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Sauvegarder l'image originale pour référence
            
            # Convertir en Image PIL
            img_pil = Image.fromarray(img_original)
            
            # Obtenir les dimensions originales
            largeur, hauteur = img_pil.size
            
            # Ajuster le canvas aux dimensions de l'image
            canvas.config(width=largeur, height=hauteur)
            
            # Convertir en image Tkinter
            photo = ImageTk.PhotoImage(img_pil)
            
            # Afficher l'image dans le canvas
            canvas.image = photo  # Conserver une référence à l'image
            canvas.create_image(0, 0, anchor="nw", image=photo)
        except Exception as e:
            print(f"Erreur lors du chargement de l'image : {e}")

def ouvrir_parametres_obscuration(type_filtre):
    global a, b  # Utiliser les variables globales pour a et b
    
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
    btn_pixelisation = tk.Button(panel_obscuration, text="Pixelisation", command=lambda: ouvrir_parametres_obscuration("../bin/floupixel"))
    btn_pixelisation.pack(pady=5)

    btn_distorsion = tk.Button(panel_obscuration, text="Distorsion", command=lambda: ouvrir_parametres_obscuration("../bin/distorsion"))
    btn_distorsion.pack(pady=5)

    btn_gaussien = tk.Button(panel_obscuration, text="Flou Gaussien", command=lambda: ouvrir_parametres_obscuration("../bin/flougaussien"))
    btn_gaussien.pack(pady=5)

    btn_mouvement = tk.Button(panel_obscuration, text="Flou de Mouvement", command=lambda: ouvrir_parametres_obscuration("../bin/floumouvement"))
    btn_mouvement.pack(pady=5)

# Créer un dossier "temp/" s'il n'existe pas
def creer_dossier_temp():
    if not os.path.exists("./temp"):
        os.makedirs("./temp")

# Appliquer un filtre en appelant un programme C++ et en sauvegardant l'image modifiée
def appliquer_obscuration(type_filtre):
    global photo, img_original, x_start, y_start, x_end, y_end, chemin_image, a, b , result

    # Créer le dossier temp s'il n'existe pas
    creer_dossier_temp()

    # Définir le chemin de l'image de sortie
    chemin_sortie = "./temp/image_modifiee.png"
    chemin_sortie2 = "./temp/image_modifiee2.png"

    # Vérifier s'il y a une sélection
    if x_start is None or x_end is None or y_start is None or y_end is None:
        # Si aucune sélection, appliquer le filtre sur toute l'image
        if type_filtre == "distorsion":
            result = subprocess.run([f"{type_filtre}", chemin_image, chemin_sortie, chemin_sortie2, str(a), str(b)])
        else:
            result = subprocess.run([f"{type_filtre}", chemin_image, chemin_sortie, str(a), str(b)])
     
    else:
        # Si une zone est sélectionnée, appliquer le filtre uniquement sur cette zone
        if type_filtre == "distorsion":
            result = subprocess.run([f"{type_filtre}zone", chemin_image, chemin_sortie, chemin_sortie2, str(a), str(b),
                            str(x_start), str(y_start), str(x_end), str(y_end)])
        else :
            result = subprocess.run([f"{type_filtre}zone", chemin_image, chemin_sortie, str(a), str(b),
                            str(x_start), str(y_start), str(x_end), str(y_end)])
    if result.returncode != 0:
        print(f"Erreur lors de l'exécution : {result.stderr}")
    else:
        print(f"Sortie : {result.stdout}")

    # Charger l'image modifiée
    img_modifiee = Image.open(chemin_sortie)
    photo = ImageTk.PhotoImage(img_modifiee)

    # Afficher l'image modifiée sur le canvas
    canvas.create_image(0, 0, anchor="nw", image=photo)
    canvas.image = photo

# Fonction pour gérer la sélection de la zone
def on_button_press(event):
    global x_start, y_start, rect_id
    x_start, y_start = event.x, event.y
    print(f"Point de départ : ({x_start}, {y_start})")
    
    # Si un rectangle est déjà en place, le supprimer
    if rect_id:
        canvas.delete(rect_id)
    
    # Créer un rectangle temporaire à partir du point de départ
    rect_id = canvas.create_rectangle(x_start, y_start, x_start, y_start, outline="red", width=2)

# Fonction appelée lorsque le bouton gauche est relâché pour enregistrer le point de fin et afficher le rectangle
def on_mouse_drag(event):
    global x_start, y_start, x_end, y_end, rect_id
    x_end, y_end = event.x, event.y
    
    # Mettre à jour les dimensions du rectangle pendant le drag
    canvas.coords(rect_id, x_start, y_start, x_end, y_end)

# Fonction appelée lorsque le bouton gauche est relâché pour enregistrer le point de fin
def on_button_release(event):
    global x_end, y_end
    x_end, y_end = event.x, event.y
    print(f"Point de fin : ({x_end}, {y_end})")
    print(f"Zone sélectionnée : x_start={x_start}, x_end={x_end}, y_start={y_start}, y_end={y_end}")

# Créer la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Afficheur d'image avec sélection de zone")

# Ajouter un bouton pour charger une image
btn_charger = tk.Button(fenetre, text="Charger une image", command=charger_image)
btn_charger.pack(pady=10)

# Ajouter un bouton pour ouvrir le panel d'obscuration
btn_obscuration = tk.Button(fenetre, text="Obscuration", command=ouvrir_panel_obscuration)
btn_obscuration.pack(pady=10)

# Ajouter un canvas pour afficher l'image
canvas = tk.Canvas(fenetre, bg="white")
canvas.pack()

# Associer les événements de la souris au canvas
canvas.bind("<ButtonPress-1>", on_button_press)  # Début du clic gauche
canvas.bind("<B1-Motion>", on_mouse_drag)  # Déplacement de la souris pendant le clic gauche
canvas.bind("<ButtonRelease-1>", on_button_release)  # Fin du clic gauche

# Lancer l'application
fenetre.mainloop()


