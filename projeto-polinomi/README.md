# Projeto Polinômio — Estrutura de Dados Lineares

Implementação do Projeto Polinômio, uma representação e manipulação de polinômios univariados ultilizando listas encadeadas.


## Estrutura de diretórios

```
projeto_polinomio/
├── src/                        # Código-fonte 
│   ├── __init__.py              # API pública do pacote
│   ├── termo_polinomio.py        # Classe TermoPolinomio (nó: coeficiente + grau)
│   ├── polinomio.py               # Classe Polinomio
│   └── file_processor.py          # Leitura/execução do arquivo de entrada (Tarefa)
├── tests/                      # Unittests
│   ├── __init__.py
│   ├── test_polinomio.py
│   └── test_file_processor.py
├── data/                        # Arquivos de dados de entrada
│   └── entrada_exemplo.txt       # Exemplo da Figura 2 do enunciado
├── main.py                       # Programa principal / demonstração
└── README.md
```

## Como executar

```bash
# Demonstração completa (todas as operações + processamento da Tarefa)
python3 main.py

# Processar outro arquivo de entrada
python3 main.py caminho/para/outro_arquivo.txt

# Executar a suíte de testes
python3 -m unittest discover -s tests -v
```

## Modelagem

Cada monômio `aᵢ·x^j` é armazenado em um nó `TermoPolinomio`
(`coeficiente`, `grau`, `proximo`). A classe `Polinomio`
(`src/polinomio.py`) organiza esses nós em uma **lista encadeada com
nó-cabeça sentinela**, mantida sempre **ordenada de forma decrescente
pelo grau** — exatamente como ilustrado na Figura 1 do enunciado:

```
Head -> [<null>] -> [-7|5] -> [2|3] -> [5.3|1] -> [-2|0] -> null
                     (coef|grau)
```

## Operações implementadas

| Enunciado       | Letra  | Método / operador Python          |
|------------------|--------|--------------------------------------|
| Grau             | g / G  | `p.grau()`                           |
| Tamanho          | t / T  | `p.tamanho()`                        |
| Adição           | —      | `p + q`  (`__add__`)                 |
| Subtração        | —      | `p - q`  (`__sub__`)                 |
| Multiplicação    | —      | `p * q`  (`__mul__`)                 |
| Avaliação        | a / A  | `p.avaliar(x)`                       |
| Exibição         | p / P  | `p.exibir()` e `str(p)` (`__str__`)  |
| Simplificação    | —      | `p.simplificar()`                    |

A **simplificação** (fusão de monômios de mesmo grau e remoção de
coeficientes nulos) é chamada **automaticamente** ao final da
construção, da adição, da subtração e da multiplicação, então o
resultado de qualquer operação já sai simplificado — reproduzindo o
exemplo do enunciado: `p(x)+q(x)` resulta diretamente em
`-3x^4 + 7x^2 - 9`.

### Uso básico da API

```python
from src import Polinomio

p = Polinomio([(-7, 5), (2, 3), (5.3, 1), (-2, 0)])  # -7x^5 + 2x^3 + 5.3x - 2
q = Polinomio([(6, 4), (8, 1), (-2, 0)])               # 6x^4 + 8x - 2

print(p.grau())        # 5
print(p.tamanho())     # 4
print(p.avaliar(2))    # -199.4
print(p + q)            # -7x^5 + 6x^4 + 2x^3 + 13.3x - 4
print(p - q)            # -7x^5 - 6x^4 + 2x^3 - 2.7x
print(p * q)            # -42x^9 + 12x^7 - 56x^6 + ...
```

## Processamento do arquivo de entrada (Seção 2 — Tarefa)

O módulo `src/file_processor.py` expõe `processar_arquivo(caminho)`,
que lê o arquivo linha a linha no formato da Figura 2 do enunciado. Um
polinômio é representado como uma sequência "achatada" de números
(`coeficiente grau coeficiente grau ...`), por exemplo
`-3 5 6 3 -7 1 8 0` representa `-3x^5 + 6x^3 - 7x + 8`.

| Comando       | Linhas de dados consumidas em seguida                       |
|----------------|----------------------------------------------------------------|
| `+` `-` `*`   | 2 linhas (dois polinômios: operando 1 e operando 2)             |
| `g/G` `t/T` `p/P` | 1 linha (um polinômio)                                       |
| `a/A`         | 1 linha com o valor de `x`, depois 1 linha com o polinômio       |

Executando `main.py` sobre `data/entrada_exemplo.txt` (idêntico à
Figura 2) obtemos exatamente os resultados descritos no enunciado:

- **(a)** Adição de `p(x)=-3x⁵+6x³-7x+8` com `q(x)=6x⁴+8x-2` →
  `-3x⁵ + 6x⁴ + 6x³ + x + 6`
- **(b)** Grau do polinômio `3x⁹+4x⁶` → **9** ✔
- **(c)** Exibição de `4x⁶+2x⁵-x+8` → `4x^6 + 2x^5 - x + 8` ✔
- **(d)** Avaliação de `p(x) = -2x²+4x` em `x=3` → `p(3) = -6`

> **Nota sobre o item (d):** o enunciado apresenta o resultado da
> avaliação como `-42`, mas o cálculo correto de
> `p(3) = -2×(3)² + 4×(3) = -18 + 12` é **-6**. O código implementa a
> avaliação matematicamente correta (validada por teste unitário); o
> valor `-42` do PDF original parece ser um erro de digitação.

## Testes

A suíte em `tests/` (12 testes, todos passando) cobre:
- construção e ordenação decrescente por grau;
- grau, tamanho, avaliação e exibição textual;
- adição, subtração e multiplicação (com simplificação automática);
- remoção de coeficientes nulos e fusão de termos de mesmo grau;
- processamento completo do arquivo de exemplo (Figura 2), validando
  os quatro resultados esperados pelo enunciado;
- tratamento de erro para comando desconhecido no arquivo de entrada.

```bash
python3 -m unittest discover -s tests -v
```