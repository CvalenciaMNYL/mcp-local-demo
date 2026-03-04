from fastapi import FastAPI
from pathlib import Path

app = FastAPI()

ALLOWED_BASE = Path("./docs").resolve()

def safe_path(p: str) -> Path:
    candidate = (ALLOWED_BASE / p).resolve()
    if ALLOWED_BASE not in candidate.parents and candidate != ALLOWED_BASE:
        raise ValueError("Ruta no permitida")
    return candidate

@app.post("/read-documents")
def read_documents(path1: str, path2: str):
    try:
        f1 = safe_path(path1)
        f2 = safe_path(path2)

        if not f1.exists() or not f2.exists():
            return {"status": "error", "message": "Archivo no existe"}

        return {
            "status": "success",
            "files": [
                {"path": str(f1), "content": f1.read_text()},
                {"path": str(f2), "content": f2.read_text()}
            ]
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}