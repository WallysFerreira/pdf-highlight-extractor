import multiprocessing
from flask import Flask, send_file, request
from flask_cors import CORS
from divisor import dividir
from main import extrair

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = './uploads'
CORS(app)

@app.route('/extract', methods=['POST'])
def extract():
    num_cores = multiprocessing.cpu_count()
    print("Qntd cores:", num_cores)

    try:
        file = request.files['entrada.PDF']
        caminho_arquivo_entrada = f'{app.config["UPLOAD_FOLDER"]}/{file.filename}'
        file.save(caminho_arquivo_entrada)
        
        if num_cores > 4:
            dividir(caminho_arquivo_entrada)
        else:
            extrair(caminho_arquivo_entrada, './anotacoes.txt')

        return send_file('./anotacoes.txt', download_name="marcacoes.txt")
    except Exception as e:
        return str(e)