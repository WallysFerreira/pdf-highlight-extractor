import tempfile
import concurrent.futures 
import os
from pypdf import PdfReader, PdfWriter 
from main import extrair

with tempfile.TemporaryDirectory() as path:
    leitor = PdfReader("teste2.pdf")
    caminhos_saida = [f"{path}/primeira_parte", f"{path}/segunda_parte", f"{path}/terceira_parte", f"{path}/quarta_parte"]
    escritor1 = PdfWriter()
    escritor2 = PdfWriter()
    escritor3 = PdfWriter()
    escritor4 = PdfWriter()

    if len(leitor.pages) >= 4:
        divisao = len(leitor.pages) // 4
        escritor1.append(leitor, pages=(0, divisao))
        escritor1.write(f'{caminhos_saida[0]}.pdf')

        escritor2.append(leitor, pages=(divisao, divisao * 2))
        escritor2.write(f'{caminhos_saida[1]}.pdf')

        escritor3.append(leitor, pages=(divisao * 2, divisao * 3))
        escritor3.write(f'{caminhos_saida[2]}.pdf')

        escritor4.append(leitor, pages=(divisao * 3, divisao * 4))
        escritor4.write(f'{caminhos_saida[3]}.pdf')
    else:
        escritor1.append(leitor)
        escritor1.write(f'{caminhos_saida[0]}.pdf')

    if len(leitor.pages) >= 4:
        with concurrent.futures.ThreadPoolExecutor(4) as executor:
            futures = [executor.submit(extrair, f'{caminhos_saida[i]}.pdf', f'{caminhos_saida[i]}.txt') for i in range(4)]
            concurrent.futures.wait(futures)
    else:
        extrair(f'{caminhos_saida[0]}.pdf', f'{caminhos_saida[0]}.txt')
    
    with open(f'anotacoes.txt', 'w') as arquivo_saida:
        for arquivo in caminhos_saida:
            if os.path.isfile(f'{arquivo}.txt'):
                with open(f'{arquivo}.txt', "r") as fragmento:
                    arquivo_saida.write(fragmento.read())

