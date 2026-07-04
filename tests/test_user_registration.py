from app.schemas.user import UserCreate


def test_user_registration_accepts_profile_photo():
    payload = UserCreate(
        phone="+254700000000",
        full_name="Jane Doe",
        pin="1234",
        image="https://example.com/profile.jpg",
        photo="https://example.com/alt.jpg",
    )

    data = payload.model_dump()

    assert data["image"] == "https://example.com/profile.jpg"
    assert data["photo"] == "https://example.com/alt.jpg"
    assert "inventory_items" not in data
