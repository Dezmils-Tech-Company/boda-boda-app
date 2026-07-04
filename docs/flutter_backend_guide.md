# Flutter Frontend Guide for the Oteri Backend

This document is a complete handoff for the Flutter app that will consume this backend. It explains what the backend does, how authentication works, what each endpoint expects, who can access each endpoint, and the business rules the frontend must respect.

## 1. Backend purpose

The backend powers a Boda Boda Chama / self-help group platform for:

- member registration and profile management
- authentication and role-based access
- loan applications and eligibility scoring
- savings deposits and balance tracking
- welfare event proposals and approval
- rental bookings for group inventory
- financial summaries for members and admins
- M-Pesa callback handling
- report generation uploads

## 2. Base URL and environment

Use the backend base URL as:

- local development: http://localhost:8000
- or whatever host/port is configured in the environment

All API routes are under:

- /api/v1

The app root is:

- GET /

## 3. Authentication model

The backend uses JWT-based authentication.

### Login flow

1. Call login with phone and PIN.
2. Receive an access token, refresh token, and role.
3. Store the tokens securely in Flutter.
4. Attach the access token as a Bearer token on protected requests.

### Token format

- access_token: short-lived JWT
- refresh_token: longer-lived JWT
- role: one of Admin, Treasurer, Secretary, Chairperson, Member

### Auth endpoints

- POST /api/v1/auth/login
- POST /api/v1/auth/refresh
- POST /api/v1/auth/reset-pin

### Role-based access

The backend uses these roles:

- Member: regular user, can view own profile, apply for loans, submit welfare proposals, view own financials, make rental bookings, deposit savings
- Treasurer: can approve loans, view loan official actions, and can access loan official permissions
- Secretary: can approve loans
- Chairperson: can approve loans
- Admin: full administrative access across users, welfare approvals, inventory, rentals, financials, reports

### Role access summary

| Role | Main capabilities |
|---|---|
| Member | login, own profile, loan eligibility, post collateral, apply for loan, savings deposit, welfare proposal, rentals booking, own financials |
| Treasurer | Member + loan approval |
| Secretary | Member + loan approval |
| Chairperson | Member + loan approval |
| Admin | Full control over members, welfare, rentals, financials, reports |

## 4. Primary role of the Flutter agent

The Flutter agent is responsible for building a mobile-friendly frontend that:

- authenticates members securely
- routes users to the right screens based on role
- consumes backend endpoints with correct payloads
- handles errors and success states cleanly
- protects sensitive operations behind role-based UI gating
- displays financial, loan, rental, and welfare information in a simple mobile-first experience

The frontend should not invent data or bypass backend validation. It should treat the backend as the source of truth.

## 5. API endpoint catalog

### A. Authentication

#### 1) Login

- Method: POST
- Path: /api/v1/auth/login
- Access: public
- Auth: none
- Payload: form-data (not JSON)

Fields:

- username: phone number
- password: PIN

Example:

```json
{
  "username": "+254700000000",
  "password": "1234"
}
```

Response:

```json
{
  "access_token": "...",
  "token_type": "bearer",
  "refresh_token": "...",
  "role": "Member"
}
```

Frontend note:
- Use the phone number as the login username.
- Save the access token and refresh token.

#### 2) Refresh token

- Method: POST
- Path: /api/v1/auth/refresh
- Access: public
- Payload:

```json
{
  "refresh_token": "..."
}
```

Response: same shape as login.

#### 3) Reset PIN

- Method: POST
- Path: /api/v1/auth/reset-pin
- Access: authenticated user
- Payload:

```json
{
  "current_pin": "1234",
  "new_pin": "5678"
}
```

## B. Users and profile

#### 4) Create a user

- Method: POST
- Path: /api/v1/users/
- Access: Admin only
- Payload:

```json
{
  "phone": "+254700000000",
  "full_name": "Jane Doe",
  "pin": "1234",
  "role": "Member",
  "id_number": "12345678",
  "image": "https://example.com/profile.jpg",
  "photo": "https://example.com/profile.jpg",
  "family_members": [
    {
      "name": "John Doe",
      "age": 25,
      "relationship": "Brother"
    }
  ],
  "next_of_kin": {
    "name": "Jane Doe",
    "phone": "+254700000001",
    "relationship": "Sister"
  }
}
```

Notes:
- The backend expects a PIN and will hash it.
- Role values are Admin, Treasurer, Secretary, Chairperson, Member.

#### 5) Get current user profile

- Method: GET
- Path: /api/v1/users/me
- Access: authenticated user
- No payload

#### 6) List all users

- Method: GET
- Path: /api/v1/users/
- Access: Admin only
- No payload

