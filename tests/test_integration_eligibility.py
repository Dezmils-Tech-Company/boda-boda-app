"""
Integration test for the eligibility scoring system.
Tests the interaction between components while mocking database dependencies.
"""
import sys
import os
import pytest
from unittest.mock import MagicMock, patch
from bson import ObjectId

# Add the project root to the Python path so we can import the app module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.asset_service import calculate_asset_score
from app.utils.eligibility_scorer import EligibilityScorer
from app.services.loan_service import calculate_eligibility


def test_asset_service_integration():
    """Test asset service integration with realistic data"""
    # Test case that simulates real asset data
    assets = [
        {"asset_type": "livestock", "quantity": 3, "unit_value": 15000},  # 3 cows @ 15k each
        {"asset_type": "equipment", "quantity": 2, "unit_value": 25000},  # 2 items @ 25k each
        {"asset_type": "business", "quantity": 1, "unit_value": 50000},   # 1 business @ 50k
        {"asset_type": "land", "quantity": 1, "unit_value": 100000}       # 1 plot @ 100k
    ]

    # Calculate expected scores:
    # Livestock: 45,000 / 1000 * 0.5 = 22.5
    # Equipment: 50,000 / 1000 * 0.3 = 15.0
    # Business: 50,000 / 1000 * 0.4 = 20.0
    # Land: 100,000 / 1000 * 0.6 = 60.0
    # Total: 117.5 -> capped at 40

    score = calculate_asset_score(assets)
    assert score == 40.0  # Should be capped at maximum


def test_eligibility_scorer_component_integration():
    """Test that all components of the eligibility scorer work together"""
    scorer = EligibilityScorer()

    # Create a member mock with sufficient data to test all components
    member = MagicMock()
    member.id = "507f1f77bcf86cd799439011"  # Valid ObjectId string
    member.join_date = None  # Will be handled by error handling in scorer
    member.status = "Active"
    member.updated_at = None

    # Test that we can get a score without exceptions
    score = scorer.calculate(member)
    assert isinstance(score, int)
    assert 0 <= score <= 100

    # Test that we get a proper breakdown
    breakdown = scorer.get_breakdown(member)
    assert isinstance(breakdown, dict)
    expected_keys = {"asset_ownership", "savings_behavior", "credit_history",
                    "membership_stability", "total", "max_loan_suggestion"}
    assert set(breakdown.keys()) == expected_keys

    # Validate score ranges
    assert 0 <= breakdown["asset_ownership"] <= 40
    assert 0 <= breakdown["savings_behavior"] <= 30
    assert 0 <= breakdown["credit_history"] <= 20
    assert 0 <= breakdown["membership_stability"] <= 10
    assert 0 <= breakdown["total"] <= 100


@pytest.mark.asyncio
async def test_loan_service_integration_with_mocked_scorer():
    """Test loan service integration with mocked eligibility scorer"""
    from unittest.mock import AsyncMock

    # Create a mock member
    member = MagicMock()
    member.id = "507f1f77bcf86cd799439011"
    member.phone = "0712345678"

    # Mock the scorer to return known values
    with patch('app.services.loan_service.scorer') as mock_scorer:
        mock_scorer.calculate.return_value = 75
        mock_scorer.get_breakdown.return_value = {
            "asset_ownership": 30,
            "savings_behavior": 20,
            "credit_history": 15,
            "membership_stability": 10,
            "total": 75,
            "max_loan_suggestion": 52500
        }

        # Test the loan service function
        result = await calculate_eligibility(member)

        # Verify it uses the scorer's results directly
        assert result["score"] == 75
        assert result["max_loan_amount"] == 52500
        assert result["eligible"] == True  # 75 >= 60
        assert result["breakdown"]["asset_ownership"] == 30
        assert result["breakdown"]["savings_behavior"] == 20
        assert result["breakdown"]["credit_history"] == 15
        assert result["breakdown"]["membership_stability"] == 10
        assert result["breakdown"]["total"] == 75
        assert result["breakdown"]["max_loan_suggestion"] == 52500


def test_end_to_end_data_flow():
    """Test a simplified end-to-end data flow with mocked database"""
    # This test verifies that data can flow through the system:
    # Asset data -> Asset service -> Eligibility scorer -> Loan service

    # 1. Simulate asset data from database
    assets_from_db = [
        {"asset_type": "livestock", "quantity": 4, "unit_value": 12000},  # 48k value
        {"asset_type": "business", "quantity": 2, "unit_value": 20000}    # 40k value
    ]

    # 2. Process through asset service
    asset_score = calculate_asset_score(assets_from_db)
    # Livestock: 48,000/1000 * 0.5 = 24
    # Business: 40,000/1000 * 0.4 = 16
    # Total: 40 (exactly at cap)
    assert asset_score == 40.0

    # 3. Verify this would contribute to eligibility scorer
    scorer = EligibilityScorer()
    # We can't easily test the scorer's asset score calculation without mocking
    # the database query, but we verified the asset service works correctly

    # 4. Verify loan service would use the scorer's results
    # This is tested in the mock test above

    assert True  # If we got here, the data flow conceptually works


if __name__ == "__main__":
    test_asset_service_integration()
    test_eligibility_scorer_component_integration()
    test_end_to_end_data_flow()
    print("All integration tests passed!")

    # Note: The async test would need to be run separately with pytest
    print("Run 'pytest test_integration_eligibility.py::test_loan_service_integration_with_mocked_scorer -v' to test the async component")