from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from app.core.config import settings
from app.core.database import init_db
from app.core.logging_config import configure_logging
from app.routers import auth_router, user_router, welfare_router, rental_router, savings_loan_router, financial_router, mpesa_router

configure_logging()

origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]
app = FastAPI(
    title="Boda Boda Chama API",
    description="Backend for Boda Boda Riders Self-Help Group",
    version="1.0.0"
)

if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

@app.on_event("startup")
async def startup_event():
    await init_db()
    logger.info("Database connected successfully")

@app.get("/")
async def root():
    return {"status": "ok", "message": "Boda Boda Chama API is running"}

# Include routers
app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(user_router.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(welfare_router.router, prefix="/api/v1/welfare", tags=["Welfare"])
app.include_router(rental_router.router, prefix="/api/v1/rentals", tags=["Rentals"])
app.include_router(savings_loan_router.router, prefix="/api/v1/loans", tags=["Loans & Savings"])
app.include_router(financial_router.router, prefix="/api/v1/financials", tags=["Financials"])
app.include_router(mpesa_router.router, prefix="/api/v1/mpesa", tags=["M-Pesa"])