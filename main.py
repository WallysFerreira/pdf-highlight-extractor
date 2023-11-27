from pypdf import PdfReader

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
                    print(coordenadas_cantos_retangulo)
                else:
                    canto_esquerdo_superior = [coordenadas_cantos_retangulo[0], coordenadas_cantos_retangulo[1]]
                    canto_direito_inferior = [coordenadas_cantos_retangulo[6], coordenadas_cantos_retangulo[7]]

                    anotacao_encontrada.coordenadas.append([canto_esquerdo_superior, canto_direito_inferior])
                    anotacao_encontrada.pagina = numero_pagina + 1

                anotacoes_encontradas.append(anotacao_encontrada)
