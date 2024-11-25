from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.pipeline import setup_pipeline
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import make_asgi_app


# Initialize FastAPI app
app = FastAPI()

# Setup Prometheus instrumentation for FastAPI
instrumentator = Instrumentator()
instrumentator.add(app)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Initialize the Retrieval QA pipeline
try:
    rag_pipeline = setup_pipeline()
except Exception as e:
    raise RuntimeError(f"Error initializing pipeline: {e}")


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    result: str


@app.post("/query", response_model=QueryResponse)
def query_system(request: QueryRequest):
    """
    Endpoint to query the Retrieval QA pipeline.
    """
    try:
        result = rag_pipeline.invoke(request.question)
        return QueryResponse(result=result['result'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

