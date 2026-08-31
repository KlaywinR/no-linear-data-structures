"""
Módulo: src/file_processor.py

Implementa a leitura e o processamento do arquivo de entrada descrito
na Seção 2 ("Tarefa") do enunciado do Projeto Polinômio.

Formato do arquivo (ver Figura 2 do enunciado):
    - Cada linha contém um COMANDO ou os dados de UM POLINÔMIO.
    - Um polinômio é representado como uma sequência "achatada" de
      números: coeficiente_1 grau_1 coeficiente_2 grau_2 ...
      (ex.: "-3 5 6 3 -7 1 8 0" representa -3x^5 + 6x^3 - 7x + 8).
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List

from .polinomio import Polinomio


@dataclass
class ResultadoOperacao:
    """Representa o resultado de uma operação lida do arquivo de entrada."""
    comando: str
    descricao: str
    resultado: str

    def __str__(self) -> str:
        return self.descricao


class FormatoArquivoInvalidoError(Exception):
    """Levantada quando o arquivo de entrada não segue o formato esperado."""
_COMANDOS_BINARIOS = {
    "+": ("Adição", lambda p, q: p + q),
    "-": ("Subtração", lambda p, q: p - q),
    "*": ("Multiplicação", lambda p, q: p * q),
}
_COMANDOS_UNARIOS_POLINOMIO = {"g", "G", "t", "T", "p", "P"}
_COMANDOS_AVALIACAO = {"a", "A"}


def _ler_polinomio(linhas: List[str], indice: int) -> Polinomio:
    if indice >= len(linhas):
        raise FormatoArquivoInvalidoError(
            "Fim de arquivo inesperado: esperava-se uma linha com um polinômio."
        )
    return Polinomio.a_partir_de_lista_plana(linhas[indice].split())


def processar_arquivo(caminho: str) -> List[ResultadoOperacao]:
    """
    Lê e processa o arquivo de entrada, executando cada operação na
    ordem em que aparece no arquivo.

    Args:
        caminho: caminho para o arquivo texto de entrada.

    Returns:
        Lista de ResultadoOperacao, uma para cada comando processado.

    Raises:
        FormatoArquivoInvalidoError: se o arquivo estiver mal formado
            ou contiver um comando desconhecido.
    """
    with open(caminho, "r", encoding="utf-8") as arquivo:
        linhas = [linha.strip() for linha in arquivo if linha.strip()]

    resultados: List[ResultadoOperacao] = []
    indice = 0

    while indice < len(linhas):
        comando = linhas[indice]
        indice += 1

        if comando in _COMANDOS_BINARIOS:
            nome_operacao, operacao = _COMANDOS_BINARIOS[comando]
            p = _ler_polinomio(linhas, indice)
            indice += 1
            q = _ler_polinomio(linhas, indice)
            indice += 1

            r = operacao(p, q)
            descricao = f"{nome_operacao}: [{p}] {comando} [{q}] = [{r}]"
            resultados.append(ResultadoOperacao(comando, descricao, str(r)))

        elif comando in _COMANDOS_UNARIOS_POLINOMIO:
            p = _ler_polinomio(linhas, indice)
            indice += 1

            if comando in ("g", "G"):
                valor = p.grau()
                descricao = f"Grau: grau([{p}]) = {valor}"
            elif comando in ("t", "T"):
                valor = p.tamanho()
                descricao = f"Tamanho: tamanho([{p}]) = {valor}"
            else:  # 'p' / 'P'
                valor = p.exibir()
                descricao = f"Exibição: {valor}"

            resultados.append(ResultadoOperacao(comando, descricao, str(valor)))

        elif comando in _COMANDOS_AVALIACAO:
            if indice >= len(linhas):
                raise FormatoArquivoInvalidoError(
                    "Fim de arquivo inesperado: esperava-se o valor de x para avaliação."
                )
            x = float(linhas[indice])
            indice += 1
            p = _ler_polinomio(linhas, indice)
            indice += 1

            valor = p.avaliar(x)
            descricao = f"Avaliação: p(x) = [{p}]  =>  p({x:g}) = {valor:g}"
            resultados.append(ResultadoOperacao(comando, descricao, f"{valor:g}"))

        else:
            raise FormatoArquivoInvalidoError(
                f"Comando desconhecido '{comando}' (linha {indice})."
            )

    return resultados