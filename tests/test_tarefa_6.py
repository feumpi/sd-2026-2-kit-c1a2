"""
Testes automatizados para a Tarefa 6: Observabilidade e Log Estruturado de Requisições
"""
import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
import inferencia_pb2


class TestTarefa6(unittest.TestCase):

    def setUp(self):
        with patch("app.modelo.carregar_modelo"):
            from app.api_rest import app
            self.client = TestClient(app)

    @patch("app.fila.enfileirar")
    def test_log_requisicao_rest_predict(self, mock_enfileirar):
        mock_enfileirar.return_value = "fake-uuid-log-1"

        with self.assertLogs("rest", level="INFO") as cm:
            resposta = self.client.post("/predict", json={"texto": "teste de observabilidade"})
            self.assertEqual(resposta.status_code, 202)

        # Deve conter registro da rota e da aplicação
        logs = " ".join(cm.output)
        self.assertIn("fake-uuid-log-1", logs)
        self.assertIn("POST", logs)
        self.assertIn("tempo_ms=", logs)

    @patch("app.fila.buscar_resultado")
    def test_log_requisicao_rest_resultado(self, mock_buscar):
        mock_buscar.return_value = {"status": "pronto", "sentimento": "positivo"}

        with self.assertLogs("rest", level="INFO") as cm:
            resposta = self.client.get("/resultado/fake-uuid-log-2")
            self.assertEqual(resposta.status_code, 200)

        logs = " ".join(cm.output)
        self.assertIn("GET /resultado/fake-uuid-log-2", logs)
        self.assertIn("tempo_ms=", logs)

    @patch("app.fila.guardar_resultado")
    def test_log_worker_processar_tarefa(self, mock_guardar):
        from app.worker import processar_tarefa

        mock_modelo = MagicMock()
        mock_modelo.prever.return_value = {
            "texto": "texto worker log",
            "sentimento": "positivo",
            "confianca": 0.99,
        }

        tarefa = {"id": "tarefa-log-worker", "texto": "texto worker log"}

        with self.assertLogs("worker", level="INFO") as cm:
            processar_tarefa(tarefa, mock_modelo)

        logs = " ".join(cm.output)
        self.assertIn("concluido tarefa-log-worker", logs)
        self.assertIn("tempo_ms=", logs)

    @patch("app.fila.reenfileirar")
    def test_log_worker_retentativa_warning(self, mock_reenfileirar):
        from app.worker import tratar_falha

        tarefa = {"id": "tarefa-log-retry", "texto": "texto", "tentativas": 1}

        with self.assertLogs("worker", level="WARNING") as cm:
            tratar_falha(tarefa, RuntimeError("Falha teste"))

        logs = " ".join(cm.output)
        self.assertIn("WARNING:worker:falha ao processar tarefa-log-retry", logs)
        self.assertIn("Reenfileirando", logs)

    @patch("app.fila.enfileirar_dead_letter")
    def test_log_worker_dead_letter_error(self, mock_dead_letter):
        from app.worker import tratar_falha

        tarefa = {"id": "tarefa-log-dead", "texto": "texto", "tentativas": 3}

        with self.assertLogs("worker", level="ERROR") as cm:
            tratar_falha(tarefa, RuntimeError("Falha fatal"))

        logs = " ".join(cm.output)
        self.assertIn("ERROR:worker:tarefa tarefa-log-dead atingiu o limite", logs)
        self.assertIn("Despachando para dead-letter", logs)

    def test_log_grpc_prever_e_prever_lote(self):
        from app.servidor_grpc import ServicoInferencia

        servico = ServicoInferencia.__new__(ServicoInferencia)
        mock_modelo = MagicMock()
        mock_modelo.prever.return_value = {
            "texto": "frase log grpc",
            "sentimento": "positivo",
            "confianca": 0.98,
        }
        servico.modelo = mock_modelo

        with self.assertLogs("grpc", level="INFO") as cm:
            servico.Prever(inferencia_pb2.PedidoPrever(texto="frase log grpc"), None)
            servico.PreverLote(inferencia_pb2.PedidoLote(textos=["frase 1", "frase 2"]), None)

        logs = " ".join(cm.output)
        self.assertIn("Prever tamanho=", logs)
        self.assertIn("PreverLote itens=2", logs)
        self.assertIn("tempo_ms=", logs)


if __name__ == "__main__":
    unittest.main()
