from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os
import random
from datetime import datetime


app = Flask(__name__)

app.secret_key = "falaai123"

ADMIN_USUARIO = "admin"

ADMIN_SENHA = "falaai2026"

ARQUIVO = "dados.json"

def administrador_logado():

    return "admin" in session


def carregar_dados():

    if not os.path.exists(ARQUIVO):

        with open(ARQUIVO, "w", encoding="utf-8") as arquivo:

            json.dump([], arquivo)


    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:

        return json.load(arquivo)


def salvar_dados(dados):

    with open(
        ARQUIVO,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            dados,
            arquivo,
            indent=4,
            ensure_ascii=False
        )


def gerar_codigo():

    mensagens = carregar_dados()


    while True:


        ano = datetime.now().year


        caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


        codigo_aleatorio = "".join(
            random.choice(caracteres)
            for _ in range(5)
        )


        codigo = f"FA-{ano}-{codigo_aleatorio}"



        existe = any(
            mensagem["codigo"] == codigo
            for mensagem in mensagens
        )



        if not existe:

            return codigo



def mensagem_status(status):

    status_textos = {

        "Em análise": "Sua mensagem foi recebida e está aguardando análise.",

        "Resolvido": "Sua mensagem foi analisada e uma solução foi registrada.",

        "Recusado": "Sua mensagem não pôde ser atendida no momento."

    }


    return status_textos.get(
        status,
        "Status desconhecido."
    )


@app.route("/")
def index():

    mensagens = carregar_dados()


    ultimas = mensagens[-3:]


    return render_template(
        "index.html",
        ultimas=ultimas
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]

        senha = request.form["senha"]


        if usuario == ADMIN_USUARIO and senha == ADMIN_SENHA:

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
                "Usuário ou senha incorretos.",
                "danger"
            )


    return render_template("login.html")

@app.route("/logout")
def logout():

    session.pop("admin", None)


    flash(
        "Você saiu do painel administrativo.",
        "info"
    )


    return redirect(
        url_for("login")
    )

@app.route("/sobre")
def sobre():

    return render_template("sobre.html")



@app.route("/cadastrar", methods=["GET","POST"])
def cadastrar():


    if request.method == "POST":


        mensagens = carregar_dados()


        agora = datetime.now()


        nova_mensagem = {


            "id": len(mensagens)+1,


            "codigo": gerar_codigo(),


            "tipo": request.form["tipo"],


            "titulo": request.form["titulo"],


            "descricao": request.form["descricao"],


            "status": "Em análise",


            "resposta": "",


            "data": agora.strftime("%d/%m/%Y"),


            "hora": agora.strftime("%H:%M")


        }


        mensagens.append(nova_mensagem)


        salvar_dados(mensagens)



        return render_template(
            "codigo.html",
            codigo=nova_mensagem["codigo"]
        )


    return render_template("cadastrar.html")



@app.route("/acompanhar", methods=["GET", "POST"])
def acompanhar():

    mensagem_encontrada = None


    if request.method == "POST":

        codigo = request.form["codigo"]


        mensagens = carregar_dados()


        for mensagem in mensagens:

            if mensagem["codigo"] == codigo:

                mensagem_encontrada = mensagem

                mensagem_encontrada["descricao_status"] = mensagem_status(
                    mensagem["status"]
                )

                break



    return render_template(
        "acompanhar.html",
        mensagem=mensagem_encontrada
    )



@app.route("/mensagens")
def mensagens():

    if not administrador_logado():

        flash(
            "Faça login para acessar o painel.",
            "warning"
        )

        return redirect(
            url_for("login")
        )


    lista = carregar_dados()


    sugestoes = sum(
        1 for m in lista
        if m["tipo"] == "Sugestão"
    )


    reclamacoes = sum(
        1 for m in lista
        if m["tipo"] == "Reclamação"
    )


    elogios = sum(
        1 for m in lista
        if m["tipo"] == "Elogio"
    )


    return render_template(
        "mensagens.html",
        mensagens=lista,
        sugestoes=sugestoes,
        reclamacoes=reclamacoes,
        elogios=elogios
    )

@app.route("/responder/<int:id>", methods=["POST"])
def responder(id):


    if not administrador_logado():

        flash(
            "Acesso negado.",
            "danger"
        )

        return redirect(
            url_for("login")
        )



    mensagens = carregar_dados()


    for mensagem in mensagens:

        if mensagem["id"] == id:

            mensagem["status"] = request.form["status"]

            mensagem["resposta"] = request.form["resposta"]

            break



    salvar_dados(mensagens)



    flash(
        "Resposta enviada com sucesso!",
        "success"
    )



    return redirect(
        url_for("mensagens")
    )

@app.route("/dashboard")
def dashboard():

    if not administrador_logado():

        flash(
            "Faça login para acessar o painel.",
            "warning"
        )

        return redirect(
            url_for("login")
        )


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



    analise = sum(
        1 for m in mensagens
        if m["status"] == "Em análise"
    )



    resolvidas = sum(
        1 for m in mensagens
        if m["status"] == "Resolvido"
    )



    recusadas = sum(
        1 for m in mensagens
        if m["status"] == "Recusado"
    )



    return render_template(
        "dashboard.html",
        total=total,
        sugestoes=sugestoes,
        reclamacoes=reclamacoes,
        elogios=elogios,
        analise=analise,
        resolvidas=resolvidas,
        recusadas=recusadas
    )

if __name__ == "__main__":

    app.run(debug=True)