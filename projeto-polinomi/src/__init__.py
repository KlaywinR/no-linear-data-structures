"""
Pacote `src` — Projeto Polinômio.

Contém a implementação completa da representação e manipulação de
polinômios univariados por meio de lista encadeada.
"""
from .termo_polinomio import TermoPolinomio
from .polinomio import Polinomio
from .file_processor import (
    processar_arquivo,
    ResultadoOperacao,
    FormatoArquivoInvalidoError,
)

__all__ = [
    "TermoPolinomio",
    "Polinomio",
    "processar_arquivo",
    "ResultadoOperacao",
    "FormatoArquivoInvalidoError",
]

__version__ = "1.0.0"