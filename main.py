from pypdf import PdfReader
from pdf2image import convert_from_path
import tempfile

leitor = PdfReader("teste.PDF")

class AnotacaoEncontrada:
    pagina = 0
    texto = ""
    coordenadas = []

    def __init__(self) -> None:
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
                anotacao_encontrada = AnotacaoEncontrada()

                coordenadas_cantos_retangulo = anotacao["/QuadPoints"]

                if len(coordenadas_cantos_retangulo) > 8:
                    anotacao_encontrada.pagina = numero_pagina + 1

                    for i in range(len(coordenadas_cantos_retangulo) // 8):
                        coordenadas = []
                        coordenadas.append(coordenadas_cantos_retangulo[i * 8])
                        coordenadas.append(coordenadas_cantos_retangulo[(i * 8) + 1])
                        coordenadas.append(coordenadas_cantos_retangulo[(i * 8) + 6])
                        coordenadas.append(coordenadas_cantos_retangulo[(i * 8) + 7])

                        anotacao_encontrada.coordenadas.append(coordenadas)
                else:
                    canto_esquerdo_superior = [coordenadas_cantos_retangulo[0], coordenadas_cantos_retangulo[1]]
                    canto_direito_inferior = [coordenadas_cantos_retangulo[6], coordenadas_cantos_retangulo[7]]

                    anotacao_encontrada.coordenadas.append([canto_esquerdo_superior, canto_direito_inferior])
                    anotacao_encontrada.pagina = numero_pagina + 1

                anotacoes_encontradas.append(anotacao_encontrada)

with tempfile.TemporaryDirectory() as path:
    imagens = convert_from_path('teste.PDF', output_folder=path)

    for numero_pagina, imagem in enumerate(imagens):
        imagem.save(f"{path}/{numero_pagina}.jpg")
