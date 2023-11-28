from pypdf import PdfReader
from pdf2image import convert_from_path
from PIL import Image
import tempfile

leitor = PdfReader("teste.PDF")

class AnotacaoEncontrada:
    def __init__(self) -> None:
        self.text = ""
        self.pagina = 0
        self.coordenadas = []
        pass

anotacoes_encontradas = []

for numero_pagina, pagina in enumerate(leitor.pages):
    # Algumas páginas não tem anotação nenhuma
    if "/Annots" in pagina:
        anotacoes = pagina["/Annots"]

        for anotacao in anotacoes:
            anotacao = anotacao.get_object()

            # A anotação só é valida se tiver o campo QuadPoints
            if "/QuadPoints" in anotacao:
                coordenadas_cantos_retangulo = anotacao["/QuadPoints"]
                anotacao_encontrada = AnotacaoEncontrada()
                anotacao_encontrada.pagina = numero_pagina + 1

                if len(coordenadas_cantos_retangulo) > 8:
                    for i in range(len(coordenadas_cantos_retangulo) // 8):
                        coordenadas1 = []
                        coordenadas2 = []

                        coordenadas1.append(coordenadas_cantos_retangulo[i * 8])
                        coordenadas1.append(coordenadas_cantos_retangulo[(i * 8) + 1])
                        coordenadas2.append(coordenadas_cantos_retangulo[(i * 8) + 6])
                        coordenadas2.append(coordenadas_cantos_retangulo[(i * 8) + 7])

                        anotacao_encontrada.coordenadas.append([coordenadas1, coordenadas2])
                else:
                    canto_esquerdo_superior = [coordenadas_cantos_retangulo[0], coordenadas_cantos_retangulo[1]]
                    canto_direito_inferior = [coordenadas_cantos_retangulo[6], coordenadas_cantos_retangulo[7]]

                    anotacao_encontrada.coordenadas.append([canto_esquerdo_superior, canto_direito_inferior])

                anotacoes_encontradas.append(anotacao_encontrada)

with tempfile.TemporaryDirectory() as path:
    imagens = convert_from_path('teste.PDF', output_folder=path)

    for numero_pagina, imagem in enumerate(imagens):
        imagem.save(f"{path}/{numero_pagina}.jpg")

    for anotacao in anotacoes_encontradas:
