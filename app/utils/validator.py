from fastapi import HTTPException

def validate_phone(phone: str):
    if not phone.startswith("+254"):
        raise HTTPException(400, "Phone must start with +254")
    if len(phone) != 13:
        raise HTTPException(400, "Invalid Kenyan phone number")
    return phone