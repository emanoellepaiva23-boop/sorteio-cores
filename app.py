from flask import Flask, render_template, request
import json
import random

app = Flask(__name__)

USUARIAS_VALIDAS = [
    "Inglidh", "Maiury", "Katia",
    "Amabily", "Jaqueline", "Emanoelle", "Ariely"
]

CORES_INICIAIS = [
    "Azul", "Amarelo", "Vermelho",
    "Rosa", "Amarelo", "Preto", "Roxo"
]

def carregar_dados():
    try:
        with open("dados.json", "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except:
        return {"sorteios": {}, "cores": CORES_INICIAIS.copy()}

def salvar_dados(dados):
    with open("dados.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)

@app.route("/", methods=["GET", "POST"])
def index():
    dados = carregar_dados()
    mensagem = ""

    if request.method == "POST":
        nome = request.form["nome"].strip()

        if nome not in USUARIAS_VALIDAS:
            mensagem = "Voce escreveu algo errado, Digite apenas seu primeiro nome"
        elif nome in dados["sorteios"]:
            mensagem = "Voce ja participou do sorteio e nao pode participar novamente."
        elif not dados["cores"]:
            mensagem = "Todas as cores ja foram sorteadas."
        else:
            cor = random.choice(dados["cores"])
            dados["cores"].remove(cor)
            dados["sorteios"][nome] = cor
            salvar_dados(dados)
            mensagem = f"{nome}, a sua cor é a {cor}"

    return render_template("index.html", mensagem=mensagem)

app.run(host="0.0.0.0", port=10000)