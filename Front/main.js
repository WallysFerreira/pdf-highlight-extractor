const inputFile = document.querySelector("#file");
const imgArea = document.querySelector(".img-area");
const pictureImageTxt = "Carregue o Arquivo";

document.querySelector('.icon').addEventListener('click', function() {
    inputFile.click();
});

inputFile.addEventListener("change", function (e) {
  const inputTarget = e.target;
  const file = inputTarget.files[0];

  if (file) {
    const reader = new FileReader();

    reader.addEventListener("load", function (e) {
      const readerTarget = e.target;

      const object = document.createElement('object');
      object.data = readerTarget.result;
      object.width = "500";
      object.height = "500";
      object.type = "application/pdf";

      imgArea.innerHTML = "";
      imgArea.appendChild(object);
    });

    reader.readAsDataURL(file);
  } else {
    imgArea.innerHTML = pictureImageTxt;
  }
});
