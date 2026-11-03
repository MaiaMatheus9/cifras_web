"""Testes automáticos. `python testes.py` imprime o resultado e gera resultados.csv."""
import csv, math, cifras


def executar_testes() -> list:
    casos = []
    def t(nome, cond, detalhe=""):
        casos.append({"teste": nome, "ok": bool(cond), "detalhe": detalhe})

    t("César: 26^1 = 26", cifras.espaco_chaves(26, 1) == 26)
    t("26^5 = 11.881.376", cifras.espaco_chaves(26, 5) == 11_881_376)
    t("Fórmula = enumeração (n,k pequenos)",
      all(cifras.espaco_chaves(n, k) == cifras.verificar_por_enumeracao(n, k)
          for n, k in [(2, 4), (3, 5), (4, 6), (26, 3)]), "(2,4) (3,5) (4,6) (26,3)")
    t("Princípio multiplicativo: N(k+1) = N(k)·n",
      all(cifras.espaco_chaves(26, k + 1) == 26 * cifras.espaco_chaves(26, k) for k in range(1, 30)))
    t("Arranjo A(26,3) = 15.600", cifras.chaves_sem_repeticao(26, 3) == 15_600)
    t("Combinação C(26,3) = 2.600", cifras.chaves_combinacao(26, 3) == 2_600)
    t("A(n,k) = C(n,k)·k!", cifras.chaves_sem_repeticao(26, 4) == cifras.chaves_combinacao(26, 4) * math.factorial(4))
    t("Vetor clássico Vigenère (LEMON)", cifras.cifrar("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR")
    msg = "Olá, Mundo! Matemática Discreta."
    t("Cifrar e decifrar devolve o original", cifras.decifrar(cifras.cifrar(msg, "chave"), "chave") == msg)
    for entrada in [(0, 3), (26, 0)]:
        try:
            cifras.espaco_chaves(*entrada); ok = False
        except ValueError:
            ok = True
        t(f"Entrada inválida {entrada} gera erro", ok)
    t("Arranjo com k > n vale zero", cifras.chaves_sem_repeticao(2, 3) == 0)
    t("Chave sem letras A-Z gera erro",
      _gera_value_error(lambda: cifras.cifrar("texto", "123!")))
    t("Texto vazio é aceito", cifras.cifrar("", "CHAVE") == "")

    return casos


def _gera_value_error(funcao):
    try:
        funcao()
    except ValueError:
        return True
    return False


def executar_testes_api() -> list:
    # Import local para evitar ciclo: app importa este módulo para expor a rota /api/testes.
    from app import app

    cliente = app.test_client()
    casos = []
    verificacoes = (
        ("API cifra texto válido", cliente.post("/api/cifra", json={"texto": "ATTACKATDAWN", "chave": "LEMON", "modo": "cifrar"}), 200, "LXFOPVEFRNHR"),
        ("API decifra texto válido", cliente.post("/api/cifra", json={"texto": "LXFOPVEFRNHR", "chave": "LEMON", "modo": "decifrar"}), 200, "ATTACKATDAWN"),
        ("API rejeita JSON malformado", cliente.post("/api/cifra", data="{", content_type="application/json"), 400, None),
        ("API rejeita corpo que não é objeto", cliente.post("/api/cifra", json=[1]), 400, None),
        ("API rejeita modo desconhecido", cliente.post("/api/cifra", json={"texto": "oi", "chave": "A", "modo": "outro"}), 400, None),
        ("API rejeita texto que não é string", cliente.post("/api/cifra", json={"texto": 1, "chave": "A", "modo": "cifrar"}), 400, None),
    )
    for nome, resposta, status_esperado, resultado_esperado in verificacoes:
        ok = resposta.status_code == status_esperado
        if resultado_esperado is not None:
            ok = ok and resposta.get_json().get("resultado") == resultado_esperado
        casos.append({"teste": nome, "ok": ok, "detalhe": f"HTTP {resposta.status_code}"})
    return casos


if __name__ == "__main__":
    for c in executar_testes() + executar_testes_api():
        print("OK  " if c["ok"] else "FALHA", c["teste"])
    with open("resultados.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["n", "k", "N", "digitos", "bits", "tempo"])
        w.writeheader(); w.writerows(cifras.tabela(26, range(1, 21)))
    print("resultados.csv gerado.")
