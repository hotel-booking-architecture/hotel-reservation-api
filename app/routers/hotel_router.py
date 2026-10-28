from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import database
from app.schemas.schemas import DisponibilidadResponse
from app.services.availability_service import AvailabilityService

router = APIRouter(prefix="/api/v1", tags=["Disponibilidad"])


@router.get("/disponibilidad", response_model=DisponibilidadResponse)
def consultar_disponibilidad(
    hotel_id: int = Query(..., ge=1),
    tipo_habitacion_id: int = Query(..., ge=1),
    fecha_entrada: date = Query(...),
    fecha_salida: date = Query(...),
    numero_personas: int = Query(..., ge=1),
    numero_habitaciones: int = Query(..., ge=1),
    session: Session = Depends(database.get_session),
):
    service = AvailabilityService(session)

    return service.consultar(
        hotel_id=hotel_id,
        tipo_habitacion_id=tipo_habitacion_id,
        fecha_entrada=fecha_entrada,
        fecha_salida=fecha_salida,
        numero_personas=numero_personas,
        numero_habitaciones=numero_habitaciones,
    )
