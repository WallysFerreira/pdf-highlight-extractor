from pypdf import PdfReader, PdfWriter
import tempfile
import tabula

def converter_coordenadas_para_tabula(coords, altura_pagina):
    padding = 2

    x1 = coords[0] - padding
    y1 = altura_pagina - coords[1]
    x2 = coords[2] + padding
    y2 = altura_pagina - coords[3]

    return [y1, x1, y2, x2]

class AnotacaoEncontrada:
    def __init__(self) -> None:
        self.texto = ""
        self.pagina = 0
        self.numero = 0
        self.coordenadas = []

def extrair(caminho_arquivo_entrada, caminho_arquivo_saida):
    anotacoes_encontradas = []
    paginas_pdf = []
    print("Entrada:", caminho_arquivo_entrada)
    print("Saida:", caminho_arquivo_saida)
    leitor = PdfReader(caminho_arquivo_entrada)
    altura_pagina = leitor.pages[0].mediabox.height
    arquivo_saida = open(caminho_arquivo_saida, 'w+')
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

    print("Terminou de procurar anotações")

    for anotacao in anotacoes_encontradas:
        for coord in anotacao.coordenadas:
            area = converter_coordenadas_para_tabula([coord[0][0], coord[0][1], coord[1][0], coord[1][1]], altura_pagina)

            linhas_extraidas = tabula.read_pdf(caminho_arquivo_entrada, area=area, pages=anotacao.pagina)

            for linha in linhas_extraidas:
                texto_extraido = linha.columns[0]

                anotacao.texto += texto_extraido
                anotacao.texto += " "

    print("Terminou de extrair o texto")

    for anotacao_encontrada in anotacoes_encontradas:
        if ultima_pagina_mostrada != anotacao_encontrada.pagina:
            #print()
            arquivo_saida.write("\n")
            #print("Pagina", anotacao_encontrada.pagina)
            arquivo_saida.write(f"Pagina {anotacao_encontrada.pagina}\n" )
            ultima_pagina_mostrada = anotacao_encontrada.pagina

        #print("Anotação", anotacao_encontrada.numero)
        arquivo_saida.write(f"Anotação {anotacao_encontrada.numero}\n")
        #print(anotacao_encontrada.texto)
        arquivo_saida.write(f"{anotacao_encontrada.texto}\n")

    print("Terminou de escrever anotações")
