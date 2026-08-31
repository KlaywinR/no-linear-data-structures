"""
Implementa a classe Polinomio: representação e manipulação de
polinômios univariados por meio de uma lista encadeada.

Cada monômio a_i * x^j é armazenado em um TermoPolinomio, guardando
o coeficiente (a_i) e o grau (j). A lista é mantida ordenada de forma
decrescente pelo grau, com um nó-cabeça no início, exatamente
como ilustrado na Figura 1 do enunciado.
"""

from __future__ import annotations
from typing import Iterable, List, Optional, Tuple

from .termo_polinomio import TermoPolinomio

Monomio = Tuple[float, int] 

class Polinomio:
    """
    Representa um polinômio univariado a_n*x^n + ... + a_1*x + a_0,
    armazenado internamente como uma lista encadeada ordenada de forma
    decrescente pelo grau de cada monômio.
    """
    _EPSILON = 1e-9

    def __init__(self, termos: Optional[Iterable[Monomio]] = None) -> None:
        """
        Construtor. Cria um polinômio a partir de uma coleção opcional
        de monômios (coeficiente, grau).

        Args:
            termos: iterável de tuplas (coeficiente, grau). Caso omitido,
                cria o polinômio nulo (p(x) = 0).
        """
        self._cabeca: TermoPolinomio = TermoPolinomio(None, None)

        if termos is not None:
            for coeficiente, grau in termos:
                self._inserir_termo(coeficiente, grau)
            self.simplificar()
            
    # Inserção ordenada
    def _inserir_termo(self, coeficiente: float, grau: int) -> None:
        """
        Insere um novo termo mantendo a lista ordenada em ordem
        decrescente de grau. Não faz fusão de termos de mesmo grau - responsabilidade de `simplificar`.
        """
        novo_termo = TermoPolinomio(coeficiente, grau)

        anterior = self._cabeca
        atual = self._cabeca.proximo
        while atual is not None and atual.grau > grau:
            anterior = atual
            atual = atual.proximo

        novo_termo.proximo = atual
        anterior.proximo = novo_termo

    def _termos(self) -> List[TermoPolinomio]:
        """Retorna, em uma lista Python, os nós de dados."""
        termos = []
        atual = self._cabeca.proximo
        while atual is not None:
            termos.append(atual)
            atual = atual.proximo
        return termos

    # a) Grau
    def grau(self) -> int:
        """
        Retorna o grau do polinômio (maior expoente com coeficiente
        não-nulo).

        Returns:
            O grau do polinômio, ou -1 caso o polinômio seja nulo
            (p(x) = 0), por convenção matemática usual.
        """
        primeiro = self._cabeca.proximo
        return primeiro.grau if primeiro is not None else -1

    #Mantendo a nomenclatura do enunciado (g/G)
    g = grau
    G = grau

    # b) Tamanho
    def tamanho(self) -> int:
        """Retorna o número de termos (monômios) do polinômio."""
        contador = 0
        atual = self._cabeca.proximo
        while atual is not None:
            contador += 1
            atual = atual.proximo
        return contador

    t = tamanho
    T = tamanho
    
    # c) Adição -> operador +
    def __add__(self, outro: "Polinomio") -> "Polinomio":
        """
        Soma dois polinômios (self + outro), retornando um novo
        polinômio já simplificado.
        """
        if not isinstance(outro, Polinomio):
            return NotImplemented

        resultado = Polinomio()
        for termo in self._termos():
            resultado._inserir_termo(termo.coeficiente, termo.grau)
        for termo in outro._termos():
            resultado._inserir_termo(termo.coeficiente, termo.grau)
        resultado.simplificar()
        return resultado
    
    # d) Subtração -> operador -
    def __sub__(self, outro: "Polinomio") -> "Polinomio":
        """
        Subtrai dois polinômios (self - outro), retornando um novo
        polinômio já simplificado.
        """
        if not isinstance(outro, Polinomio):
            return NotImplemented

        resultado = Polinomio()
        for termo in self._termos():
            resultado._inserir_termo(termo.coeficiente, termo.grau)
        for termo in outro._termos():
            resultado._inserir_termo(-termo.coeficiente, termo.grau)
        resultado.simplificar()
        return resultado

    # e) Multiplicação -> operador *
    def __mul__(self, outro: "Polinomio") -> "Polinomio":
        """
        Multiplica dois polinômios (self * outro), retornando um novo
        polinômio já simplificado.
        """
        if not isinstance(outro, Polinomio):
            return NotImplemented

        resultado = Polinomio()
        for termo_a in self._termos():
            for termo_b in outro._termos():
                novo_coeficiente = termo_a.coeficiente * termo_b.coeficiente
                novo_grau = termo_a.grau + termo_b.grau
                resultado._inserir_termo(novo_coeficiente, novo_grau)
        resultado.simplificar()
        return resultado
  
    # f) Avaliação
    def avaliar(self, x: float) -> float:
        """
        Avalia o polinômio para um valor real x fornecido, isto é,
        calcula p(x).

        Args:
            x: valor real no qual o polinômio será avaliado.

        Returns:
            O resultado numérico de p(x).
        """
        resultado = 0.0
        atual = self._cabeca.proximo
        while atual is not None:
            resultado += atual.coeficiente * (x ** atual.grau)
            atual = atual.proximo
        return resultado

    a = avaliar
    A = avaliar


    # g) Exibição -> __str__ (equivalente à sobrecarga do operador <<)
    def exibir(self) -> str:
        """
        Gera e retorna a representação textual do polinômio, no formato
        "a_n*x^n + ... + a_1*x + a_0", omitindo termos de coeficiente
        nulo e simplificando a notação de expoentes 0 e 1.

        Returns:
            String com a representação textual do polinômio.
        """
        termos = self._termos()

        if not termos:
            return "0"

        partes: List[str] = []
        for indice, termo in enumerate(termos):
            coeficiente, grau = termo.coeficiente, termo.grau
            sinal = "-" if coeficiente < 0 else "+"
            modulo = abs(coeficiente)

            # Formata o valor absoluto do coeficiente sem casas decimais
            # desnecessárias (ex.: 5.0 -> "5", 5.3 -> "5.3").
            if float(modulo).is_integer():
                texto_coeficiente = str(int(modulo))
            else:
                texto_coeficiente = str(modulo)

            if grau == 0:
                termo_str = texto_coeficiente
            elif grau == 1:
                termo_str = "x" if texto_coeficiente == "1" else f"{texto_coeficiente}x"
            else:
                termo_str = f"x^{grau}" if texto_coeficiente == "1" else f"{texto_coeficiente}x^{grau}"

            if indice == 0:
                partes.append(f"-{termo_str}" if sinal == "-" else termo_str)
            else:
                partes.append(f" {sinal} {termo_str}")

        return "".join(partes)

    p = exibir
    P = exibir

    def __str__(self) -> str:
        return self.exibir()

    def __repr__(self) -> str:
        return f"Polinomio('{self.exibir()}')"
    
    # h) Simplificação
    def simplificar(self) -> None:
        """
        Simplifica o polinômio, unificando (somando) monômios de mesmo
        grau e eliminando monômios com coeficiente igual a zero.

        Como a lista é mantida ordenada de forma decrescente pelo grau,
        termos de mesmo grau ficam sempre adjacentes, o que permite
        realizar a simplificação em uma única passagem O(n).
        """
        anterior = self._cabeca
        atual = self._cabeca.proximo

        while atual is not None:
            # Funde todos os termos que possuam o mesmo grau.
            while atual.proximo is not None and atual.proximo.grau == atual.grau:
                duplicado = atual.proximo
                atual.coeficiente += duplicado.coeficiente
                atual.proximo = duplicado.proximo
                duplicado.proximo = None  # quebra o nó fundido

            if abs(atual.coeficiente) < self._EPSILON:
                # Remove o termo com coeficiente zero.
                anterior.proximo = atual.proximo
                removido = atual
                atual = atual.proximo
                removido.proximo = None
            else:
                anterior = atual
                atual = atual.proximo
                
    # Métodos utilitários - main/testes
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Polinomio):
            return NotImplemented
        termos_a = [(t.coeficiente, t.grau) for t in self._termos()]
        termos_b = [(t.coeficiente, t.grau) for t in other._termos()]
        return termos_a == termos_b

    @classmethod
    def a_partir_de_lista_plana(cls, numeros: Iterable[float]) -> "Polinomio":
        """
        Constrói um Polinomio a partir de uma sequência "plana" de
        números, agrupados dois a dois como (coeficiente, grau) —
        exatamente o formato utilizado no arquivo de entrada descrito
        na Figura 2 do enunciado (ex.: "-3 5 6 3 -7 1 8 0").

        Args:
            numeros: sequência plana [coef_1, grau_1, coef_2, grau_2, ...]

        Returns:
            Um novo Polinomio já simplificado.
        """
        valores = list(numeros)
        pares = [
            (float(valores[i]), int(valores[i + 1]))
            for i in range(0, len(valores), 2)
        ]
        return cls(pares)