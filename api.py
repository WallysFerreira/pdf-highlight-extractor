from flask import Flask, send_file, request
from main import extrair

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = './uploads'

@app.route('/extract')
def extract():
    try:
        file = request.files['entrada.PDF']
        file.save(f'{app.config["UPLOAD_FOLDER"]}/{file.filename}')
        extrair()
        return send_file('./saida.txt', download_name="marcacoes.txt")
    except Exception as e:
        return str(e)