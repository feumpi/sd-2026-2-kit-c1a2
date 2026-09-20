"""
Interface REST do servico de inferencia.

O QUE JA ESTA PRONTO:
  - carregamento do modelo UMA vez, na subida (nao a cada requisicao)
  - rota sincrona /predict-sync, usada no laboratorio da Aula 6

O QUE VOCE PRECISA FAZER (TAREFAS.md, itens 1 e 2):
  - POST /predict  -> colocar na fila e devolver o id
  - GET  /resultado/{id} -> devolver o resultado quando estiver pronto

Rodar:  uvicorn app.api_rest:app --reload --port 8000
Docs:   http://localhost:8000/docs
"""
import logging
import time

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from app import fila
from app.modelo import carregar_modelo

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger("rest")

app = FastAPI(title="Servico de Inferencia - C1.A2", version="0.1.0")

modelo = None


class Entrada(BaseModel):
    texto: str


class RespostaSubmissao(BaseModel):
    id: str
    status: str = "na_fila"


@app.middleware("http")
async def log_requisicoes(request: Request, call_next):
    inicio = time.time()
    resposta = await call_next(request)
    tempo_ms = round((time.time() - inicio) * 1000, 2)
    logger.info(f"{request.method} {request.url.path} status={resposta.status_code} tempo_ms={tempo_ms}")
    return resposta


@app.on_event("startup")
def _subir():
    """Carrega o modelo UMA vez. Este e o ponto-chave da Aula 6."""
    global modelo
    inicio = time.time()
    modelo = carregar_modelo()
    logger.info(f"[startup] modelo carregado em {time.time() - inicio:.3f}s")



@app.get("/saude")
def saude():
    return {"status": "ok", "modelo_carregado": modelo is not None}


@app.post("/predict-sync")
def predict_sync(entrada: Entrada):
    """Inferencia SINCRONA: o cliente espera a resposta. Lab da Aula 6."""
    if not entrada.texto.strip():
        raise HTTPException(status_code=400, detail="texto vazio")
    inicio = time.time()
    resultado = modelo.prever(entrada.texto)
    resultado["tempo_ms"] = round((time.time() - inicio) * 1000, 2)
    logger.info(
        f"predict-sync tamanho={len(entrada.texto)} sentimento={resultado['sentimento']} "
        f"confianca={resultado['confianca']} tempo_ms={resultado['tempo_ms']}"
    )
    return resultado


# ------------------------------------------------------------------
# TAREFA 1 - submissao assincrona
# ------------------------------------------------------------------
@app.post("/predict", status_code=202, response_model=RespostaSubmissao)
def predict(entrada: Entrada):
    """Deve enfileirar a tarefa e devolver {"id": ...} SEM esperar."""
    if not entrada.texto.strip():
        raise HTTPException(status_code=400, detail="texto vazio")

    inicio = time.time()
    tarefa_id = fila.enfileirar(entrada.texto)
    tempo_ms = round((time.time() - inicio) * 1000, 2)
    logger.info(f"POST /predict id={tarefa_id} tamanho={len(entrada.texto)} tempo_ms={tempo_ms}")
    return RespostaSubmissao(id=tarefa_id, status="na_fila")


# ------------------------------------------------------------------
# TAREFA 2 - consulta do resultado
# ------------------------------------------------------------------
@app.get("/resultado/{tarefa_id}")
def resultado(tarefa_id: str):
    """Deve devolver o resultado; 404 se o id nao existir."""
    inicio = time.time()
    dados = fila.buscar_resultado(tarefa_id)
    if dados is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    tempo_ms = round((time.time() - inicio) * 1000, 2)
    logger.info(f"GET /resultado/{tarefa_id} status={dados.get('status')} tempo_ms={tempo_ms}")
    return dados


