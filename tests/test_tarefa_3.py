"""
Testes automatizados para a Tarefa 3: Worker Grava o Resultado
"""
import unittest
from unittest.mock import MagicMock, patch

from app.worker import processar_tarefa


class TestTarefa3(unittest.TestCase):

    @patch("app.fila.guardar_resultado")
    def test_processar_tarefa_sucesso(self, mock_guardar):
        mock_modelo = MagicMock()
        mock_modelo.prever.return_value = {
            "texto": "adorei o servico",
            "sentimento": "positivo",
            "confianca": 0.992,
        }

        tarefa = {
            "id": "tarefa-teste-123",
            "texto": "adorei o servico",
        }

        resultado = processar_tarefa(tarefa, mock_modelo)

        # Verifica chamada ao modelo de inferência
        mock_modelo.prever.assert_called_once_with("adorei o servico")

        # Verifica que o resultado foi salvo no Redis com metadados corretos
        mock_guardar.assert_called_once()
        args, _ = mock_guardar.call_args
        self.assertEqual(args[0], "tarefa-teste-123")
        dados_salvos = args[1]
        self.assertEqual(dados_salvos["status"], "pronto")
        self.assertEqual(dados_salvos["sentimento"], "positivo")
        self.assertEqual(dados_salvos["confianca"], 0.992)
        self.assertIn("tempo_ms", dados_salvos)
        self.assertIsInstance(dados_salvos["tempo_ms"], float)

        # Verifica o retorno da função
        self.assertEqual(resultado["status"], "pronto")
        self.assertEqual(resultado["sentimento"], "positivo")

    @patch("app.fila.guardar_resultado")
    def test_processar_tarefa_propaga_erro(self, mock_guardar):
        mock_modelo = MagicMock()
        mock_modelo.prever.side_effect = RuntimeError("Falha no modelo de IA")

        tarefa = {
            "id": "tarefa-erro-456",
            "texto": "texto com falha",
        }

        with self.assertRaises(RuntimeError):
            processar_tarefa(tarefa, mock_modelo)

        # Não deve ter chamado guardar_resultado com sucesso
        mock_guardar.assert_not_called()


if __name__ == "__main__":
    unittest.main()
