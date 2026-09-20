"""
Interface gRPC do servico de inferencia.

PRE-REQUISITO: gerar os stubs antes de rodar (veja scripts/gerar_stubs).

O QUE JA ESTA PRONTO: o metodo Prever.
O QUE VOCE PRECISA FAZER (TAREFAS.md, item 4): o metodo PreverLote.

Rodar:  python -m app.servidor_grpc
"""
import logging
import time
from concurrent import futures

import grpc

from app.modelo import carregar_modelo

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger("grpc")

try:
    import inferencia_pb2
    import inferencia_pb2_grpc
except ImportError:  # pragma: no cover
    raise SystemExit(
        "Stubs nao encontrados. Rode antes:\n"
        "  python -m grpc_tools.protoc -I proto --python_out=. "
        "--grpc_python_out=. proto/inferencia.proto"
    )


class ServicoInferencia(inferencia_pb2_grpc.InferenciaServicer):

    def __init__(self):
        logger.info("carregando modelo...")
        self.modelo = carregar_modelo()
        logger.info("modelo pronto")

    def Prever(self, request, context):
        inicio = time.time()
        r = self.modelo.prever(request.texto)
        tempo_ms = round((time.time() - inicio) * 1000, 2)
        logger.info(f"Prever tamanho={len(request.texto)} sentimento={r['sentimento']} tempo_ms={tempo_ms}")
        return inferencia_pb2.RespostaPrever(
            texto=r["texto"], sentimento=r["sentimento"], confianca=r["confianca"]
        )

    def PreverLote(self, request, context):
        """Processa multiplas inferencias em uma unica requisicao gRPC."""
        inicio = time.time()
        respostas = []
        for t in request.textos:
            r = self.modelo.prever(t)
            respostas.append(
                inferencia_pb2.RespostaPrever(
                    texto=r["texto"],
                    sentimento=r["sentimento"],
                    confianca=r["confianca"],
                )
            )
        tempo_ms = round((time.time() - inicio) * 1000, 2)
        logger.info(f"PreverLote itens={len(request.textos)} tempo_ms={tempo_ms}")
        return inferencia_pb2.RespostaLote(resultados=respostas)


def servir(porta: int = 50051):
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inferencia_pb2_grpc.add_InferenciaServicer_to_server(
        ServicoInferencia(), servidor)
    servidor.add_insecure_port(f"[::]:{porta}")
    servidor.start()
    logger.info(f"escutando na porta {porta}")
    servidor.wait_for_termination()


if __name__ == "__main__":
    servir()
