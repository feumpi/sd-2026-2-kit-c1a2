"""
Testes automatizados para a Tarefa 1: Submissão Assíncrona (POST /predict)
"""
import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

# Mock modelo antes de importar api_rest para evitar treino pesado no teste
with patch("app.modelo.carregar_modelo") as mock_carregar:
    mock_modelo = MagicMock()
    mock_carregar.return_value = mock_modelo
    from app.api_rest import app


class TestTarefa1(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    @patch("app.fila.enfileirar")
    def test_predict_assincrono_sucesso(self, mock_enfileirar):
        mock_enfileirar.return_value = "fake-uuid-1234"

        resposta = self.client.post("/predict", json={"texto": "atendimento excelente"})

        # Deve retornar HTTP 202 Accepted
        self.assertEqual(resposta.status_code, 202)
        dados = resposta.json()
        self.assertEqual(dados["id"], "fake-uuid-1234")
        self.assertEqual(dados["status"], "na_fila")

        # Verifica que o enfileirar foi chamado com o texto correto
        mock_enfileirar.assert_called_once_with("atendimento excelente")

    def test_predict_texto_vazio(self):
        # Texto vazio deve retornar 400 Bad Request
        resposta = self.client.post("/predict", json={"texto": ""})
        self.assertEqual(resposta.status_code, 400)
        self.assertIn("texto vazio", resposta.json()["detail"])

        # Texto apenas com espaços deve retornar 400 Bad Request
        resposta_espacos = self.client.post("/predict", json={"texto": "    "})
        self.assertEqual(resposta_espacos.status_code, 400)
        self.assertIn("texto vazio", resposta_espacos.json()["detail"])

    @patch("app.fila.enfileirar")
    def test_invariante_modelo_nao_chamado(self, mock_enfileirar):
        # Garante que modelo.prever JAMAIS seja chamado na rota POST /predict
        mock_enfileirar.return_value = "fake-uuid-5678"
        from app import api_rest
        mock_modelo_instancia = MagicMock()
        api_rest.modelo = mock_modelo_instancia

        self.client.post("/predict", json={"texto": "mensagem para teste"})
        mock_modelo_instancia.prever.assert_not_called()



if __name__ == "__main__":
    unittest.main()
