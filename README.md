# pdf-highlight-extractor
Extract highlights from PDF files.

## O que vai precisar ser feito
- Pegar as coordenadas das marcações no PDF (PyPDF)
- Transformar as páginas em imagem (pdf2image)
- Cortar usando as coordenadas das marcações (pillow)
- Pegar o texto da imagem cortada (pytesseract)
- Mostrar para o usuario (terminal ou html)

## Pontos para tomar cuidado
- Marcações de mais de uma linha. São a mesma marcação mas vão ter dois retangulos. Como vai manter o contexto de ser uma única marcação mas juntar o texto de duas imagens cortadas diferentes?
- A apresentação pro usuário
- Vai salvar uma imagem para cada página. Tem como usar a imagem sem salvar? Parece que tem com tempfile
