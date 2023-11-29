const inputFile = document.querySelector("#file");
const imgArea = document.querySelector(".img-area");
const pictureImageTxt = "Carregue o Arquivo";
const progressBar = document.querySelector("#progress-bar"); // Adduma barra de progresso no seu HTML
const progressText = document.querySelector("#progress-text"); // Add um elemento de texto para mostrar o progresso

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

    reader.addEventListener("progress", function (e) {
      if (e.lengthComputable) {
        const percentLoaded = Math.round((e.loaded / e.total) * 100);
        progressBar.value = percentLoaded; // Atualiza o valor da barra de progresso
        progressText.textContent = `Carregando ${file.name}: ${percentLoaded}%`; // Atualiza o texto do progresso
      }
    });

    reader.addEventListener("loadend", async function () {
      const fd = new FormData();
      fd.append('entrada.PDF', inputFile.files[0]); // carregamento aqui 

      let res = await fetch('https://pdf-highlight-extractor-api.onrender.com/extract', {
          method: 'POST',
          body: fd
      });

      let blob_saida = await res.blob();
      let blobUrl = URL.createObjectURL(blob_saida);

      var botao_download = document.createElement("a");
      botao_download.href = blobUrl;
      botao_download.download = "saida.txt";
      botao_download.click();
    });

    reader.readAsDataURL(file);
  } else {
    imgArea.innerHTML = pictureImageTxt;
    progressText.textContent = ""; // Limpa o texto do progresso
  }
});
