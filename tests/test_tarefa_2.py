"""
Testes automatizados para a Tarefa 2: Consulta de Resultado (GET /resultado/{tarefa_id})
"""
import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

# Mock modelo antes de importar api_rest
with patch("app.modelo.carregar_modelo") as mock_carregar:
    mock_modelo = MagicMock()
    mock_carregar.return_value = mock_modelo
    from app.api_rest import app


class TestTarefa2(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    @patch("app.fila.buscar_resultado")
    def test_resultado_nao_encontrado_404(self, mock_buscar):
        # Quando a tarefa não existe no Redis, deve retornar 404
        mock_buscar.return_value = None

        resposta = self.client.get("/resultado/id-inexistente-123")
        self.assertEqual(resposta.status_code, 404)
        self.assertEqual(resposta.json()["detail"], "Tarefa não encontrada")
        mock_buscar.assert_called_once_with("id-inexistente-123")

    @patch("app.fila.buscar_resultado")
    def test_resultado_na_fila_200(self, mock_buscar):
        # Quando a tarefa ainda está na fila
        mock_buscar.return_value = {"status": "na_fila"}

        resposta = self.client.get("/resultado/id-pendente-456")
        self.assertEqual(resposta.status_code, 200)
        dados = resposta.json()
        self.assertEqual(dados["status"], "na_fila")

    @patch("app.fila.buscar_resultado")
    def test_resultado_pronto_200(self, mock_buscar):
        # Quando a tarefa foi concluída pelo worker
        mock_buscar.return_value = {
            "texto": "atendimento excelente",
            "sentimento": "positivo",
            "confianca": 0.9876,
            "status": "pronto",
            "tempo_ms": 12.34,
        }

        resposta = self.client.get("/resultado/id-concluido-789")
        self.assertEqual(resposta.status_code, 200)
        dados = resposta.json()
        self.assertEqual(dados["status"], "pronto")
        self.assertEqual(dados["sentimento"], "positivo")
        self.assertEqual(dados["confianca"], 0.9876)
        self.assertEqual(dados["texto"], "atendimento excelente")

    @patch("app.fila.buscar_resultado")
    def test_resultado_erro_200(self, mock_buscar):
        # Quando a tarefa falhou e foi para dead-letter
        mock_buscar.return_value = {
            "status": "erro",
            "detalhes": "falha simulada no processamento",
        }

        resposta = self.client.get("/resultado/id-erro-999")
        self.assertEqual(resposta.status_code, 200)
        dados = resposta.json()
        self.assertEqual(dados["status"], "erro")
        self.assertEqual(dados["detalhes"], "falha simulada no processamento")


if __name__ == "__main__":
    unittest.main()
