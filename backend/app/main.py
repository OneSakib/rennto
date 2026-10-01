from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.api import auth, tenants, plans, rents, dashboard, history

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rennto API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(tenants.router, prefix="/api/v1/tenants", tags=["Tenants"])
app.include_router(plans.router, prefix="/api/v1/plans", tags=["Plans"])
app.include_router(rents.router, prefix="/api/v1/rents", tags=["Rents"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])
app.include_router(history.router, prefix="/api/v1/history", tags=["History"])

@app.get("/health")
def health():
    return {"status": "ok", "app": "rennto"}
