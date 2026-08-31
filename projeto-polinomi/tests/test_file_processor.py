"""Testes unitários para o módulo file_processor (pacote `src`)."""

import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.file_processor import processar_arquivo, FormatoArquivoInvalidoError

CAMINHO_ENTRADA_EXEMPLO = Path(__file__).parent.parent / "data" / "entrada_exemplo.txt"

class TestFileProcessor(unittest.TestCase):
    def test_processa_arquivo_de_exemplo_da_figura_2(self) -> None:
        resultados = processar_arquivo(str(CAMINHO_ENTRADA_EXEMPLO))
        self.assertEqual(len(resultados), 4)

        self.assertIn("Adição", resultados[0].descricao)
        self.assertEqual(resultados[0].resultado, "-3x^5 + 6x^4 + 6x^3 + x + 6")

        self.assertEqual(resultados[1].resultado, "9")

        self.assertEqual(resultados[2].resultado, "4x^6 + 2x^5 - x + 8")

        self.assertEqual(resultados[3].resultado, "-6")

    def test_comando_desconhecido_levanta_erro(self) -> None:
        caminho_temp = Path(__file__).parent / "_arquivo_invalido_temp.txt"
        caminho_temp.write_text("z\n1 1\n", encoding="utf-8")
        try:
            with self.assertRaises(FormatoArquivoInvalidoError):
                processar_arquivo(str(caminho_temp))
        finally:
            caminho_temp.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()