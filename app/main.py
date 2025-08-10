from loguru import logger
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import httpx
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from app.config import Settings
from app.services.tft_api_fetcher.router import fetch_router

settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Do Setup and cleanup for the FastAPI app.

    Creates a shared httpx.AsyncClient for making async HTTP requests,
    and closes it on shutdown.

    Args:
    ----
        app (FastAPI): The FastAPI app instance.

    Yields:
    ------
        None

    """
    app.request_client = httpx.AsyncClient()  # type: ignore[attr-defined]
    FastAPICache.init(InMemoryBackend())

    yield

    await app.request_client.aclose()  # type: ignore[attr-defined]


app = FastAPI(lifespan=lifespan)

# Add routers
app.include_router(fetch_router)

origins = [
    "*",
    "http://localhost",
    "http://localhost:8080",
]


@app.get("/health")
def health():
    try:
        logger.info("OK: Everything is OK")
        return "ok"
    except Exception as e:
        logger.error(e)
        return e


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
