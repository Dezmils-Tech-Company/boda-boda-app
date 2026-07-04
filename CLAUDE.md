# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

**Running the Application:**
```bash
# Start the development server
python run.py

# Access Swagger UI at http://localhost:8000/docs
# Access ReDoc at http://localhost:8000/redoc
```

**Environment Setup:**
1. Create a `.env` file based on `.env.example`
2. Required variables: `MONGO_URI`, `SECRET_KEY` (for JWT)
3. Optional variables for Twilio SMS: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM_PHONE`
4. Optional variables for M-Pesa: `MPESA_CONSUMER_KEY`, `MPESA_CONSUMER_SECRET`, `MPESA_SHORTCODE`, `MPESA_PASSKEY`, `MPESA_CALLBACK_URL`

**Testing:**
- Test files are located in the `tests/` directory with `unit/` and `integration/` subdirectories
- Run tests with: `pytest`
- Run a specific test: `pytest tests/unit/test_filename.py::test_function_name`

**Code Quality:**
- Formatting: `black .`
- Import sorting: `isort .`
- Type checking: `mypy .`
- Linting would typically be added via flake8 or similar

## Codebase Architecture

**High-Level Structure:**
- **Entry Point**: `run.py` -> `app.main:app` (FastAPI instance)
- **Configuration**: `app/core/config.py` (Pydantic settings with environment variable loading)
- **Database**: `app/core/database.py` (MongoDB connection with Beanie ODM initialization)
- **Security**: `app/core/security.py` (JWT authentication, password hashing, admin requirements)
- **Models**: `app/models/` (Beanie ODM documents representing MongoDB collections)
- **Schemas**: `app/schemas/` (Pydantic models for request/response validation)
- **Services**: `app/services/` (Business logic layer)
- **Routes**: `app/routers/` (API endpoint definitions organized by feature)
- **Tasks**: `app/tasks/` (Celery background tasks for asynchronous processing)
- **Utils**: `app/utils/` (Helper functions like phone validation, date utilities)

**Key Design Patterns:**
1. **Layered Architecture**: Controllers (routers) -> Services -> Models
2. **Dependency Injection**: FastAPI's Depends system for authentication and database access
3. **Environment Configuration**: Pydantic Settings with `.env` file support
4. **Async/Await**: Full async support throughout (FastAPI, Beanie, Motor)
5. **Background Processing**: Celery with Redis broker for scheduled tasks

**Authentication Flow:**
1. User logs in via `/api/v1/auth/login` with phone/PIN
2. System verifies credentials against User model
3. JWT access token (60 min) and refresh token (7 days) are issued
4. Protected endpoints use `get_current_user` dependency to validate tokens
5. Admin endpoints additionally check `require_admin` dependency

**Data Models (Beanie Documents):**
- User: Rider/member information with roles and status
- Loan: Loan applications with repayment schedules
- RentalBooking: Asset reservations
- WelfareEvent: Group support activities
- EventContribution: Tracking contributions to welfare events
- SubscriptionPayment: Membership payment tracking
- Transaction: Financial transaction history
- AuditLog: System activity logging
- InventoryItem: Group assets available for rental
- GroupSettings: Global configuration settings

**API Organization:**
- `/api/v1/auth`: Authentication endpoints (login, refresh, reset-pin)
- `/api/v1/users`: User profile management (admin and self-service)
- `/api/v1/loans`: Loan applications and eligibility checking
- `/api/v1/rentals`: Rental booking management
- `/api/v1/welfare`: Welfare events and support tracking
- `/api/v1/financials`: Financial summaries (personal and group)
- `/api/v1/mpesa`: M-Pesa payment callback handler
- `/api/v1/financials`: Financial reporting

**Background Tasks (Celery):**
- Monthly subscription reminders (daily)
- Loan due date reminders (daily) 
- December redemption processing (annual on Dec 1 at 9 AM)

**Notable Features:**
- Phone number validation and normalization (Kenyan format +254XXX)
- Role-based access control (Admin, Treasurer, Secretary, Chairperson, Member)
- Secure password hashing with bcrypt via passlib
- CORS middleware configured via environment variables
- Comprehensive logging with Loguru
- Swagger/OpenAPI documentation auto-generated