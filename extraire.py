import numpy as np
import os
import cv2

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


#Extraction de la marque des valeurs singulieres
def extract_watermark_svd(S_cover, S_watermarked):
    extracted_watermark_values = (S_watermarked - S_cover) / SVD_WATERMARKING_CONDITION
    extracted_watermark_bytes = extracted_watermark_values.astype(np.uint8).tobytes()
    return extracted_watermark_bytes

#Lecture du fichier binaire
def read_binary_file(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
    return content

#Extraction de la marque à partie de l'image originale et l'image tatouee
def SVD_GRAY_EXTRACT(coverImagePath, watermarkedImagePath):
    coverImage = read_image(coverImagePath, "GRAY")
    watermarkedImage = read_image(watermarkedImagePath, "GRAY")

    U_cover, S_cover, V_cover = svd(coverImage)
    U_watermarked, S_watermarked, V_watermarked = svd(watermarkedImage)

    extracted_watermark_bytes = extract_watermark_svd(S_cover, S_watermarked)
    out_path = IMAGES_DIR + 'extracted_watermark_SVD_GRAY.bin'
    #Ouverture du fichier binaire
    with open(out_path, 'wb') as f:
        #Ecrire le contenu de la marque
        f.write(extracted_watermark_bytes)
    return out_path

if __name__ == "__main__":
    #Chemin du fichier en cours d'execution
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    #Chemin de limage origiale et l'image tatouee
    coverImagePath = os.path.join(script_dir, "images", "coverImagePath.jpg")
    watermarkedImagePath = os.path.join(script_dir, IMAGES_DIR, 'watermarked_image_SVD_GRAY.jpg')

    try:
        #Extraction de la marque
        extracted_watermark_path = SVD_GRAY_EXTRACT(coverImagePath, watermarkedImagePath)
        print("Watermark extrait avec succès.")
        print("Watermark extrait sauvegardé à:", extracted_watermark_path)
        
        #Lecture du fichier binaire qui contient la marque
        binary_content = read_binary_file(extracted_watermark_path)
        print("Contenu du fichier binaire :", binary_content)
    
    #Cas d'erreur
    except Exception as e:
        print("Une erreur s'est produite:", e)