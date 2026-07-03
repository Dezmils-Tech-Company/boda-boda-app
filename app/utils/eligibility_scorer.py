from app.models.user import User
from datetime import datetime, timedelta

class EligibilityScorer:
    def calculate(self, member: User) -> int:
        score = 0

        # 1. Subscription History (Max 40)
        # In production, query SubscriptionPayment collection
        score += 25  # Placeholder real logic: count paid months

        # 2. Repayment Behavior (Max 25)
        score += 15  # Check previous loans

        # 3. Boda Boda Specific (Max 20)
        score += 12  # Bike ownership check

        # 4. Group Participation (Max 10)
        score += 6   # Meeting attendance

        # 5. Bonus (Max 5)
        if member.join_date < datetime.utcnow() - timedelta(days=365):
            score += 3

        return min(score, 100)

    def get_breakdown(self, member: User) -> dict:
        return {
            "subscription_history": 25,
            "repayment_behavior": 15,
            "boda_specific": 12,
            "participation": 6,
            "longevity_bonus": 3,
            "total": 61,
            "max_loan_suggestion": 61000
        }