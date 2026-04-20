from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, appointments, ai_routes, patient, doctor, websockets, emergency, notifications, doctors_list, records
from models import user, patient as patient_model, doctor as doctor_model, appointment

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MediBridge AI API")

app.include_router(auth.router)
app.include_router(appointments.router)
app.include_router(ai_routes.router)
app.include_router(patient.router)
app.include_router(doctor.router)
app.include_router(websockets.router)
app.include_router(emergency.router)
app.include_router(notifications.router)
app.include_router(doctors_list.router)
app.include_router(records.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to MediBridge AI API", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
