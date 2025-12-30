from flask import Flask, render_template, request
import json
import random
import threading
import os

app = Flask(__name__)

lock = threading.Lock()

ARQUIVO = "dados.json"

NOMES_VALIDOS = [
    "Inglidh",
    "Maiury",
    "Katia",
    "Amabily",
    "Jaqueline",
    "Emanoelle",
    "Ariely"
]

def carregar_dados():
    if not os.path.exists(ARQUIVO):
        return {"sorteios": {}, "cores": []}
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_dados(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

@app.route("/", methods=["GET", "POST"])
def index():
    mensagem = None
    cor = None
    nome = None

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()

        if nome not in NOMES_VALIDOS:
            mensagem = "Voce escreveu algo errado, Digite apenas seu primeiro nome"
        else:
            with lock:
                dados = carregar_dados()

                if "sorteios" not in dados:
                    dados["sorteios"] = {}

                if "cores" not in dados:
                    dados["cores"] = []

                if nome in dados["sorteios"]:
                    mensagem = "Voce ja participou do sorteio"
                elif not dados["cores"]:
                    mensagem = "Nao ha mais cores disponiveis"
                else:
                    cor = random.choice(dados["cores"])
                    dados["cores"].remove(cor)
                    dados["sorteios"][nome] = cor
                    salvar_dados(dados)

    return render_template("index.html", mensagem=mensagem, cor=cor, nome=nome)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
