from fastapi import APIRouter

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/")
def get_notifications():
    return [
        {"id": 1, "title": "Appointment Confirmed", "message": "Your appointment with Dr. Sharma is confirmed for tomorrow.", "time": "2 hours ago", "read": False},
        {"id": 2, "title": "New Message", "message": "You have a new message from the pharmacy.", "time": "5 hours ago", "read": True},
        {"id": 3, "title": "Health Tip", "message": "Remember to drink at least 8 glasses of water today!", "time": "1 day ago", "read": True}
    ]
