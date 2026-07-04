from app.schemas.loan import LoanApplication, CollateralAssetCreate


def test_loan_application_accepts_collateral_assets():
    payload = {
        "amount": 50000,
        "tenure_months": 6,
        "purpose": "Emergency cash",
        "guarantor_ids": [],
        "collateral_assets": [
            {
                "asset_type": "livestock",
                "description": "Two dairy cows",
                "quantity": 2,
                "unit_value": 15000,
            }
        ],
    }

    loan_application = LoanApplication(**payload)

    assert len(loan_application.collateral_assets) == 1
    assert loan_application.collateral_assets[0].asset_type == "livestock"
    assert loan_application.collateral_assets[0].total_value == 30000.0


def test_collateral_asset_schema_requires_positive_values():
    asset = CollateralAssetCreate(
        asset_type="equipment",
        description="Power saw",
        quantity=1,
        unit_value=8000,
    )

    assert asset.total_value == 8000.0
