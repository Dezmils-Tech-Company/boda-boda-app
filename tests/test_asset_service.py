import pytest
from app.services.asset_service import calculate_asset_score

def test_asset_service_known_values():
    """Test asset service with known values and expected outcomes"""

    # Test case 1: Single asset type that should cap at 40 points
    assets = [
        {"asset_type": "livestock", "quantity": 10, "unit_value": 15000}  # 150k value
    ]
    # 150,000 / 1000 * 0.5 = 75 points -> capped at 40
    score = calculate_asset_score(assets)
    assert score == 40.0, f"Expected 40.0, got {score}"

    # Test case 2: Mixed assets that should cap
    assets = [
        {"asset_type": "livestock", "quantity": 2, "unit_value": 20000},  # 40k value
        {"asset_type": "equipment", "quantity": 1, "unit_value": 50000},  # 50k value
        {"asset_type": "business", "quantity": 3, "unit_value": 10000}   # 30k value
    ]
    # Livestock: 40,000/1000 * 0.5 = 20
    # Equipment: 50,000/1000 * 0.3 = 15
    # Business: 30,000/1000 * 0.4 = 12
    # Total: 47 -> capped at 40
    score = calculate_asset_score(assets)
    assert score == 40.0, f"Expected 40.0, got {score}"

    # Test case 3: Low value assets
    assets = [
        {"asset_type": "livestock", "quantity": 1, "unit_value": 5000}  # 5k value
    ]
    # 5,000/1000 * 0.5 = 2.5 points
    score = calculate_asset_score(assets)
    assert score == 2.5, f"Expected 2.5, got {score}"

    # Test case 4: No assets
    assets = []
    score = calculate_asset_score(assets)
    assert score == 0.0, f"Expected 0.0, got {score}"

    # Test case 5: Unknown asset type (should use default value)
    assets = [
        {"asset_type": "unknown_type", "quantity": 10, "unit_value": 10000}  # 100k value
    ]
    # 100,000/1000 * 0.2 (default) = 20 points
    score = calculate_asset_score(assets)
    assert score == 20.0, f"Expected 20.0, got {score}"

def test_asset_service_edge_cases():
    """Test edge cases for asset service"""

    # Test with zero values
    assets = [
        {"asset_type": "livestock", "quantity": 0, "unit_value": 10000},
        {"asset_type": "equipment", "quantity": 10, "unit_value": 0}
    ]
    score = calculate_asset_score(assets)
    assert score == 0.0, f"Expected 0.0, got {score}"

    # Test with negative values (should be treated as zero)
    assets = [
        {"asset_type": "livestock", "quantity": -5, "unit_value": 10000},
        {"asset_type": "equipment", "quantity": 10, "unit_value": -1000}
    ]
    score = calculate_asset_score(assets)
    assert score == 0.0, f"Expected 0.0, got {score}"

if __name__ == "__main__":
    test_asset_service_known_values()
    test_asset_service_edge_cases()
    print("All asset service tests passed!")