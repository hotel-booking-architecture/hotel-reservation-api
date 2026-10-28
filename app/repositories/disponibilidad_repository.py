from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import (
    Habitacion,
    PeriodoTemporada,
    Reserva,
    ReservaHabitacion,
    Tarifa,
    Temporada,
)


class DisponibilidadRepository:
    def __init__(self, session: Session):
        self.session = session

    def buscar_habitaciones(
        self,
        hotel_id: int,
        tipo_habitacion_id: int,
        fecha_entrada: date,
        fecha_salida: date,
    ):
        habitaciones_ocupadas = (
            select(ReservaHabitacion.habitacion_id)
            .join(Reserva, Reserva.id == ReservaHabitacion.reserva_id)
            .where(
                Reserva.estado.in_(["PENDIENTE", "CONFIRMADA"]),
                Reserva.fecha_entrada < fecha_salida,
                Reserva.fecha_salida > fecha_entrada,
            )
        )

        consulta = (
            select(Habitacion)
            .where(
                Habitacion.hotel_id == hotel_id,
                Habitacion.tipo_habitacion_id == tipo_habitacion_id,
                Habitacion.activa.is_(True),
                Habitacion.id.not_in(habitaciones_ocupadas),
            )
            .order_by(Habitacion.numero)
        )

        return self.session.scalars(consulta).all()

    def obtener_temporada(self, fecha: date):
        consulta = (
            select(Temporada)
            .join(PeriodoTemporada)
            .where(
                PeriodoTemporada.fecha_inicio <= fecha,
                PeriodoTemporada.fecha_fin >= fecha,
            )
        )

        return self.session.scalars(consulta).first()

    def obtener_tarifa(self, hotel_id: int, tipo_habitacion_id: int, temporada_id: int):
        consulta = select(Tarifa).where(
            Tarifa.hotel_id == hotel_id,
            Tarifa.tipo_habitacion_id == tipo_habitacion_id,
            Tarifa.temporada_id == temporada_id,
        )

        return self.session.scalars(consulta).first()
