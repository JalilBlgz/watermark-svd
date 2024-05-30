import numpy as np
import os
import cv2
from flask import Flask, request, jsonify


#Repertoire ou les images seront enregistrees
IMAGES_DIR = "processed_images/"
#Facteur de Ponderation
SVD_WATERMARKING_CONDITION = 0.01

#Lire une image en gris et la retourner en un tableau
def read_image(path, color_mode="GRAY"):
    if color_mode == "GRAY":
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    else:
        raise ValueError("Invalid color mode. Use 'GRAY' or 'RGB'.")
    return img

#Decomposition en valeurs singulieres des images
def svd(image):
    U, S, V = np.linalg.svd(image, full_matrices=True)
    return U, S, V

#Inserer la marque dans les valeurs singulieres
def embed_watermark_svd(S_cover, watermark):
    watermark_values = np.frombuffer(watermark.encode(), dtype=np.uint8)
    watermark_values = np.tile(watermark_values, len(S_cover) // len(watermark_values) + 1)[:len(S_cover)]
    S_wimgR = S_cover + (watermark_values * SVD_WATERMARKING_CONDITION)
    return S_wimgR


#Inserer la marque dans l'image
def SVD_GRAY_EMBED(image, watermark):
    U_cover, S_cover, V_cover = svd(image)
    embedded_S_watermark = embed_watermark_svd(S_cover, watermark)
    watermarked_image = np.dot(U_cover, np.dot(np.diag(embedded_S_watermark), V_cover))
    return watermarked_image


#Creation de l'application Flask
app = Flask(__name__)

#Route pour traiter l'image
@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        #Recuperer les donnees du formulaire
        image_file = request.files['image']
        nom = request.form['nom']
        prenom = request.form['prenom']
        age = request.form['age']
        sexe = request.form['sexe']
        clinique = request.form['clinique']
        maladie = request.form['maladie']
        medecin_traitant = request.form['medecinTraitant']

       #Verifier l'existance du repertoire
        if not os.path.exists(IMAGES_DIR):
            os.makedirs(IMAGES_DIR)

        #Enregistrer l'image dans le dossier temporaire    
        image_path = os.path.join(IMAGES_DIR, 'Image Initiale.jpg')
        image_file.save(image_path)

        #Lire l'image
        coverImage = read_image(image_path, "GRAY")

        #Generer le watermark a partir des donnees du formulaire
        watermark = f"Nom: {nom}, Prénom: {prenom}, Age: {age}, Sexe: {sexe}, Clinique: {clinique}, Maladie: {maladie}, Médecin Traitant: {medecin_traitant}"

        #Integrer le watermark dans l'image
        watermarked_image = SVD_GRAY_EMBED(coverImage, watermark)

        #Sauvegarder l'image tatouee
        out_path = os.path.join(IMAGES_DIR, 'Image Traitee.jpg')
        cv2.imwrite(out_path, watermarked_image)

        #Verifier que le fichier image est correctement sauvegarde
        if not os.path.isfile(out_path):
            return jsonify({'status': 'error', 'message': 'Erreur lors de la sauvegarde de l\'image watermarkée.'})

        #Message de reussite
        return jsonify({'status': 'success', 'message': 'Watermark incorporé avec succès.', 'image_path': out_path})

    #Cas d'erreur
    except Exception as e:
        return jsonify({'status': 'error', 'message': f"Une erreur s'est produite : {e}"})

#Execution du serveur flask
if __name__ == "__main__":
    app.run(debug=True)
    