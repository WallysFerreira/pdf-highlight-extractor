from pypdf import PdfReader, PdfWriter
from pdf2image import convert_from_path
from PIL import Image
import tempfile
import pytesseract

leitor = PdfReader("teste.PDF")

class AnotacaoEncontrada:
    def __init__(self) -> None:
        self.texto = ""
        self.pagina = 0
        self.numero = 0
        self.coordenadas = []
        pass

anotacoes_encontradas = []
numero_anotacoes_encontradas = 1
path = tempfile.TemporaryDirectory()

for numero_pagina, pagina in enumerate(leitor.pages):
    # Algumas páginas não tem anotação nenhuma
    if "/Annots" in pagina:
        anotacoes = pagina["/Annots"]

        for anotacao in anotacoes:
            anotacao = anotacao.get_object()

            # A anotação só é valida se tiver o campo QuadPoints
            if "/QuadPoints" in anotacao:
                escritor = PdfWriter()
                coordenadas_cantos_retangulo = anotacao["/QuadPoints"]
                anotacao_encontrada = AnotacaoEncontrada()
                anotacao_encontrada.pagina = numero_pagina + 1
                anotacao_encontrada.numero = numero_anotacoes_encontradas
                numero_anotacoes_encontradas += 1

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

                for coord in anotacao_encontrada.coordenadas:
                    pagina.mediabox.upper_left = (coord[0][0], coord[0][1])
                    pagina.mediabox.lower_right = (coord[1][0], coord[1][1])

                    escritor.add_page(pagina)
                    escritor.write(f'{path.name}/{anotacao_encontrada.pagina}_{anotacao_encontrada.numero}.pdf')

ultima_pagina_mostrada = 0
for anotacao in anotacoes_encontradas:
    imagens = convert_from_path(f'{path.name}/{anotacao.pagina}_{anotacao.numero}.pdf', output_folder=path.name)

    for imagem in imagens:
        texto_extraido = pytesseract.image_to_string(imagem, lang="por").strip()

        anotacao.texto += texto_extraido
        anotacao.texto += " "

    if ultima_pagina_mostrada != anotacao.pagina:
        print()
        print("Pagina:", anotacao.pagina)
        ultima_pagina_mostrada = anotacao.pagina

    print("Anotação:", anotacao.numero)
    print(anotacao.texto)