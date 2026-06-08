import os
import uvicorn
from app import app

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    log_level = os.getenv("LOG_LEVEL", "info")
    reload = os.getenv("ENVIRONMENT", "development") == "development"

    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=reload,
    )
