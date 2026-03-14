from flask import Flask, render_template, request, redirect
import sqlite3
import datetime

app = Flask(__name__)

def db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():

    conn = db()

    pessoas = conn.execute(
        "SELECT * FROM atendidos"
    ).fetchall()

    return render_template("index.html", pessoas=pessoas)


@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")


@app.route("/salvar", methods=["POST"])
def salvar():

    nome = request.form["nome"]
    telefone = request.form["telefone"]
    ciclo = request.form["ciclo"]

    conn = db()

    conn.execute(
        "INSERT INTO atendidos (nome, telefone, inicio, ciclo, status) VALUES (?, ?, ?, ?, ?)",
        (nome, telefone, datetime.date.today(), ciclo, "ativo")
    )

    conn.commit()

    return redirect("/")


@app.route("/presenca/<id>")
def presenca(id):

    conn = db()

    conn.execute(
        "INSERT INTO presencas (atendido_id, data) VALUES (?, ?)",
        (id, datetime.date.today())
    )

    conn.execute(
        "UPDATE atendidos SET presencas = presencas + 1 WHERE id=?",
        (id,)
    )

    conn.commit()

    return redirect("/")


@app.route("/dashboard")
def dashboard():

    conn = db()

    total = conn.execute(
        "SELECT COUNT(*) as t FROM atendidos"
    ).fetchone()["t"]

    concluidos = conn.execute(
        "SELECT COUNT(*) as t FROM atendidos WHERE status='concluido'"
    ).fetchone()["t"]

    return render_template(
        "dashboard.html",
        total=total,
        concluidos=concluidos
    )


@app.route("/recepcao")
def recepcao():
    return render_template("recepcao.html")


@app.route("/esde")
def esde():

    conn = db()

    turmas = conn.execute(
        "SELECT * FROM turmas_esde"
    ).fetchall()

    return render_template("esde.html", turmas=turmas)


@app.route("/evangelizacao")
def evangelizacao():

    conn = db()

    alunos = conn.execute(
        "SELECT * FROM evangelizandos"
    ).fetchall()

    return render_template("evangelizacao.html", alunos=alunos)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
