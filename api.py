from flask import Flask, send_file, request
from flask_cors import CORS
from main import extrair

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = './uploads'
CORS(app)

@app.route('/extract', methods=['POST'])
def extract():
    try:
        file = request.files['entrada.PDF']
        caminho_arquivo_entrada = f'{app.config["UPLOAD_FOLDER"]}/{file.filename}'
        file.save(caminho_arquivo_entrada)
        extrair(caminho_arquivo_entrada)
        return send_file('./saida.txt', download_name="marcacoes.txt")
    except Exception as e:
        return str(e)