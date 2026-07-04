from app.models.user import User
from datetime import datetime, timedelta
from app.services.asset_service import calculate_asset_score
import logging

logger = logging.getLogger(__name__)

class EligibilityScorer:
    def calculate(self, member: User) -> int:
        """Calculate enhanced eligibility score (0-100) based on multiple factors"""
        try:
            # 1. Asset Ownership (Max 40 points)
            asset_score = self._calculate_asset_score(member.id)

            # 2. Savings & Payment Behavior (Max 30 points)
            savings_score = self._calculate_savings_score(member.id)

            # 3. Credit & Repayment History (Max 20 points)
            credit_score = self._calculate_credit_score(member.id)

            # 4. Membership Stability & Engagement (Max 10 points)
            stability_score = self._calculate_stability_score(member)

            total_score = asset_score + savings_score + credit_score + stability_score
            return min(int(max(total_score, 0)), 100)  # Ensure 0-100 range
        except Exception as e:
            logger.error(f"Error calculating eligibility score for member {getattr(member, 'id', 'unknown')}: {e}")
            # Return fallback score based on basic info
            return self._calculate_fallback_score(member)

    def _calculate_asset_score(self, member_id: str) -> float:
        """Calculate asset ownership score (0-40 points)"""
        try:
            # Import here to avoid circular imports
            from app.models.asset import Asset
            from beanie import PydanticObjectId

            # Convert string ID to ObjectId if needed
            try:
                member_id_obj = PydanticObjectId(member_id)
            except Exception:
                # If not a valid ObjectId, use as string ID
                member_id_obj = member_id

            # Fetch user's assets
            assets = Asset.find(Asset.member.id == member_id_obj).to_list()

            if not assets:
                return 0.0

            # Convert to format expected by asset service
            asset_data = []
            for asset in assets:
                asset_data.append({
                    "asset_type": asset.asset_type,
                    "quantity": asset.quantity,
                    "unit_value": asset.unit_value
                })

            # Calculate score using asset service
            return calculate_asset_score(asset_data)
        except Exception as e:
            logger.warning(f"Error calculating asset score for member {member_id}: {e}")
            return 0.0

    def _calculate_savings_score(self, member_id: str) -> float:
        """Calculate savings and payment behavior score (0-30 points)"""
        try:
            # Import here to avoid circular imports
            from app.models.transaction import Transaction
            from datetime import datetime, timedelta

            # Get member's transactions
            transactions = Transaction.find(Transaction.member.id == member_id).to_list()

            if not transactions:
                return 0.0

            score = 0.0

            # Analyze transaction patterns for savings behavior
            # Separate debits (negative) and credits (positive)
            credits = [t.amount for t in transactions if t.amount > 0]
            debits = [abs(t.amount) for t in transactions if t.amount < 0]

            total_credits = sum(credits)
            total_debits = sum(debits) if debits else 0.01  # Avoid division by zero

            # Factor 1: Consistent monthly deposits (0-15 points)
            # Check for regular incoming transactions
            if credits:
                # Simple heuristic: if we have regular credits, give points
                # In a real implementation, we'd analyze timing patterns
                avg_credit = sum(credits) / len(credits)
                if avg_credit > 1000:  # Average deposit > 1000 KES
                    score += min(15, len(credits) * 2)  # Up to 15 points for frequency

            # Factor 2: Savings rate (0-10 points)
            # Percentage of income that's saved/not spent
            if total_credits > 0:
                savings_rate = (total_credits - total_debits) / total_credits
                savings_rate = max(0, min(1, savings_rate))  # Clamp between 0 and 1
                score += savings_rate * 10  # 0-10 points

            # Factor 3: Recent activity (0-5 points)
            # Points for recent financial activity
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            recent_transactions = [t for t in transactions if t.created_at >= thirty_days_ago]
            if recent_transactions:
                score += min(5, len(recent_transactions))  # Up to 5 points

            return min(score, 30.0)  # Cap at 30 points
        except Exception as e:
            logger.warning(f"Error calculating savings score for member {member_id}: {e}")
            return 0.0

    def _calculate_credit_score(self, member_id: str) -> float:
        """Calculate credit and repayment history score (0-20 points)"""
        try:
            # Import here to avoid circular imports
            from app.models.loan import Loan

            # Get member's loans
            loans = Loan.find(Loan.member.id == member_id).to_list()

            if not loans:
                # No loan history - neutral score
                return 10.0  # Middle of the road for no history

            score = 0.0

            # Factor 1: Loan repayment status (0-10 points)
            # Points based on what percentage of loans are paid/closed
            total_loans = len(loans)
            paid_loans = len([l for l in loans if l.status in ["Paid", "Closed"]])

            if total_loans > 0:
                repayment_ratio = paid_loans / total_loans
                score += repayment_ratio * 10  # 0-10 points

            # Factor 2: Timeliness of payments (0-10 points)
            # This would require analyzing repayment_schedule in each loan
            # For now, we'll use a simplified approach based on loan status
            active_loans = [l for l in loans if l.status in ["Pending", "Approved"]]
            if not active_loans:
                # No active loans - good sign if they had loans before
                if total_loans > 0:
                    score += 5  # Bonus for having paid off loans
            else:
                # Has active loans - check if they're current
                # Simplified: assume active loans are being paid as agreed
                score += 5  # Partial credit for managing current debt

            return min(score, 20.0)  # Cap at 20 points
        except Exception as e:
            logger.warning(f"Error calculating credit score for member {member_id}: {e}")
            return 0.0

    def _calculate_stability_score(self, member: User) -> float:
        """Calculate membership stability and engagement score (0-10 points)"""
        try:
            score = 0.0

            # Tenure bonus: 5 points for >1 year membership
            if hasattr(member, 'join_date') and member.join_date:
                tenure_days = (datetime.utcnow() - member.join_date).days
                if tenure_days > 365:
                    score += 5.0
                elif tenure_days > 180:  # Partial credit for 6+ months
                    score += 2.5
                elif tenure_days > 90:  # Partial credit for 3+ months
                    score += 1.0

            # Participation bonus: up to 5 points for engagement
            if hasattr(member, 'status') and member.status == "Active":
                # Base points for being active
                score += 2.0

                # Additional points for recent activity
                if hasattr(member, 'updated_at') and member.updated_at:
                    days_since_update = (datetime.utcnow() - member.updated_at).days
                    if days_since_update < 30:  # Active in last month
                        score += 3.0
                    elif days_since_update < 90:  # Active in last 3 months
                        score += 1.5
                    elif days_since_update < 180:  # Active in last 6 months
                        score += 0.5

            return min(score, 10.0)  # Cap at 10 points
        except Exception as e:
            logger.warning(f"Error calculating stability score for member {getattr(member, 'id', 'unknown')}: {e}")
            return 0.0

    def _calculate_fallback_score(self, member: User) -> int:
        """Calculate a basic fallback score when main calculation fails"""
        try:
            score = 50  # Start with middle score

            # Adjust based on basic info
            if hasattr(member, 'status'):
                if member.status == "Active":
                    score += 10
                elif member.status != "Active":
                    score -= 10

            # Ensure bounds
            return max(0, min(100, score))
        except Exception:
            return 50  # Ultimate fallback

    def get_breakdown(self, member: User) -> dict:
        """Get detailed breakdown of score components"""
        try:
            member_id = str(member.id) if hasattr(member, 'id') else str(member)

            asset_score = self._calculate_asset_score(member_id)
            savings_score = self._calculate_savings_score(member_id)
            credit_score = self._calculate_credit_score(member_id)
            stability_score = self._calculate_stability_score(member)
            total = int(asset_score + savings_score + credit_score + stability_score)

            return {
                "asset_ownership": int(max(0, min(asset_score, 40))),
                "savings_behavior": int(max(0, min(savings_score, 30))),
                "credit_history": int(max(0, min(credit_score, 20))),
                "membership_stability": int(max(0, min(stability_score, 10))),
                "total": max(0, min(total, 100)),
                "max_loan_suggestion": max(0, min(total, 100)) * 700  # Example multiplier
            }
        except Exception as e:
            logger.error(f"Error getting breakdown for member {getattr(member, 'id', 'unknown')}: {e}")
            # Return default breakdown
            return {
                "asset_ownership": 0,
                "savings_behavior": 0,
                "credit_history": 0,
                "membership_stability": 0,
                "total": 50,
                "max_loan_suggestion": 35000
            }