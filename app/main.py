from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.db.database import database
from app.routers.hotel_router import router as hotel_router
from app.routers.availability_router import router as availability_router


class HotelReservationAPI:
    def __init__(self):
        self.settings = get_settings()

        self.app = FastAPI(title="Hotel Reservation API", version="1.0.0")

        self.configure_cors()
        self.configure_routes()

    def configure_cors(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.settings.cors_origins,
            allow_credentials=True,
            allow_methods=["GET"],
            allow_headers=["*"],
        )

    def configure_routes(self):
        self.app.include_router(hotel_router)
        self.app.include_router(availability_router)

        @self.app.get("/health", tags=["Health"])
        def health():
            try:
                database.check_connection()
                return {"status": "ok", "database": "connected"}
            except Exception:
                raise HTTPException(
                    status_code=503, detail="Database connection unavailable"
                )


api = HotelReservationAPI()
app = api.app
