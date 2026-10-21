from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Header
from module_1.config import get_settings
from module_4.workflow_graph import ask
from module_2.vectorstore import add_documents
from module_2.ingestion import load_file, chunk_documents, SUPPORTED
from module_2.audit import write_audit
from module_1.models import ChatRequest, ChatResponse, IngestResponse

router = APIRouter(prefix="/api")
settings = get_settings()


@router.get("/health")
def health():
    return {"status": "ok", "service": settings.app_name}


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    try:
        result = ask(payload.question)
        write_audit(payload.question, result["source_used"], result.get("trace", []))

        return ChatResponse(
            answer=result["answer"],
            source_used=result["source_used"],
            trace=result.get("trace", []),
            citations=result.get("citations", []),
            rewritten_query=result.get("current_query", payload.question),
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/ingest", response_model=IngestResponse)
async def ingest(file: UploadFile = File(...), x_admin_key: str = Header(default="")):
    if x_admin_key != settings.admin_api_key:
        raise HTTPException(status_code=401, detail="Invalid admin key")
    suffix = Path(file.filename or "").suffix.lower()
     