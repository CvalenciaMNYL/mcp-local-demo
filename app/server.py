from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Document Reader", json_response=True)

# Carpeta permitida (ajusta si quieres)
ALLOWED_BASE = (Path(__file__).resolve().parent.parent / "docs").resolve()

def _safe_path(p: str) -> Path:
    """Permite solo rutas dentro de ./docs evitando path traversal."""
    candidate = Path(p)
    if not candidate.is_absolute():
        candidate = (ALLOWED_BASE / candidate).resolve()
    else:
        candidate = candidate.resolve()

    if ALLOWED_BASE not in candidate.parents and candidate != ALLOWED_BASE:
        raise ValueError(f"Ruta no permitida (fuera de {ALLOWED_BASE}).")

    return candidate

@mcp.tool()
def read_two_paths(path1: str, path2: str) -> dict:
    """
    Lee 2 archivos dentro de ./docs y devuelve su contenido en JSON.
    """
    try:
        f1 = _safe_path(path1)
        f2 = _safe_path(path2)

        if not f1.exists() or not f1.is_file():
            return {"status": "error", "message": f"No existe o no es archivo: {str(f1)}"}
        if not f2.exists() or not f2.is_file():
            return {"status": "error", "message": f"No existe o no es archivo: {str(f2)}"}

        return {
            "status": "success",
            "files": [
                {"path": str(f1), "content": f1.read_text(encoding="utf-8", errors="replace")},
                {"path": str(f2), "content": f2.read_text(encoding="utf-8", errors="replace")},
            ],
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Levanta el server por HTTP en localhost:8000 (endpoint /mcp)
    mcp.run(transport="streamable-http")