"""
Programa principal do Projeto Polinômio.
Execução:
    python main.py
    python main.py caminho/para/arquivo.txt
"""

from __future__ import annotations

import sys
from pathlib import Path

from src import Polinomio, processar_arquivo, FormatoArquivoInvalidoError


CAMINHO_PADRAO = Path(__file__).parent / "data" / "entrada_exemplo.txt"


def linha(caractere: str = "─", tamanho: int = 80) -> None:
    """Linha separadora."""
    print(caractere * tamanho)


def titulo(texto: str) -> None:
    """Título principal."""
    print()
    linha("═")
    print(texto.center(80))
    linha("═")

def secao(numero: int, texto: str) -> None:
    """Título de uma seção."""
    print()
    print(f"[ {numero} ] {texto.upper()}")
    linha()

def sucesso(texto: str) -> None:
    """MAensagem de sucesso."""
    print()
    print(f"{texto}")

def demonstrar_polinomio() -> None:
    """Demonstra as operações principais com polinômios."""

    titulo("PROJETO POLINÔMIO")
    print("Demonstração das operações".center(80))

    # 1. CONSTRUÇÃO
    secao(1, "Construção")

    p = Polinomio([
        (-7, 5),
        (2, 3),
        (5.3, 1),
        (-2, 0),
    ])

    print(f"{'p(x)':<12}= {p}")
    print(f"{'Grau':<12}= {p.grau()}")
    print(f"{'Tamanho':<12}= {p.tamanho()} termos")

    # 2. AVALIAÇÃO
    secao(2, "Avaliação")

    x = 2

    print(f"{'p(x)':<12}= {p}")
    print(f"{'p(2)':<12}= {p.avaliar(x)}")

    # 3. OPERAÇÕES
    secao(3, "Operações")

    q = Polinomio([
        (6, 4),
        (8, 1),
        (-2, 0),
    ])

    print(f"{'q(x)':<12}= {q}")
    print()

    print(f"{'p + q':<12}= {p + q}")
    print(f"{'p - q':<12}= {p - q}")
    print(f"{'p × q':<12}= {p * q}")

    # 4. SIMPLIFICAÇÃO
    secao(4, "Simplificação")

    poli_p = Polinomio([
        (2, 2),
        (-4, 1),
        (1, 0),
    ])

    poli_q = Polinomio([
        (-3, 4),
        (5, 2),
        (4, 1),
        (-10, 0),
    ])

    soma = poli_p + poli_q

    print(f"{'p(x)':<12}= {poli_p}")
    print(f"{'q(x)':<12}= {poli_q}")
    print(f"{'w(x)':<12}= p(x) + q(x)")
    print(f"{'Resultado':<12}= {soma}")

    assert str(soma) == "-3x^4 + 7x^2 - 9", (
        "Resultado divergente do esperado no enunciado!"
    )

    sucesso("O resultado confere com o esperado no enunciado.")


def demonstrar_processamento_arquivo(caminho: str) -> bool:
    """Processa o arquivo de entrada e exibe os resultados."""

    titulo("PROCESSAMENTO DO ARQUIVO DE ENTRADA")

    print(f"Arquivo: {caminho}")

    try:
        resultados = processar_arquivo(caminho)

    except (FormatoArquivoInvalidoError, FileNotFoundError) as erro:
        print()
        print(f"Não foi possível processar o arquivo.")
        print(f"  Motivo: {erro}")
        return False

    for numero, resultado in enumerate(resultados, start=1):
        print()
        print(f"[ {numero} ]")

        linha()

        print(resultado)

    return True


def escolher_arquivo() -> str:
    """
    Define qual arquivo será processado.

    Se o caminho for informado pela linha de comando, ele será usado.
    Caso contrário, o usuário pode informar um caminho ou pressionar
    ENTER para utilizar o arquivo de exemplo.
    """
    if len(sys.argv) > 1:
        return sys.argv[1]

    print()
    print("Arquivo de entrada")
    linha()

    print(f"Arquivo de exemplo: {CAMINHO_PADRAO}")
    print()

    resposta = input(
        "Por favor, digite o caminho do arquivo ou pressione ENTER para usar "
        "o arquivo de exemplo: "
    ).strip()

    if resposta:
        return resposta

    return str(CAMINHO_PADRAO)

def main() -> None:
    """Função principal do programa."""

    caminho_arquivo = escolher_arquivo()

    demonstrar_polinomio()

    sucesso_arquivo = demonstrar_processamento_arquivo(caminho_arquivo)

    print()
    linha("═")

    if sucesso_arquivo:
        print(
            "A DEMONSTRAÇÃO FOI CONCLUÍDA COM SUCESSO".center(80)
        )
    else:
        print(
            "A DEMONSTRAÇÃO CONCLUÍDA COM ERROS NO ARQUIVO".center(80)
        )

    linha("═")

if __name__ == "__main__":
    main()