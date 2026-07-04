# Enhanced Loan Eligibility Scorer Design

## Overview
This document describes the design for an enhanced loan eligibility scorer that is more financially oriented and production-ready, focusing on assets/savings as the primary factor while incorporating other financial behaviors.

## Goals
- Provide a nuanced, weighted scoring model (0-100) that reflects financial health
- Leverage existing data models where possible and extend with new models as needed
- Maintain backward compatibility with existing interface (score 0-100 + breakdown dict)
- Focus on assets/savings as the primary financial factor

## Architecture

### Core Components

#### 1. Asset Model (New)
```python
class Asset(Document):
    """Model to track member assets for collateral and wealth assessment"""
    member: Link["User"]
    asset_type: str  # livestock, equipment, business, land, etc.
    description: str
    quantity: int
    unit_value: float  # Estimated market value per unit
    total_value: float  # Computed: quantity * unit_value
    acquisition_date: datetime
    status: str = "Active"  # Active, Sold, Disposed
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "assets"
```

#### 2. Enhanced Transaction Analysis
Utilize existing `Transaction` model to analyze:
- Savings Behavior: Regular deposits, subscription payments
- Income Patterns: Consistent inflows
- Financial Discipline: Balance maintenance, savings growth

#### 3. Scoring Engine (Enhanced EligibilityScorer)
Four weighted components:
- **Asset Ownership (40 points)**: Based on types, quantity, and value of assets
- **Savings & Payment Behavior (30 points)**: Transaction history analysis
- **Credit & Repayment History (20 points)**: Loan repayment performance  
- **Membership Stability & Engagement (10 points)**: Tenure and participation

### Data Flow
1. **Data Collection**: 
   - Query Asset model for member's assets
   - Query Transaction model for financial history
   - Query Loan model for repayment history
   - Query User model for membership details

2. **Analysis Modules**:
   - Asset Analyzer: Calculates asset score (0-40)
   - Transaction Analyzer: Scores savings/income behavior (0-30)  
   - Credit Analyzer: Scores loan repayment (0-20)
   - Stability Analyzer: Scores tenure/participation (0-10)

3. **Scoring & Output**:
   - Sum component scores (0-100)
   - Generate detailed breakdown
   - Return score and breakdown dictionary

### Scoring Details

#### Asset Ownership (40 points)
- Points based on asset types and values:
  - Livestock: 0.5 points per 1,000 KES value (max 10 pts)
  - Equipment: 0.3 points per 1,000 KES value (max 10 pts)  
  - Business assets: 0.4 points per 1,000 KES value (max 10 pts)
  - Land: 0.6 points per 1,000 KES value (max 10 pts)
- Total capped at 40 points

#### Savings & Payment Behavior (30 points)
- Analyze transaction history for regular patterns:
  - Consistent monthly deposits: up to 15 points
  - Subscription payment regularity: up to 10 points
  - Average savings balance relative to income: up to 5 points

#### Credit & Repayment History (20 points)
- Loan repayment performance:
  - Percentage of loans paid on time: up to 10 points
  - Loan completion rate (paid/closed vs total): up to 10 points

#### Membership Stability & Engagement (10 points)
- Tenure bonus: 5 points for >1 year membership
- Participation bonus: 5 points for regular meeting attendance (if tracked) or consistent financial activity

## Interface
The enhanced `EligibilityScorer.calculate()` method will maintain the same signature:
```python
def calculate(self, member: User) -> int:
    # Returns score 0-100
```

The `get_breakdown()` method will return a dictionary with:
```python
{
    "asset_ownership": points_earned,
    "savings_behavior": points_earned,
    "credit_history": points_earned,
    "membership_stability": points_earned,
    "total": total_score,
    "max_loan_suggestion": total_score * 700  # Example multiplier
}
```

## Implementation Considerations
1. **Asset Valuation**: Need to establish standard unit values for different asset types
2. **Backfill Strategy**: Existing members will need asset records created or estimated
3. **Performance**: Ensure queries should not made big impact
4. **Configuration**: Point thresholds and multipliers should be configurable via environment or settings
5. **Testing**: Unit tests for each analyzer component and integration tests for full scoring

## Extensibility
- New asset types can be added to the scoring matrix
- Additional transaction analysis dimensions can be incorporated
- Weights can be adjusted based on empirical performance data

## Security & Validation
- Asset values should be validated (non-negative, reasonable ranges)
- Member ownership of assets is enforced via database links
- No directly user-editable financial scores; derived from verified data