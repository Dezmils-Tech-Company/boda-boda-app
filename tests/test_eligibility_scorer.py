import pytest
from unittest.mock import MagicMock
from app.utils.eligibility_scorer import EligibilityScorer

def test_eligibility_scorer_interface():
    """Test that EligibilityScorer maintains expected interface"""
    scorer = EligibilityScorer()

    # Test that all expected methods exist
    assert hasattr(scorer, 'calculate')
    assert callable(scorer.calculate)

    assert hasattr(scorer, 'get_breakdown')
    callable(scorer.get_breakdown)

    # Test calculate method returns int in correct range
    member = MagicMock()
    member.id = "test_user"
    score = scorer.calculate(member)
    assert isinstance(score, int)
    assert 0 <= score <= 100

    # Test get_breakdown returns expected structure
    breakdown = scorer.get_breakdown(member)
    assert isinstance(breakdown, dict)
    expected_keys = {"asset_ownership", "savings_behavior", "credit_history",
                    "membership_stability", "total", "max_loan_suggestion"}
    assert set(breakdown.keys()) == expected_keys

    # Verify all values are in expected ranges
    assert 0 <= breakdown["asset_ownership"] <= 40
    assert 0 <= breakdown["savings_behavior"] <= 30
    assert 0 <= breakdown["credit_history"] <= 20
    assert 0 <= breakdown["membership_stability"] <= 10
    assert 0 <= breakdown["total"] <= 100
    assert breakdown["max_loan_suggestion"] >= 0

def test_eligibility_scorer_with_complete_mock():
    """Test EligibilityScorer with reasonably complete mock data"""
    scorer = EligibilityScorer()

    # Create a member mock with reasonable attributes
    member = MagicMock()
    member.id = "507f1f77bcf86cd799439011"  # Valid ObjectId string
    member.join_date = None  # Will be handled gracefully
    member.status = "Active"
    member.updated_at = None

    # These should not throw exceptions
    try:
        score = scorer.calculate(member)
        assert isinstance(score, int)
        assert 0 <= score <= 100
    except Exception as e:
        pytest.fail(f"calculate() raised unexpected exception: {e}")

    try:
        breakdown = scorer.get_breakdown(member)
        assert isinstance(breakdown, dict)
        assert "total" in breakdown
        assert isinstance(breakdown["total"], int)
        assert 0 <= breakdown["total"] <= 100
    except Exception as e:
        pytest.fail(f"get_breakdown() raised unexpected exception: {e}")

def test_eligibility_scorer_error_handling():
    """Test that EligibilityScorer handles errors gracefully"""
    scorer = EligibilityScorer()

    # Test with completely invalid member
    member = MagicMock()
    member.id = None  # This will cause issues in the scoring methods
    # Remove other attributes to force error conditions
    del member.join_date
    del member.status
    del member.updated_at

    # Should still return a score (fallback) rather than throwing
    score = scorer.calculate(member)
    assert isinstance(score, int)
    # Should be in valid range even if it's a fallback score
    assert 0 <= score <= 100

    breakdown = scorer.get_breakdown(member)
    assert isinstance(breakdown, dict)
    assert "total" in breakdown

if __name__ == "__main__":
    test_eligibility_scorer_interface()
    test_eligibility_scorer_with_complete_mock()
    test_eligibility_scorer_error_handling()
    print("All eligibility scorer tests passed!")