"""Testes unitários para a classe Polinomio (pacote `src`)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.polinomio import Polinomio


class TestPolinomio(unittest.TestCase):
    def test_polinomio_nulo(self) -> None:
        p = Polinomio()
        self.assertEqual(p.tamanho(), 0)
        self.assertEqual(p.grau(), -1)
        self.assertEqual(str(p), "0")

    def test_construcao_e_ordenacao(self) -> None:
        p = Polinomio([(-7, 5), (2, 3), (5.3, 1), (-2, 0)])
        self.assertEqual(p.grau(), 5)
        self.assertEqual(p.tamanho(), 4)
        self.assertEqual(str(p), "-7x^5 + 2x^3 + 5.3x - 2")

    def test_grau_e_tamanho_do_exemplo_do_enunciado(self) -> None:
        p = Polinomio.a_partir_de_lista_plana([4, 6, 3, 9])
        self.assertEqual(p.grau(), 9)
        self.assertEqual(p.tamanho(), 2)

    def test_exibicao_do_exemplo_do_enunciado(self) -> None:
        p = Polinomio.a_partir_de_lista_plana([8, 0, 2, 5, 4, 6, -1, 1])
        self.assertEqual(p.exibir(), "4x^6 + 2x^5 - x + 8")

    def test_avaliacao(self) -> None:
        p = Polinomio.a_partir_de_lista_plana([-2, 2, 4, 1])
        # p(x) = -2x^2 + 4x  =>  p(3) = -2*9 + 4*3 = -6
        self.assertAlmostEqual(p.avaliar(3), -6)

    def test_adicao_com_simplificacao(self) -> None:
        p = Polinomio([(2, 2), (-4, 1), (1, 0)])
        q = Polinomio([(-3, 4), (5, 2), (4, 1), (-10, 0)])
        w = p + q
        self.assertEqual(str(w), "-3x^4 + 7x^2 - 9")

    def test_subtracao(self) -> None:
        p = Polinomio([(5, 2), (3, 0)])
        q = Polinomio([(2, 2), (3, 0)])
        self.assertEqual(str(p - q), "3x^2")

    def test_multiplicacao(self) -> None:
        p = Polinomio([(1, 1), (1, 0)])   # x + 1
        q = Polinomio([(1, 1), (-1, 0)])  # x - 1
        resultado = p * q                 # (x+1)(x-1) = x^2 - 1
        self.assertEqual(str(resultado), "x^2 - 1")

    def test_simplificar_remove_coeficiente_zero(self) -> None:
        p = Polinomio([(3, 2), (-3, 2), (5, 0)])
        self.assertEqual(str(p), "5")
        self.assertEqual(p.tamanho(), 1)

    def test_igualdade(self) -> None:
        p = Polinomio([(1, 2), (1, 0)])
        q = Polinomio([(1, 0), (1, 2)])
        self.assertEqual(p, q)


if __name__ == "__main__":
    unittest.main()