#### 7) Get a user by phone

- Method: GET
- Path: /api/v1/users/{phone}
- Access: authenticated user
- No payload

## C. Welfare

#### 8) Create a welfare event directly

- Method: POST
- Path: /api/v1/welfare/events
- Access: Admin only
- Payload:

```json
{
  "event_type": "Medical",
  "title": "Emergency support",
  "description": "Support for a member",
  "affected_member_id": "member_id_here",
  "amount_per_member": 500,
  "deadline": "2026-07-15T10:00:00Z"
}
```

#### 9) Submit a welfare proposal

- Method: POST
- Path: /api/v1/welfare/events/propose
- Access: authenticated member
- Payload:

```json
{
  "event_type": "School",
  "title": "School fees support",
  "description": "Help with school fees",
  "proof_images": [
    "https://example.com/image1.jpg"
  ]
}
```

Important:
- The authenticated user becomes the affected member automatically.
- This creates a pending proposal that must be approved by Admin.
- The proposal does not require amount/deadline at submission time.

#### 10) Approve a welfare proposal

- Method: POST
- Path: /api/v1/welfare/events/{event_id}/approve
- Access: Admin only
- Payload: none

#### 11) List active welfare events

- Method: GET
- Path: /api/v1/welfare/events/active
- Access: authenticated user
- No payload

#### 12) List pending welfare proposals

- Method: GET
- Path: /api/v1/welfare/events/pending
- Access: Admin only
- No payload

## D. Rentals and inventory

#### 13) Create a rental booking

- Method: POST
- Path: /api/v1/rentals/bookings
- Access: authenticated user
- Payload:

```json
{
  "items": [
    {
      "item_id": "inventory_item_id",
      "quantity": 1
    }
  ],
  "start_date": "2026-07-10T08:00:00Z",
  "end_date": "2026-07-12T08:00:00Z"
}
```

#### 14) Get my rental bookings

- Method: GET
- Path: /api/v1/rentals/my-bookings
- Access: authenticated user
- No payload

#### 15) List inventory items

- Method: GET
- Path: /api/v1/rentals/inventory
- Access: authenticated user
- Query parameters:
  - available_only: boolean, optional

Example:

- /api/v1/rentals/inventory?available_only=true

#### 16) Add a new inventory item

- Method: POST
- Path: /api/v1/rentals/inventory
- Access: Admin only
- Payload:

```json
{
  "name": "Motorbike Helmet",
  "category": "Safety",
  "total_quantity": 10,
  "available_quantity": 10,
  "daily_rate": 200,
  "deposit_rate": 1000,
  "photos": ["https://example.com/helmet.jpg"],
  "condition": "Good",
  "location": "Store A"
}
```

#### 17) Delete an inventory item

- Method: DELETE
- Path: /api/v1/rentals/inventory/{item_id}
- Access: Admin only
- No payload

#### 18) List pending rental bookings

- Method: GET
- Path: /api/v1/rentals/bookings/pending
- Access: Admin only
- No payload

#### 19) Approve a rental booking

- Method: POST
- Path: /api/v1/rentals/bookings/{booking_id}/approve
- Access: Admin only
- Payload: none

## E. Loans and savings

#### 20) Get loan eligibility

- Method: GET
- Path: /api/v1/loans/eligibility
- Access: authenticated user
- No payload

Response:

```json
{
  "score": 78,
  "max_loan_amount": 54600,
  "eligible": true,
  "breakdown": {
    "subscription_history": 12,
    "repayment_behavior": 25,
    "boda_specific": 20,
    "participation": 10,
    "longevity_bonus": 5
  }
}
```

Frontend note:
- Show the eligibility score and the max loan amount before loan application.
- If eligible is false, block the apply flow.

#### 21) Post collateral asset for eligibility scoring

- Method: POST
- Path: /api/v1/loans/assets
- Access: authenticated user
- Payload:

```json
{
  "asset_type": "Motorbike",
  "description": "Bajaj Boxer",
  "quantity": 1,
  "unit_value": 180000,
  "total_value": 180000
}
```

Important:
- This asset is stored for the current user and contributes to loan eligibility scoring.
- The frontend should allow the member to add collateral before applying.

#### 22) Apply for a loan

- Method: POST
- Path: /api/v1/loans/apply
- Access: authenticated user
- Payload:

```json
{
  "amount": 50000,
  "tenure_months": 6,
  "purpose": "Business expansion",
  "guarantor_ids": ["guarantor_user_id"],
  "interest_rate": 1.5,
  "collateral_assets": [
    {
      "asset_type": "Motorbike",
      "description": "Bajaj Boxer",
      "quantity": 1,
      "unit_value": 180000,
      "total_value": 180000
    }
  ]
}
```

