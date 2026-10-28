from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import database
from app.repositories.hotel_repository import HotelRepository
from app.schemas.schemas import HotelResponse, TipoHabitacionResponse

router = APIRouter(prefix="/api/v1", tags=["Hoteles"])


@router.get("/hoteles", response_model=list[HotelResponse])
def listar_hoteles(session: Session = Depends(database.get_session)):
    repository = HotelRepository(session)
    return repository.obtener_todos()


@router.get("/tipos-habitacion", response_model=list[TipoHabitacionResponse])
def listar_tipos_habitacion(session: Session = Depends(database.get_session)):
    repository = HotelRepository(session)
    return repository.obtener_tipos_habitacion()
