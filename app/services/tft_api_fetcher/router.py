from fastapi import APIRouter
from starlette.requests import Request

fetch_router: APIRouter = APIRouter(tags=["Fetch"])


@fetch_router.get("/get_tft_top_compositions")
async def get_tft_top_compositions(request: Request) -> list:
    return []
