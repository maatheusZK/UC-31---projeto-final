from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

import json
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = "falaai2026"

ARQUIVO_JSON = "dados.json"


# ============================================================
# FUNÇÕES
# ============================================================

def carregar_mensagens():
    if not os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
            json.dump([], arquivo, indent=4, ensure_ascii=False)

    with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
        try:
            return json.load(arquivo)
        except json.JSONDecodeError:
            return []


def salvar_mensagens(mensagens):
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(
            mensagens,
            arquivo,
            indent=4,
            ensure_ascii=False
        )


def gerar_id():
    mensagens = carregar_mensagens()

    if not mensagens:
        return 1

    return max(m["id"] for m in mensagens) + 1


def login_obrigatorio(func):

    @wraps(func)
    def verificar(*args, **kwargs):

        if not session.get("admin"):
            flash("Faça login para acessar esta página.", "warning")
            return redirect(url_for("login"))

        return func(*args, **kwargs)

    return verificar


# ============================================================
# PÁGINA INICIAL
# ============================================================

@app.route("/")
def index():

    mensagens = carregar_mensagens()

    total = len(mensagens)

    elogios = len(
        [m for m in mensagens if m["tipo"] == "Elogio"]
    )

    sugestoes = len(
        [m for m in mensagens if m["tipo"] == "Sugestão"]
    )

    reclamacoes = len(
        [m for m in mensagens if m["tipo"] == "Reclamação"]
    )

    ultimas = sorted(
        mensagens,
        key=lambda x: x["id"],
        reverse=True
    )[:5]

    return render_template(
        "index.html",
        total=total,
        elogios=elogios,
        sugestoes=sugestoes,
        reclamacoes=reclamacoes,
        ultimas=ultimas
    )


# ============================================================
# SOBRE
# ============================================================

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


# ============================================================
# CADASTRAR
# ============================================================

@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():

    if request.method == "POST":

        tipo = request.form["tipo"]
        titulo = request.form["titulo"].strip()
        descricao = request.form["descricao"].strip()

        if titulo == "" or descricao == "":
            flash("Preencha todos os campos.", "danger")
            return redirect(url_for("cadastrar"))

        mensagens = carregar_mensagens()

        nova = {

            "id": gerar_id(),

            "tipo": tipo,

            "titulo": titulo,

            "descricao": descricao,

            "data": datetime.now().strftime("%d/%m/%Y"),

            "hora": datetime.now().strftime("%H:%M")

        }

        mensagens.append(nova)

        salvar_mensagens(mensagens)

        flash("Mensagem enviada com sucesso!", "success")

        return redirect(url_for("index"))

    return render_template("cadastrar.html")


# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        senha = request.form["senha"]

        if usuario == "admin" and senha == "1234":

            session["admin"] = True

            flash("Login realizado com sucesso.", "success")

            return redirect(url_for("dashboard"))

        flash("Usuário ou senha inválidos.", "danger")

    return render_template("login.html")


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
@login_obrigatorio
def logout():

    session.clear()

    flash("Logout realizado.", "info")

    return redirect(url_for("index"))


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
@login_obrigatorio
def dashboard():

    mensagens = carregar_mensagens()

    total = len(mensagens)

    elogios = len(
        [m for m in mensagens if m["tipo"] == "Elogio"]
    )

    sugestoes = len(
        [m for m in mensagens if m["tipo"] == "Sugestão"]
    )

    reclamacoes = len(
        [m for m in mensagens if m["tipo"] == "Reclamação"]
    )

    return render_template(

        "dashboard.html",

        total=total,

        elogios=elogios,

        sugestoes=sugestoes,

        reclamacoes=reclamacoes

    )


# ============================================================
# LISTA DE MENSAGENS
# ============================================================

@app.route("/mensagens")
@login_obrigatorio
def mensagens():

    lista = carregar_mensagens()

    pesquisa = request.args.get("pesquisa", "").strip()

    categoria = request.args.get("categoria", "").strip()

    if pesquisa:

        lista = [

            mensagem

            for mensagem in lista

            if pesquisa.lower() in mensagem["titulo"].lower()

            or pesquisa.lower() in mensagem["descricao"].lower()

        ]

    if categoria:

        lista = [

            mensagem

            for mensagem in lista

            if mensagem["tipo"] == categoria

        ]

    lista = sorted(

        lista,

        key=lambda x: x["id"],

        reverse=True

    )

    return render_template(

        "mensagens.html",

        mensagens=lista,

        pesquisa=pesquisa,

        categoria=categoria

    )

# ============================================================
# EDITAR MENSAGEM
# ============================================================

@app.route("/editar/<int:id>", methods=["GET", "POST"])
@login_obrigatorio
def editar(id):

    mensagens = carregar_mensagens()

    mensagem = next(
        (m for m in mensagens if m["id"] == id),
        None
    )

    if mensagem is None:
        flash("Mensagem não encontrada.", "danger")
        return redirect(url_for("mensagens"))

    if request.method == "POST":

        mensagem["tipo"] = request.form["tipo"]
        mensagem["titulo"] = request.form["titulo"].strip()
        mensagem["descricao"] = request.form["descricao"].strip()

        salvar_mensagens(mensagens)

        flash("Mensagem atualizada com sucesso.", "success")

        return redirect(url_for("mensagens"))

    return render_template(
        "editar.html",
        mensagem=mensagem
    )


# ============================================================
# EXCLUIR MENSAGEM
# ============================================================

@app.route("/excluir/<int:id>", methods=["POST"])
@login_obrigatorio
def excluir(id):

    mensagens = carregar_mensagens()

    nova_lista = [
        mensagem
        for mensagem in mensagens
        if mensagem["id"] != id
    ]

    if len(nova_lista) == len(mensagens):
        flash("Mensagem não encontrada.", "danger")
    else:
        salvar_mensagens(nova_lista)
        flash("Mensagem excluída com sucesso.", "success")

    return redirect(url_for("mensagens"))


# ============================================================
# ERRO 404
# ============================================================

@app.errorhandler(404)
def erro404(erro):
    return render_template("404.html"), 404


# ============================================================
# ERRO 500
# ============================================================

@app.errorhandler(500)
def erro500(erro):
    return render_template("500.html"), 500


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    app.run(
        debug=True
    )