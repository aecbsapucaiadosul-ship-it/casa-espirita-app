from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    db = get_db()
    pessoas = db.execute("SELECT * FROM atendidos").fetchall()
    return render_template("index.html", pessoas=pessoas)

@app.route("/novo", methods=["POST"])
def novo():

    nome = request.form["nome"]
    telefone = request.form["telefone"]

    db = get_db()

    db.execute(
        "INSERT INTO atendidos (nome, telefone, presencas) VALUES (?, ?, 0)",
        (nome, telefone)
    )

    db.commit()

    return redirect("/")

@app.route("/presenca/<id>")
def presenca(id):

    db = get_db()

    db.execute(
        "UPDATE atendidos SET presencas = presencas + 1 WHERE id=?",
        (id,)
    )

    db.commit()

    return redirect("/")

app.run(host="0.0.0.0", port=81)
