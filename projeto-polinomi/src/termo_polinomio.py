"""
Módulo: src/termo_polinomio.py

Implementa TermoPolinomio, o nó especializado utilizado pela classe
Polinomio. Cada nó modela um monômio a_i * x^j, armazenando o
coeficiente (a_i) e o grau (j), além do ponteiro para o próximo termo.

Segue o mesmo padrão de nó apresentado na Figura 1 do enunciado
(nó-cabeça + nós de dados com campos "coeficiente" e "grau").
"""
from __future__ import annotations
from typing import Optional


class TermoPolinomio:
    """
    Representa um único termo (monômio) de um polinômio: coeficiente * x^grau.

    Attributes:
        coeficiente (float): valor do coeficiente do monômio (a_i).
        grau (Optional[int]): expoente da variável x (j). É None apenas
            no nó-cabeça (sentinela), que não representa um monômio real.
        proximo (Optional[TermoPolinomio]): referência para o próximo
            termo da lista.
    """

    __slots__ = ("coeficiente", "grau", "proximo")

    def __init__(self, coeficiente: Optional[float], grau: Optional[int]) -> None:
        self.coeficiente: Optional[float] = coeficiente
        self.grau: Optional[int] = grau
        self.proximo: Optional["TermoPolinomio"] = None

    def __repr__(self) -> str:
        return f"TermoPolinomio(coeficiente={self.coeficiente}, grau={self.grau})"