Business rule:
- If the member is not eligible, the backend returns a 400 error.
- The frontend should show a friendly message and not crash.

#### 23) Approve a loan

- Method: POST
- Path: /api/v1/loans/{loan_id}/approve
- Access: Treasurer, Secretary, or Chairperson
- Payload: none

#### 24) Deposit savings

- Method: POST
- Path: /api/v1/loans/savings/deposit
- Access: authenticated user
- Query parameters or form fields:
  - amount
  - description

Example:

- /api/v1/loans/savings/deposit?amount=1000&description=Monthly%20savings

#### 25) Get current savings balance

- Method: GET
- Path: /api/v1/loans/savings/balance
- Access: authenticated user
- No payload

#### 26) Get savings transactions

- Method: GET
- Path: /api/v1/loans/savings/transactions
- Access: authenticated user
- Query parameter:
  - limit: optional integer

## F. Financials

#### 27) Get group financial summary

- Method: GET
- Path: /api/v1/financials/group
- Access: Admin only
- No payload

Response:

```json
{
  "total_balance": 120000,
  "total_income": 300000,
  "total_expenses": 180000,
  "members_savings_total": 250000,
  "active_loans": 4
}
```

#### 28) Get my financial summary

- Method: GET
- Path: /api/v1/financials/me
- Access: authenticated user
- No payload

Response:

```json
{
  "current_savings": 25000,
  "total_contributed": 40000,
  "active_loans": [],
  "transactions": []
}
```

## G. M-Pesa callback

#### 29) M-Pesa callback endpoint

- Method: POST
- Path: /api/v1/mpesa/callback
- Access: external system / callback
- Payload: M-Pesa callback body

The Flutter app should not rely on this endpoint directly. It is mostly for backend payment integration.

## H. Reports

#### 30) Generate a report PDF

- Method: POST
- Path: /api/v1/reports/generate
- Access: Admin only
- Query parameters:
  - title
  - content

Example:

- /api/v1/reports/generate?title=Monthly%20Report&content=Body%20text%20here

Response:

```json
{
  "status": "success",
  "message": "Report generated and stored in Cloudinary",
  "data": {
    "title": "Monthly Report",
    "url": "https://...
",
    "public_id": "..."
  }
}
```

## 6. Important frontend implementation notes

### Recommended Flutter architecture

Use a clean structure like this:

- auth/
  - login, refresh token, secure storage
- models/
  - user, loan, rental, welfare, financial models
- services/
  - api_service, auth_service, user_service, loan_service, welfare_service, rental_service, financial_service
- providers/
  - auth_provider, user_provider, loan_provider, rental_provider, welfare_provider
- screens/
  - login, dashboard, profile, loans, rentals, welfare, financials, admin screens

### Token handling

- Store access and refresh tokens in secure storage.
- Add an auth interceptor to attach the access token automatically.
- If the access token expires, refresh it before retrying.

### Role-based UI

The UI should gate screens and actions based on the current role:

- Admin-only screens: user management, welfare approval, inventory management, financial summary, reports
- Loan-official screens: loan approval actions
- Member screens: loan eligibility, application, savings, welfare proposal, bookings

### Error handling

The backend returns clear errors for validation and business rules.

The frontend should display them as friendly messages, including:

- invalid PIN or login failure
- loan ineligibility
- missing guarantor or invalid item
- approval failure
- insufficient inventory for rental booking
- invalid request payload

## 7. Core business rules the UI must honor

- Members cannot apply for a loan if eligibility score is below threshold.
- Loan applications can include collateral assets and guarantors.
- Rental bookings must have valid inventory items and available stock.
- Welfare proposals are created by the member and approved by Admin.
- Admin approval is required for welfare events and inventory management.
- Admin access is required for group financial views and report generation.
- The frontend should never assume a role-based endpoint is available without the right token and role.

## 8. Suggested initial Flutter screens

1. Splash / auth check
2. Login screen
3. Dashboard screen
4. Profile screen
5. Loans screen with eligibility and apply flow
6. Savings screen
7. Welfare screen with proposal and approval views
8. Rentals screen with inventory and booking flow
9. Financials screen for members and admins
10. Admin panel for user management, approvals, inventory, reports

## 9. Summary for the agent

The frontend agent should build the app around the following workflow:

- authenticate user
- load current profile
- show role-appropriate dashboard
- let members manage savings, loans, welfare proposals, and rentals
- let admins manage approvals, inventory, and reports
- use the backend as the system of record for all state changes

If this guide is followed closely, the Flutter app will align with the backend’s real contracts and business logic.
