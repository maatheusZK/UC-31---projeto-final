from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os
from datetime import datetime


app = Flask(__name__)

app.secret_key = "falaai2026"


ARQUIVO_JSON = "dados.json"


# ==========================
# LOGIN ADMINISTRADOR
# ==========================

ADMIN = {
    "usuario": "admin",
    "senha": "falaai2026"
}


# ==========================
# FUNÇÕES AUXILIARES
# ==========================


def carregar_dados():

    if not os.path.exists(ARQUIVO_JSON):

        with open(
            ARQUIVO_JSON,
            "w",
            encoding="utf-8"
        ) as arquivo:

            json.dump([], arquivo)


    with open(
        ARQUIVO_JSON,
        "r",
        encoding="utf-8"
    ) as arquivo:

        return json.load(arquivo)



def salvar_dados(dados):

    with open(
        ARQUIVO_JSON,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            dados,
            arquivo,
            indent=4,
            ensure_ascii=False
        )



def gerar_id(dados):

    if not dados:
        return 1

    return max(
        item["id"]
        for item in dados
    ) + 1



def administrador_logado():

    return "admin" in session



# ==========================
# LOGIN
# ==========================


@app.route("/login", methods=["GET", "POST"])
def login():


    if request.method == "POST":


        usuario = request.form["usuario"]

        senha = request.form["senha"]



        if (
            usuario == ADMIN["usuario"]
            and senha == ADMIN["senha"]
        ):


            session["admin"] = usuario


            flash(
                "Login realizado com sucesso!",
                "success"
            )


            return redirect(
                url_for("mensagens")
            )


        else:


            flash(
                "Usuário ou senha incorretos!",
                "danger"
            )



    return render_template(
        "login.html"
    )



@app.route("/logout")
def logout():


    session.pop(
        "admin",
        None
    )


    flash(
        "Logout realizado.",
        "warning"
    )


    return redirect(
        url_for("index")
    )



# ==========================
# PÁGINA INICIAL
# ==========================


@app.route("/")
def index():


    mensagens = carregar_dados()



    total = len(mensagens)


    sugestoes = sum(
        1 for m in mensagens
        if m["tipo"] == "Sugestão"
    )


    reclamacoes = sum(
        1 for m in mensagens
        if m["tipo"] == "Reclamação"
    )


    elogios = sum(
        1 for m in mensagens
        if m["tipo"] == "Elogio"
    )



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



# ==========================
# CADASTRAR COMENTÁRIO
# USUÁRIO ANÔNIMO
# ==========================


@app.route(
    "/cadastrar",
    methods=["GET", "POST"]
)
def cadastrar():


    if request.method == "POST":


        mensagens = carregar_dados()



        nova = {


            "id": gerar_id(mensagens),


            "tipo": request.form["tipo"],


            "titulo": request.form["titulo"],


            "descricao": request.form["descricao"],


            "data": datetime.now().strftime(
                "%d/%m/%Y %H:%M"
            )

        }



        mensagens.append(nova)



        salvar_dados(
            mensagens
        )



        flash(
            "Manifestação enviada com sucesso!",
            "success"
        )


        return redirect(
            url_for("index")
        )



    return render_template(
        "cadastrar.html"
    )



# ==========================
# ÁREA ADMINISTRADOR
# ==========================


@app.route("/mensagens")
def mensagens():


    if not administrador_logado():


        flash(
            "Faça login como administrador.",
            "warning"
        )


        return redirect(
            url_for("login")
        )



    lista = carregar_dados()



    pesquisa = request.args.get(
        "pesquisa",
        ""
    ).lower()



    if pesquisa:


        lista = [

            m for m in lista

            if pesquisa in m["titulo"].lower()

            or pesquisa in m["descricao"].lower()

            or pesquisa in m["tipo"].lower()

        ]



    lista = sorted(
        lista,
        key=lambda x:x["id"],
        reverse=True
    )



    return render_template(
        "mensagens.html",
        mensagens=lista
    )



@app.route(
    "/editar/<int:id>",
    methods=["GET", "POST"]
)
def editar(id):


    if not administrador_logado():


        flash(
            "Acesso negado.",
            "danger"
        )


        return redirect(
            url_for("login")
        )



    mensagens = carregar_dados()



    mensagem = next(
        (
            m for m in mensagens
            if m["id"] == id
        ),
        None
    )



    if mensagem is None:


        flash(
            "Mensagem não encontrada.",
            "danger"
        )


        return redirect(
            url_for("mensagens")
        )



    if request.method == "POST":


        mensagem["tipo"] = request.form["tipo"]

        mensagem["titulo"] = request.form["titulo"]

        mensagem["descricao"] = request.form["descricao"]



        salvar_dados(
            mensagens
        )



        flash(
            "Mensagem atualizada!",
            "success"
        )


        return redirect(
            url_for("mensagens")
        )



    return render_template(
        "editar.html",
        mensagem=mensagem
    )



@app.route(
    "/excluir/<int:id>",
    methods=["POST"]
)
def excluir(id):


    if not administrador_logado():


        flash(
            "Acesso negado.",
            "danger"
        )


        return redirect(
            url_for("login")
        )



    mensagens = carregar_dados()



    mensagens = [

        m for m in mensagens

        if m["id"] != id

    ]



    salvar_dados(
        mensagens
    )



    flash(
        "Mensagem excluída!",
        "warning"
    )



    return redirect(
        url_for("mensagens")
    )



# ==========================
# SOBRE
# ==========================


@app.route("/sobre")
def sobre():

    return render_template(
        "sobre.html"
    )



# ==========================
# ERRO 404
# ==========================


@app.errorhandler(404)
def pagina_nao_encontrada(erro):

    return render_template(
        "404.html"
    ), 404



# ==========================
# EXECUÇÃO
# ==========================


if __name__ == "__main__":

    app.run(
        debug=True
    )