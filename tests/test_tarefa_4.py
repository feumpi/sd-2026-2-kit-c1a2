"""
Testes automatizados para a Tarefa 4: Interface gRPC (Prever e PreverLote) e Paridade com REST
"""
import unittest
from unittest.mock import MagicMock

import inferencia_pb2
from app.servidor_grpc import ServicoInferencia


class TestTarefa4(unittest.TestCase):

    def setUp(self):
        self.servico = ServicoInferencia.__new__(ServicoInferencia)
        self.mock_modelo = MagicMock()
        self.servico.modelo = self.mock_modelo

    def test_prever_individual(self):
        self.mock_modelo.prever.return_value = {
            "texto": "atendimento excelente",
            "sentimento": "positivo",
            "confianca": 0.995,
        }

        pedido = inferencia_pb2.PedidoPrever(texto="atendimento excelente")
        resposta = self.servico.Prever(pedido, None)

        self.mock_modelo.prever.assert_called_once_with("atendimento excelente")
        self.assertEqual(resposta.texto, "atendimento excelente")
        self.assertEqual(resposta.sentimento, "positivo")
        self.assertEqual(resposta.confianca, 0.995)

    def test_prever_lote(self):
        def mock_prever_side_effect(texto):
            if "bom" in texto:
                return {"texto": texto, "sentimento": "positivo", "confianca": 0.98}
            return {"texto": texto, "sentimento": "negativo", "confianca": 0.95}

        self.mock_modelo.prever.side_effect = mock_prever_side_effect

        pedido = inferencia_pb2.PedidoLote(
            textos=["o servico foi bom", "produto ruim nao gostei"]
        )
        resposta = self.servico.PreverLote(pedido, None)

        self.assertEqual(len(resposta.resultados), 2)
        self.assertEqual(resposta.resultados[0].texto, "o servico foi bom")
        self.assertEqual(resposta.resultados[0].sentimento, "positivo")
        self.assertEqual(resposta.resultados[0].confianca, 0.98)

        self.assertEqual(resposta.resultados[1].texto, "produto ruim nao gostei")
        self.assertEqual(resposta.resultados[1].sentimento, "negativo")
        self.assertEqual(resposta.resultados[1].confianca, 0.95)

    def test_prever_lote_vazio(self):
        pedido = inferencia_pb2.PedidoLote(textos=[])
        resposta = self.servico.PreverLote(pedido, None)

        self.assertEqual(len(resposta.resultados), 0)
        self.mock_modelo.prever.assert_not_called()

    def test_paridade_estrita_grpc_e_rest(self):
        # Testa com o modelo real para assegurar paridade estrita
        from app.modelo import carregar_modelo
        from app import api_rest
        from fastapi.testclient import TestClient

        modelo_real = carregar_modelo()
        self.servico.modelo = modelo_real
        api_rest.modelo = modelo_real
        client_rest = TestClient(api_rest.app)

        frases_teste = [
            "o atendimento foi excelente e muito rapido",
            "pessimo atendimento, ninguem resolve nada",
            "produto quebrou no primeiro dia de uso",
            "melhor compra que fiz esse ano",
        ]

        for frase in frases_teste:
            # Predição gRPC
            pedido_grpc = inferencia_pb2.PedidoPrever(texto=frase)
            resposta_grpc = self.servico.Prever(pedido_grpc, None)

            # Predição REST
            resposta_rest = client_rest.post("/predict-sync", json={"texto": frase})
            self.assertEqual(resposta_rest.status_code, 200)
            dados_rest = resposta_rest.json()

            # Validação de paridade estrita
            self.assertEqual(
                resposta_grpc.sentimento,
                dados_rest["sentimento"],
                f"Divergência de sentimento na frase: {frase}"
            )
            self.assertEqual(
                resposta_grpc.confianca,
                dados_rest["confianca"],
                f"Divergência de confiança na frase: {frase}"
            )


if __name__ == "__main__":
    unittest.main()
