from concurrent.futures import ThreadPoolExecutor
from pypdf import PdfReader, PdfWriter
from pdf2image import convert_from_path
from PIL import Image
import tempfile
import threading
import pytesseract

# Variaveis globais
anotacoes_encontradas = []
paginas_pdf = []

def cortar_e_salvar(pagina, coords, caminho):
    escritor = PdfWriter()

    for coord in coords:
        pagina.mediabox.upper_left = (coord[0][0], coord[0][1])
        pagina.mediabox.lower_right = (coord[1][0], coord[1][1])

        escritor.add_page(pagina)
        escritor.write(caminho)
        
    escritor.close()

class AnotacaoEncontrada:
    def __init__(self) -> None:
        self.texto = ""
        self.pagina = 0
        self.numero = 0
        self.coordenadas = []

def extrair(caminho_arquivo_entrada):
    leitor = PdfReader(caminho_arquivo_entrada)
    arquivo_saida = open('saida.txt', 'w')
    ultima_pagina_mostrada = 0
    numero_anotacoes_encontradas = 1
    path = tempfile.TemporaryDirectory()

    for numero_pagina, pagina in enumerate(leitor.pages):
        paginas_pdf.append(pagina)

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

                    """
                    thread = threading.Thread(target=cortar_e_salvar, args=(pagina, anotacao_encontrada.coordenadas, f'{path.name}/{anotacao_encontrada.pagina}_{anotacao_encontrada.numero}.pdf'))
                    #cortar_e_salvar(pagina, anotacao_encontrada.coordenadas, f'{path.name}/{anotacao_encontrada.pagina}_{anotacao_encontrada.numero}.pdf')

                    imagens = convert_from_path(f'{path.name}/{anotacao_encontrada.pagina}_{anotacao_encontrada.numero}.pdf', output_folder=path.name)

                    for imagem in imagens:
                        texto_extraido = pytesseract.image_to_string(imagem, lang="por").strip()

                        anotacao_encontrada.texto += texto_extraido
                        anotacao_encontrada.texto += " "

                    if ultima_pagina_mostrada != anotacao_encontrada.pagina:
                        print()
                        arquivo_saida.write("\n")
                        print("Pagina", anotacao_encontrada.pagina)
                        arquivo_saida.write(f"Pagina {anotacao_encontrada.pagina}\n" )
                        ultima_pagina_mostrada = anotacao_encontrada.pagina

                    print("Anotação", anotacao_encontrada.numero)
                    arquivo_saida.write(f"Anotação {anotacao_encontrada.numero}\n")
                    print(anotacao_encontrada.texto)
                    arquivo_saida.write(f"{anotacao_encontrada.texto}\n")
"""

import time
extrair('./teste.PDF')
#print(anotacoes_encontradas)

tempo_comeco_thread = time.time()
array_anotacoes_comeco = anotacoes_encontradas[len(anotacoes_encontradas) // 2 + 1:]
array_anotacoes_final = anotacoes_encontradas[:len(anotacoes_encontradas) // 2]

for anotacao in array_anotacoes_comeco:
    threading.Thread(target=cortar_e_salvar, args=(paginas_pdf[anotacao.pagina - 1], anotacao.coordenadas, f'{anotacao.pagina}_{anotacao.numero}.pdf')).start()

for anotacao in array_anotacoes_final:
    threading.Thread(target=cortar_e_salvar, args=(paginas_pdf[anotacao.pagina - 1], anotacao.coordenadas, f'{anotacao.pagina}_{anotacao.numero}.pdf')).start()

tempo_final_thread = time.time()

tempo_comeco_sem_thread = time.time()
for anotacao in anotacoes_encontradas:
    cortar_e_salvar(paginas_pdf[anotacao.pagina - 1], anotacao.coordenadas, f'{anotacao.pagina}_{anotacao.numero}.pdf')
tempo_final_sem_thread = time.time()

print("Tempo total thread:", tempo_final_thread - tempo_comeco_thread)
print("Tempo total sem thread:", tempo_final_sem_thread - tempo_comeco_sem_thread)