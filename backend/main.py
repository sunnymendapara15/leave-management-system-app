from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app import crud
from backend.app.database import Base, SessionLocal, engine
from backend.app.routers import auth, entitlements, leave_requests, leave_types

app = FastAPI(title="Leave Management API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(leave_types.router)
app.include_router(leave_requests.router)
app.include_router(entitlements.router)


@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    try:
        crud.seed_default_leave_types(db)
    finally:
        db.close()
