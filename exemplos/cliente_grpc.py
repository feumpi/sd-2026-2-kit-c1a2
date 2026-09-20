"""
Cliente gRPC de exemplo para chamadas síncronas individual e em lote.
Rode com o servidor gRPC no ar: python -m app.servidor_grpc
"""
import sys
import grpc

try:
    import inferencia_pb2
    import inferencia_pb2_grpc
except ImportError:
    raise SystemExit(
        "Stubs nao encontrados. Rode antes:\n"
        "  python -m grpc_tools.protoc -I proto --python_out=. --grpc_python_out=. proto/inferencia.proto"
    )

ENDERECO = "localhost:50051"


def prever_unico(stub, texto: str):
    resposta = stub.Prever(inferencia_pb2.PedidoPrever(texto=texto))
    print(f"[grpc] Prever: texto='{resposta.texto}' | sentimento={resposta.sentimento} | confianca={resposta.confianca}")
    return resposta


def prever_lote(stub, textos: list):
    resposta = stub.PreverLote(inferencia_pb2.PedidoLote(textos=textos))
    print(f"[grpc] PreverLote ({len(resposta.resultados)} itens processados):")
    for r in resposta.resultados:
        print(f"  -> texto='{r.texto}' | sentimento={r.sentimento} | confianca={r.confianca}")
    return resposta


if __name__ == "__main__":
    canal = grpc.insecure_channel(ENDERECO)
    stub = inferencia_pb2_grpc.InferenciaStub(canal)

    texto = " ".join(sys.argv[1:]) or "o atendimento foi muito bom"
    print("=== Teste Chamada Individual (Prever) ===")
    prever_unico(stub, texto)

    print("\n=== Teste Chamada em Lote (PreverLote) ===")
    lote = [
        "adorei o produto, recomendo demais",
        "pessimo atendimento, ninguem resolve nada",
        "entrega super rapida e bem embalada",
    ]
    prever_lote(stub, lote)
