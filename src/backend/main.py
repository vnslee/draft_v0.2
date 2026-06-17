from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from db.connection import close_db, init_db
from routers import analysis, countries, reports, settings as settings_router
from ws.progress import ws_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(title="오토금융 해외진출 진단 API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(countries.router, prefix="/countries", tags=["countries"])
app.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])
app.include_router(settings_router.router, prefix="/settings", tags=["settings"])
app.include_router(ws_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
