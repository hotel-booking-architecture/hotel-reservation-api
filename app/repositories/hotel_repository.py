from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Hotel, TipoHabitacion


class HotelRepository:
    def __init__(self, session: Session):
        self.session = session

    def obtener_todos(self):
        consulta = select(Hotel).where(Hotel.activo.is_(True))
        return self.session.scalars(consulta).all()

    def obtener_por_id(self, hotel_id: int):
        return self.session.get(Hotel, hotel_id)

    def obtener_tipos_habitacion(self):
        consulta = select(TipoHabitacion)
        return self.session.scalars(consulta).all()
