"""Servidor web. Execute: python app.py  ->  http://127.0.0.1:5000"""
from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import BadRequest
import cifras, testes

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/espaco")
def api_espaco():
    n, k = request.args.get("n", 26, type=int), request.args.get("k", 8, type=int)
    if not (1 <= n <= 100 and 1 <= k <= 100):       # limites p/ não estourar a resposta
        return jsonify(erro="Use n e k entre 1 e 100."), 400
    r = cifras.resumo(n, k)
    r["arranjo"] = str(cifras.chaves_sem_repeticao(n, k))
    r["combinacao"] = str(cifras.chaves_combinacao(n, k)) if k <= n else "0"
    return jsonify(r)


@app.get("/api/tabela")
def api_tabela():
    return jsonify(cifras.tabela(26, range(1, 21)))


@app.get("/api/testes")
def api_testes():
    return jsonify(testes.executar_testes() + testes.executar_testes_api())


@app.post("/api/cifra")
def api_cifra():
    try:
        d = request.get_json()
    except BadRequest:
        return jsonify(erro="Envie um JSON válido."), 400
    if not isinstance(d, dict):
        return jsonify(erro="O corpo deve ser um objeto JSON."), 400
    modo = d.get("modo")
    if modo not in ("cifrar", "decifrar"):
        return jsonify(erro="O modo deve ser 'cifrar' ou 'decifrar'."), 400
    texto, chave = d.get("texto", ""), d.get("chave", "")
    if not isinstance(texto, str) or not isinstance(chave, str):
        return jsonify(erro="Texto e chave devem ser strings."), 400
    try:
        f = cifras.cifrar if modo == "cifrar" else cifras.decifrar
        return jsonify(resultado=f(texto, chave))
    except ValueError as e:
        return jsonify(erro=str(e)), 400


if __name__ == "__main__":
    app.run(debug=True)
