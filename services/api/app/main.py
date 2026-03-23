from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.api.app.api.routes.health import router as health_router
from services.api.app.api.routes.auth import router as auth_router
from services.api.app.api.routes.ops import router as ops_router
from services.api.app.api.routes.projects import router as projects_router
from services.api.app.api.routes.properties import router as properties_router
from services.api.app.api.routes.reports import router as reports_router
from services.api.app.api.routes.visits import router as visits_router
from services.api.app.core.config import settings


app = FastAPI(
    title="Imjang Companion API",
    description="Backend service for real-estate field visit workflows.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(ops_router)
app.include_router(projects_router)
app.include_router(properties_router)
app.include_router(visits_router)
app.include_router(reports_router)
