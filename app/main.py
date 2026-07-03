from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from app.core.database import init_db
from app.routers import auth_router, user_router, welfare_router, rental_router, savings_loan_router, financial_router, mpesa_router

app = FastAPI(
    title="Boda Boda Chama API",
    description="Backend for Boda Boda Riders Self-Help Group",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
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