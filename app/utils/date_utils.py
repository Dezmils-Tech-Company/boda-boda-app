from datetime import datetime, timedelta

def is_december_redemption_period():
    """Check if we are in December for annual redemption"""
    now = datetime.utcnow()
    return now.month == 12

def get_next_subscription_due():
    """Return next subscription due date"""
    now = datetime.utcnow()
    return (now + timedelta(days=30)).replace(day=1)