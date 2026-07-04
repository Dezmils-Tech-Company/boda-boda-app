# app/services/asset_service.py
from datetime import datetime
from typing import List, Dict
from app.models.asset import Asset
from app.models.user import User

# Asset valuation constants (points per 1000 KES)
ASSET_VALUES = {
    "livestock": 0.5,  # 0.5 points per 1000 KES
    "equipment": 0.3,
    "business": 0.4,
    "land": 0.6,
    "default": 0.2
}

async def create_member_asset(member: User, asset_data) -> Asset:
    """Persist a member's collateral asset for eligibility scoring."""
    asset = Asset(
        member=member,
        asset_type=asset_data.asset_type,
        description=asset_data.description,
        quantity=asset_data.quantity,
        unit_value=asset_data.unit_value,
        total_value=asset_data.total_value,
        acquisition_date=(
            asset_data.acquisition_date
            if hasattr(asset_data, "acquisition_date") and asset_data.acquisition_date is not None
            else datetime.utcnow()
        ),
        status="Active",
    )
    await asset.insert()
    return asset


def calculate_asset_score(assets: List[Dict]) -> float:
    """
    Calculate asset ownership score (0-40 points)

    Args:
        assets: List of asset dictionaries with asset_type, quantity, unit_value

    Returns:
        float: Asset score between 0 and 40
    """
    total_score = 0.0

    for asset in assets:
        asset_type = asset.get("asset_type", "default")
        quantity = max(0, asset.get("quantity", 0))  # Ensure non-negative
        unit_value = max(0.0, asset.get("unit_value", 0.0))  # Ensure non-negative

        # Calculate total value
        total_value = quantity * unit_value

        # Get points per 1000 KES for this asset type
        points_per_1000 = ASSET_VALUES.get(asset_type, ASSET_VALUES["default"])

        # Calculate score for this asset
        asset_score = (total_value / 1000) * points_per_1000
        total_score += asset_score

    # Cap at 40 points
    return min(total_score, 40.0)