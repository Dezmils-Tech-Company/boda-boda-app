from app.models.loan import Loan
from app.models.user import User
from app.utils.eligibility_scorer import EligibilityScorer

scorer = EligibilityScorer()

async def calculate_eligibility(member: User):
    score = scorer.calculate(member)
    return {
        "score": score,
        "max_loan_amount": score * 500,  # Example logic
        "eligible": score >= 60
    }

async def create_loan(loan_data, member):
    eligibility = await calculate_eligibility(member)
    if not eligibility["eligible"]:
        raise ValueError("Not eligible for loan")
    
    loan = Loan(**loan_data.dict(), member=member)
    await loan.insert()
    return loan