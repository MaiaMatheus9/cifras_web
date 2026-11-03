"""Grupo 9 - Cifras Polialfabéticas e Combinatória (Matemática Discreta).
Módulo central: espaço de chaves N = |Σ|^k, variações combinatórias e cifra de Vigenère."""
import itertools, math, string

ALFABETO = string.ascii_uppercase      # Σ = {A..Z}, |Σ| = 26


def espaco_chaves(n: int, k: int) -> int:
    """N = n^k. Princípio multiplicativo: cada uma das k posições da chave
    é escolhida de forma independente entre n símbolos -> n·n·...·n (k vezes)."""
    if n < 1 or k < 1:
        raise ValueError("n e k devem ser inteiros positivos")
    N = 1
    for _ in range(k):                 # multiplicação explícita, passo a passo
        N *= n
    return N


def chaves_sem_repeticao(n: int, k: int) -> int:
    """Arranjo A(n,k) = n!/(n-k)!: chaves de k símbolos todos distintos."""
    return math.perm(n, k) if k <= n else 0


def chaves_combinacao(n: int, k: int) -> int:
    """Combinação C(n,k): conjuntos de k símbolos onde a ORDEM não importa."""
    return math.comb(n, k)


def verificar_por_enumeracao(n: int, k: int) -> int:
    """Conta todas as chaves uma a uma (produto cartesiano). Só viável para n,k pequenos."""
    return sum(1 for _ in itertools.product(range(n), repeat=k))


def formatar_tempo(segundos: int) -> str:
    for nome, v in (("anos", 31_557_600), ("dias", 86_400), ("horas", 3_600), ("min", 60)):
        if segundos >= v:
            return f"{segundos / v:,.2f} {nome}"
    return f"{segundos} s"


def resumo(n: int, k: int, taxa: int = 10**9) -> dict:
    """Linha de resultados: N, nº de dígitos, bits de segurança e tempo de força bruta
    (taxa = chaves testadas por segundo)."""
    N = espaco_chaves(n, k)
    return {"n": n, "k": k, "N": str(N), "digitos": len(str(N)),
            "bits": round(math.log2(N), 2), "tempo": formatar_tempo(N // taxa)}


def tabela(n: int = 26, ks=range(1, 21)) -> list:
    return [resumo(n, k) for k in ks]


def _deslocar(texto: str, chave: str, sinal: int) -> str:
    desloc = [ALFABETO.index(c) for c in chave.upper() if c in ALFABETO]
    if not desloc:
        raise ValueError("A chave precisa ter ao menos uma letra A-Z")
    saida, i = [], 0
    for c in texto:
        if c.isascii() and c.isalpha():          # só cifra letras A-Z; o resto passa intacto
            base = ord("A") if c.isupper() else ord("a")
            d = desloc[i % len(desloc)] * sinal  # cada letra usa um alfabeto diferente (polialfabética)
            saida.append(chr((ord(c) - base + d) % 26 + base))
            i += 1
        else:
            saida.append(c)
    return "".join(saida)


def cifrar(texto: str, chave: str) -> str:
    """Vigenère: C_i = (P_i + K_{i mod k}) mod 26."""
    return _deslocar(texto, chave, +1)


def decifrar(texto: str, chave: str) -> str:
    """Vigenère: P_i = (C_i - K_{i mod k}) mod 26."""
    return _deslocar(texto, chave, -1)
