from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import httpx
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from loguru import logger

from app.config import Settings
from app.services.tft_api_fetcher.router import fetch_router
from app.utils.logger_config import configure_logging

settings = Settings()


if settings.is_sentry:
    import sentry_sdk

    sentry_sdk.init(
        dsn="https://0c9a7785d72172b768c679be0b185d10@o4507929979912192.ingest.de.sentry.io/4509826174419024",
        traces_sample_rate=1.0,
        _experiments={
            "continuous_profiling_auto_start": True,
        },
    )


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
    configure_logging()
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
    """Health check."""
    try:
        logger.info("OK: Everything is OK")
        return "ok"  # noqa: TRY300
    except Exception as e:  # noqa: BLE001
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
    uvicorn.run(app, host=settings.host, port=settings.port)  # noqa: S104
