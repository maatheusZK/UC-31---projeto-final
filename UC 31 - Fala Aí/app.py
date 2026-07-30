from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "falaai2026"

ARQUIVO_JSON = "dados.json"


# ==========================
# FUNÇÕES AUXILIARES
# ==========================

def carregar_dados():
    """Lê o arquivo JSON."""
    if not os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
            json.dump([], arquivo)

    with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_dados(dados):
    """Salva alterações no JSON."""
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)


def gerar_id(dados):
    if not dados:
        return 1
    return max(item["id"] for item in dados) + 1


# ==========================
# ROTAS
# ==========================

@app.route("/")
def index():
    mensagens = carregar_dados()

    total = len(mensagens)
    sugestoes = sum(1 for m in mensagens if m["tipo"] == "Sugestão")
    reclamacoes = sum(1 for m in mensagens if m["tipo"] == "Reclamação")
    elogios = sum(1 for m in mensagens if m["tipo"] == "Elogio")

    recentes = sorted(
        mensagens,
        key=lambda x: x["id"],
        reverse=True
    )[:5]

    return render_template(
        "index.html",
        total=total,
        sugestoes=sugestoes,
        reclamacoes=reclamacoes,
        elogios=elogios,
        recentes=recentes
    )


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():

    if request.method == "POST":

        mensagens = carregar_dados()

        nova = {
            "id": gerar_id(mensagens),
            "tipo": request.form["tipo"],
            "titulo": request.form["titulo"],
            "descricao": request.form["descricao"],
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        }

        mensagens.append(nova)
        salvar_dados(mensagens)

        flash("Manifestação enviada com sucesso!", "success")

        return redirect(url_for("index"))

    return render_template("cadastrar.html")


@app.route("/mensagens")
def mensagens():

    lista = carregar_dados()

    pesquisa = request.args.get("pesquisa", "").lower()

    if pesquisa:
        lista = [
            m for m in lista
            if pesquisa in m["titulo"].lower()
            or pesquisa in m["descricao"].lower()
            or pesquisa in m["tipo"].lower()
        ]

    lista = sorted(lista, key=lambda x: x["id"], reverse=True)

    return render_template("mensagens.html", mensagens=lista)


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    mensagens = carregar_dados()

    mensagem = next((m for m in mensagens if m["id"] == id), None)

    if mensagem is None:
        flash("Mensagem não encontrada.", "danger")
        return redirect(url_for("mensagens"))

    if request.method == "POST":

        mensagem["tipo"] = request.form["tipo"]
        mensagem["titulo"] = request.form["titulo"]
        mensagem["descricao"] = request.form["descricao"]

        salvar_dados(mensagens)

        flash("Mensagem atualizada com sucesso!", "success")

        return redirect(url_for("mensagens"))

    return render_template("editar.html", mensagem=mensagem)


@app.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):

    mensagens = carregar_dados()

    nova_lista = [m for m in mensagens if m["id"] != id]

    salvar_dados(nova_lista)

    flash("Mensagem excluída com sucesso!", "warning")

    return redirect(url_for("mensagens"))


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


# ==========================
# ERRO 404
# ==========================

@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template("404.html"), 404


# ==========================
# EXECUÇÃO
# ==========================

if __name__ == "__main__":
    app.run(debug=True)