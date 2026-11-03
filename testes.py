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
    return casos


if __name__ == "__main__":
    for c in executar_testes():
        print("OK  " if c["ok"] else "FALHA", c["teste"])
    with open("resultados.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["n", "k", "N", "digitos", "bits", "tempo"])
        w.writeheader(); w.writerows(cifras.tabela(26, range(1, 21)))
    print("resultados.csv gerado.")
