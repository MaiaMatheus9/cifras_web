# Cifras Polialfabéticas e Combinatória

**Matemática Discreta, Grupo 9.** Conceitos: contagem, princípio multiplicativo e combinações.

Aplicação web em Python (Flask) que calcula o espaço de chaves de cifras polialfabéticas,

    N = |Σ|^k

onde |Σ| é o tamanho do alfabeto e k é o tamanho da chave. Também implementa a cifra de Vigenère, valida a fórmula com testes automáticos e traz explicação dos conceitos e um relatório técnico.

---

## 1. Como acessar

### Requisitos
- Python **3.8 ou superior** (o código usa `math.perm`, disponível a partir da 3.8)
- `pip` (já vem com o Python)
- Um navegador moderno

Verifique a versão do Python:
```bash
python --version        # no Linux/macOS, se não funcionar, use: python3 --version
```

### Passo a passo

**1) Extraia o `cifras_web.zip` e entre na pasta**
```bash
cd cifras_web
```

**2) (Recomendado) Crie um ambiente virtual**

Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```
Windows (PowerShell):
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```
Windows (CMD):
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**3) Instale a dependência**
```bash
pip install -r requirements.txt
```

**4) Inicie o servidor**
```bash
python app.py
```
O terminal mostrará algo como `Running on http://127.0.0.1:5000`.

**5) Abra no navegador**

    http://127.0.0.1:5000

Para encerrar o servidor, pressione `Ctrl + C` no terminal.

---

## 2. O que a página oferece

| Seção | Conteúdo |
|---|---|
| Calculadora (topo) | Calcula N = \|Σ\|^k para \|Σ\| e k de 1 a 100. Mostra nº de dígitos, bits de segurança, tempo estimado de força bruta, arranjo A(n,k) e combinação C(n,k). |
| 1. Conceitos fundamentais | Cifra polialfabética, princípio multiplicativo, arranjos, combinações e segurança. |
| 2. Algoritmo | Demonstração interativa da cifra de Vigenère (cifrar e decifrar). |
| 3. Testes e resultados | Os testes são executados ao vivo na página, mais uma tabela de N para k = 1 a 20 (\|Σ\| = 26). |
| 4. Relatório técnico | Objetivo, metodologia, resultados e conclusão. O botão "Imprimir / salvar em PDF" gera o arquivo pelo navegador. |

---

## 3. Estrutura do projeto

```
cifras_web/
├── app.py               # Servidor Flask: rotas da página e da API
├── cifras.py            # Núcleo matemático e a cifra de Vigenère (código comentado)
├── testes.py            # Testes automáticos; gera resultados.csv
├── templates/
│   └── index.html       # Interface web (HTML + CSS + JavaScript)
├── requirements.txt     # Dependências (Flask)
├── resultados.csv       # Tabela de N para k = 1..20, gerada pelo código
├── saida_testes.txt     # Saída da execução dos testes
└── README.md            # Este arquivo
```

---

## 4. Fundamentação matemática

- **Princípio multiplicativo:** uma tarefa com k etapas independentes, cada uma com m_j opções, pode ser feita de m_1 · m_2 · … · m_k modos. Cada uma das k posições da chave admite |Σ| símbolos, logo **N = |Σ|^k**.
- **Arranjo (chave sem símbolos repetidos):** A(n,k) = n! / (n−k)!
- **Combinação (a ordem não importa):** C(n,k) = n! / (k! · (n−k)!), e vale A(n,k) = C(n,k) · k!
- **Bits de segurança:** log₂(N). Cada letra a mais numa chave de 26 símbolos soma cerca de 4,7 bits.
- **Cifra de Vigenère:** cifrar C_i = (P_i + K_{i mod k}) mod 26; decifrar P_i = (C_i − K_{i mod k}) mod 26.

Exemplo: com |Σ| = 26 e k = 10, N = 141.167.095.653.376 (≈ 47 bits). A 10⁹ chaves por segundo, a busca exaustiva leva cerca de 1,63 dia.

---

## 5. Executando os testes

```bash
python testes.py
```

Isso imprime cada teste como `OK` ou `FALHA` e regrava o `resultados.csv`. Os testes cobrem:

1. Casos conhecidos: 26¹ = 26 (César) e 26⁵ = 11.881.376.
2. A fórmula N = |Σ|^k comparada com a **enumeração exaustiva** de todas as chaves, em casos pequenos.
3. O princípio multiplicativo: N(k+1) = n · N(k), para k de 1 a 29.
4. Os valores A(26,3) = 15.600 e C(26,3) = 2.600, e a identidade A = C · k!.
5. O vetor clássico de Vigenère: `ATTACKATDAWN` com chave `LEMON` resulta em `LXFOPVEFRNHR`.
6. Cifrar e depois decifrar devolve o texto original, mesmo com acentos e pontuação.
7. Entradas inválidas (n ou k menores que 1) geram erro.

---

## 6. API (opcional)

A interface usa estas rotas, que você também pode chamar diretamente:

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/espaco?n=26&k=10` | Espaço de chaves, bits, tempo, arranjo e combinação |
| GET | `/api/tabela` | Tabela de N para k = 1..20 com \|Σ\| = 26 |
| GET | `/api/testes` | Executa os testes e devolve o resultado em JSON |
| POST | `/api/cifra` | Corpo: `{"texto": "...", "chave": "...", "modo": "cifrar" ou "decifrar"}` |

Exemplo:
```bash
curl "http://127.0.0.1:5000/api/espaco?n=26&k=10"
```

---

## 7. Observações e limitações

- A cifra processa apenas letras **A–Z** (sem acento). Espaços, números, pontuação e letras acentuadas passam sem alteração. A chave usa só as letras A–Z que contiver.
- A calculadora aceita n e k entre **1 e 100**, para manter a resposta de tamanho razoável.
- O tempo de força bruta é uma **estimativa** que supõe 10⁹ chaves testadas por segundo.
- Um espaço de chaves grande não garante segurança: Vigenère é vulnerável à análise de frequência e ao teste de Kasiski, que descobrem k sem busca exaustiva. O espaço de chaves é condição necessária, não suficiente.
- O `app.py` roda com `debug=True`, o que serve para desenvolvimento local. Não use esse modo em um servidor público.

---

## 8. Solução de problemas

| Problema | Solução |
|---|---|
| `python: command not found` | Use `python3` (Linux/macOS) ou `py` (Windows). |
| `No module named flask` | Ative o ambiente virtual e rode `pip install -r requirements.txt`. |
| Erro de ativação no PowerShell | Execute `Set-ExecutionPolicy -Scope Process RemoteSigned` e tente de novo. |
| Porta 5000 ocupada (comum no macOS por causa do AirPlay) | Troque a última linha do `app.py` para `app.run(debug=True, port=5001)` e acesse `http://127.0.0.1:5001`. |
| Página abre, mas tabela e testes não carregam | Acesse pelo servidor (`http://127.0.0.1:5000`). Abrir o `index.html` direto no navegador não funciona, pois ele depende da API. |

---

## 9. Autoria

Preencha com os nomes do grupo, a disciplina, o professor e a data.
