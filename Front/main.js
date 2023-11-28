window.onload = () => {
    const inputFile = document.querySelector('#file');

    document.getElementById('img-area').addEventListener('click', function () {
        document.getElementById('file').click();
    });

    inputFile.addEventListener('change', async function () {
        const fd = new FormData()
        fd.append('entrada.PDF', inputFile.files[0])

        let res = await fetch('https://pdf-highlight-extractor-api.onrender.com/extract', {
            method: 'POST',
            body: fd
        })

        let blob_saida = await res.blob()
        let blobUrl = URL.createObjectURL(blob_saida)
    
        var botao_download = document.createElement("a")
        botao_download.href = blobUrl
        botao_download.download = "saida.txt"
        botao_download.click()
    })
}
