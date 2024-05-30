

function goToInsertion() {
  window.location.href = "insertion.html";
}

function goToExtraction(){
  window.location.href = "extraction.html";
}

// Fonction pour diriger vers la page précédente
function goBack() {
  window.history.back();
}

// Event listener pour le bouton "Add" pour ajouter le watermark à l'image
document.getElementById("addBtn").addEventListener("click", function () {
  addWatermarkToImage();
});

// Event listener pour le bouton "Back" pour revenir en arrière
document.getElementById("backBtn").addEventListener("click", function () {
  goBack();
});

// Event listener pour le bouton "Sauvegarder" pour sauvegarder le watermark
document.getElementById("saveBtn").addEventListener("click", function () {
  saveWatermark();
});

// Masquer les éléments de texte initialement
document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("filename").classList.add("hidden");
  document.getElementById("output-path").classList.add("hidden");
});






function addWatermarkToImage() {
   // Récupérer les données du formulaire
  var formData = new FormData(document.getElementById("patientForm"));

 // Récupérer l'image sélectionnée
  var imageFile = document.getElementById("img").files[0];
  formData.append("image", imageFile);

  // Envoyer les données du formulaire et de l'image à l'API
  fetch('http://127.0.0.1:5000/process_image', {
      method: 'POST',
      body: formData
  })
  .then(response => response.json())
  .then(data => {
      if (data.status === 'success') {
         // Afficher un message de succès
          alert('Image sauvegardée avec succès dans le dossier processed_images.');
      } else {
         // Afficher un message d'erreur
          alert('Erreur: ' + data.message);
      }
  })
  .catch(error => {
      console.error('Error:', error);
  });
}

const extractBtn = document.getElementById('extractWatermarkBtn');

extractBtn.onclick = function() {
    
    extraireWatermark();
};

// Exécuter le script Python extraire.py
function extraireWatermark() {
  exec('python extraire.py', (error, stdout, stderr) => {
      if (error) {
          console.error(`Erreur lors de l'extraction du watermark: ${error.message}`);
          return;
      }
      if (stderr) {
          console.error(`Erreur lors de l'extraction du watermark: ${stderr}`);
          return;
      }
      console.log(`Le watermark a été extrait avec succès: ${stdout}`);
  });
}

// Apercu de l'image selectionnee 
function showimage() {
  const input = document.getElementById("img");
  if (input.files && input.files[0]) {
    const reader = new FileReader();
    reader.onload = function (e) {
      const imagePreview = document.getElementById("preview");
      imagePreview.innerHTML = '<img src="' + e.target.result + '" alt="Selected Image">';
      imagePreview.classList.remove("hidden");
    };
    reader.readAsDataURL(input.files[0]);
  }
}


