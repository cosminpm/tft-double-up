import asyncio
import hashlib
import json
from typing import TYPE_CHECKING

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache
from starlette import status
from starlette.requests import Request

from app.config import Settings
from app.services.tft_api_fetcher.fetch_best_pairs import generate_best_pairs
from app.services.tft_api_fetcher.fetch_champion_weapon_images import fetch_champion_weapon_images

if TYPE_CHECKING:
    from httpx import AsyncClient, Response

settings = Settings()
fetch_router: APIRouter = APIRouter(tags=["Fetch"])


@fetch_router.get("/best_pairs")
@cache(expire=86400) if not settings.debug else (lambda f: f)
async def get_best_pairs(request: Request) -> JSONResponse:
    """Retrieve and return the best composition pairings from the TFT tier list.

    Args:
    ----
        request: FastAPI request object containing the shared HTTP client.

    Returns:
    -------
        Dict of composition name to composition data with paired composition names.

    """
    request_client: AsyncClient = request.app.request_client

    serializable_pairs: dict[str, dict] = await generate_best_pairs(client=request_client)
    content_bytes = json.dumps(serializable_pairs).encode("utf-8")
    etag = hashlib.md5(content_bytes).hexdigest()

    if request.headers.get("if-none-match") == etag:
        return JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED, content=None)
    return JSONResponse(content=serializable_pairs, headers={"ETag": etag})


@fetch_router.get("/champion_weapon_images")
@cache(expire=86400)
async def get_champion_weapon_images(request: Request) -> JSONResponse:
    """Fetch champion weapon image URLs from the TFT tier list endpoint.

    Args:
    ----
        request: FastAPI request object containing the shared HTTP client.

    Returns:
    -------
        Mapping of champion names to their weapon image URLs.

    """
    request_client: AsyncClient = request.app.request_client
    champion_images: dict[str, str] = await fetch_champion_weapon_images(request_client)

    content_bytes = json.dumps(champion_images).encode("utf-8")
    etag = hashlib.md5(content_bytes).hexdigest()

    if request.headers.get("if-none-match") == etag:
        return JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED, content=None)

    return JSONResponse(content=champion_images, headers={"ETag": etag})
