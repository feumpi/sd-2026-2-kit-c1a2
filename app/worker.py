"""
Worker: consome a fila e executa a inferencia.

O QUE JA ESTA PRONTO: o laco principal e o carregamento do modelo.
O QUE VOCE PRECISA FAZER (TAREFAS.md, itens 3 e 5):
  - guardar o resultado ao terminar
  - tratar erro com retentativa e fila de descarte (dead-letter)

Rodar:  python -m app.worker
Suba mais de um worker em terminais diferentes e veja a carga se dividir.
"""
import time

from app import fila
from app.modelo import carregar_modelo


def processar_tarefa(tarefa: dict, modelo) -> dict:
    """Executa a inferência de uma tarefa e persiste o resultado pronto no Redis."""
    inicio = time.time()
    resultado = modelo.prever(tarefa["texto"])
    resultado["status"] = "pronto"
    resultado["tempo_ms"] = round((time.time() - inicio) * 1000, 2)

    fila.guardar_resultado(tarefa["id"], resultado)
    print(
        f"[worker] concluido {tarefa['id']} sentimento={resultado['sentimento']} "
        f"confianca={resultado['confianca']} tempo_ms={resultado['tempo_ms']}"
    )
    return resultado


def tratar_falha(tarefa: dict, erro: Exception) -> None:
    """Aplica política de retentativa e encaminhamento para dead-letter."""
    tentativa_atual = tarefa.get("tentativas", 1)

    if tentativa_atual < fila.MAX_TENTATIVAS:
        tarefa["tentativas"] = tentativa_atual + 1
        print(
            f"[worker] AVISO: falha ao processar {tarefa.get('id')} "
            f"(tentativa {tentativa_atual}/{fila.MAX_TENTATIVAS}): {erro}. Reenfileirando..."
        )
        fila.reenfileirar(tarefa)
    else:
        print(
            f"[worker] ERRO CRÍTICO: tarefa {tarefa.get('id')} atingiu o limite de "
            f"{fila.MAX_TENTATIVAS} tentativas. Despachando para dead-letter: {erro}"
        )
        fila.enfileirar_dead_letter(tarefa, str(erro))


def main():
    print("[worker] carregando modelo...")
    modelo = carregar_modelo()
    print("[worker] pronto. aguardando tarefas (Ctrl+C para sair)")

    while True:
        tarefa = fila.proxima_tarefa(timeout=5)
        if tarefa is None:
            continue

        print(f"[worker] processando {tarefa['id']}")
        try:
            processar_tarefa(tarefa, modelo)
        except Exception as erro:  # noqa: BLE001
            tratar_falha(tarefa, erro)


if __name__ == "__main__":
    main()
