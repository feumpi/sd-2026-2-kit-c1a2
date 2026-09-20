"""
Testes automatizados para a Tarefa 5: Resiliência, Retentativas e Dead-Letter Queue
"""
import json
import unittest
from unittest.mock import MagicMock, patch

from app import fila
from app.worker import tratar_falha


class TestTarefa5(unittest.TestCase):

    @patch("app.fila.reenfileirar")
    @patch("app.fila.enfileirar_dead_letter")
    def test_tratar_falha_retentativa_tentativa_1(self, mock_dead_letter, mock_reenfileirar):
        tarefa = {"id": "tarefa-1", "texto": "texto com erro", "tentativas": 1}
        erro = ValueError("Erro temporário")

        tratar_falha(tarefa, erro)

        # Deve incrementar para 2 e reenfileirar
        self.assertEqual(tarefa["tentativas"], 2)
        mock_reenfileirar.assert_called_once_with(tarefa)
        mock_dead_letter.assert_not_called()

    @patch("app.fila.reenfileirar")
    @patch("app.fila.enfileirar_dead_letter")
    def test_tratar_falha_retentativa_tentativa_2(self, mock_dead_letter, mock_reenfileirar):
        tarefa = {"id": "tarefa-2", "texto": "texto com erro", "tentativas": 2}
        erro = TimeoutError("Timeout transitório")

        tratar_falha(tarefa, erro)

        # Deve incrementar para 3 e reenfileirar
        self.assertEqual(tarefa["tentativas"], 3)
        mock_reenfileirar.assert_called_once_with(tarefa)
        mock_dead_letter.assert_not_called()

    @patch("app.fila.reenfileirar")
    @patch("app.fila.enfileirar_dead_letter")
    def test_tratar_falha_envio_dead_letter_na_3a_tentativa(self, mock_dead_letter, mock_reenfileirar):
        tarefa = {"id": "tarefa-3", "texto": "poison pill", "tentativas": 3}
        erro = RuntimeError("Erro irrecuperável")

        tratar_falha(tarefa, erro)

        # Não deve reenfileirar na fila principal
        mock_reenfileirar.assert_not_called()
        # Deve enviar para dead-letter
        mock_dead_letter.assert_called_once_with(tarefa, "Erro irrecuperável")

    @patch("app.fila.cliente")
    def test_fila_reenfileirar_redis(self, mock_cliente_func):
        mock_redis = MagicMock()
        mock_cliente_func.return_value = mock_redis

        tarefa = {"id": "id-retry", "texto": "frase", "tentativas": 2}
        fila.reenfileirar(tarefa)

        # Verifica push na fila principal
        mock_redis.rpush.assert_called_once()
        args_rpush = mock_redis.rpush.call_args[0]
        self.assertEqual(args_rpush[0], "tarefas")
        self.assertIn("id-retry", args_rpush[1])

        # Verifica atualização do status para 'retentando'
        mock_redis.set.assert_called_once()
        chave, valor = mock_redis.set.call_args[0]
        self.assertEqual(chave, "resultado:id-retry")
        dados = json.loads(valor)
        self.assertEqual(dados["status"], "retentando")
        self.assertEqual(dados["tentativas"], 2)

    @patch("app.fila.cliente")
    def test_fila_enfileirar_dead_letter_redis(self, mock_cliente_func):
        mock_redis = MagicMock()
        mock_cliente_func.return_value = mock_redis

        tarefa = {"id": "id-dead", "texto": "frase", "tentativas": 3}
        fila.enfileirar_dead_letter(tarefa, "Falha fatal de execução")

        # Verifica envio para a fila de descarte
        mock_redis.rpush.assert_called_once()
        args_rpush = mock_redis.rpush.call_args[0]
        self.assertEqual(args_rpush[0], "tarefas:dead_letter")
        dados_dl = json.loads(args_rpush[1])
        self.assertEqual(dados_dl["tarefa"]["id"], "id-dead")
        self.assertEqual(dados_dl["erro"], "Falha fatal de execução")
        self.assertIn("timestamp", dados_dl)

        # Verifica persistência do status final 'erro'
        mock_redis.set.assert_called_once()
        chave, valor = mock_redis.set.call_args[0]
        self.assertEqual(chave, "resultado:id-dead")
        dados_res = json.loads(valor)
        self.assertEqual(dados_res["status"], "erro")
        self.assertEqual(dados_res["detalhes"], "Falha fatal de execução")
        self.assertEqual(dados_res["tentativas"], 3)


if __name__ == "__main__":
    unittest.main()
