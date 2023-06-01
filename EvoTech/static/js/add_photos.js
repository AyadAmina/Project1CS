// add_photos.js
const fileInput = document.getElementById("file-input");
const imagesContainer = document.getElementById("images");

fileInput.addEventListener("change", handleFileInputChange);

function handleFileInputChange(event) {
  const files = event.target.files;
  imagesContainer.innerHTML = "";

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const reader = new FileReader();

    reader.onload = function (e) {
      const img = document.createElement("img");
      img.src = e.target.result;
      imagesContainer.appendChild(img);
    };

    reader.readAsDataURL(file);
  }
}
