# Export asset service
from .asset_service import calculate_asset_score, ASSET_VALUES

# Only export what we need to avoid circular imports
__all__ = [
    "calculate_asset_score",
    "ASSET_VALUES"
]