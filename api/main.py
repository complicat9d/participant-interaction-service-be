import uvicorn
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, APIRouter, Response, status, Query
from contextlib import asynccontextmanager
from typing import List, Optional
from datetime import datetime

from database.session import session_dep
from utils.db.client import get_clients_filtered
from schemas import ClientSchema, Gender, SortType

from api.client import client_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return


@app.exception_handler(Exception)
async def debug_exception_handler(exc: Exception):
    import traceback

    return Response(
        content="".join(
            traceback.format_exception(type(exc), value=exc, tb=exc.__traceback__)
        )
    )


router = APIRouter(prefix="/api")


@router.get(
    "/list",
    response_model=Optional[List[ClientSchema]],
    description="**Input format for from_date and until_date: YYYY-MM-DDTHH:MM:SS (e.g 2024-11-01T10:56:02)**",
)
async def list_clients(
    session: session_dep,
    gender: Optional[Gender] = Query(None),
    first_name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    from_date: Optional[datetime] = Query(None),
    until_date: Optional[datetime] = Query(None),
    sort_by_date: Optional[SortType] = Query(None),
):
    return await get_clients_filtered(
        session, first_name, last_name, gender, from_date, until_date, sort_by_date
    )


router.include_router(client_router, prefix="/clients")
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
