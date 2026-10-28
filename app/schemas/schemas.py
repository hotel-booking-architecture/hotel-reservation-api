from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class HotelResponse(BaseModel):
    id: int
    nombre: str
    ciudad: str
    capacidad_por_habitacion: int

    model_config = ConfigDict(from_attributes=True)


class TipoHabitacionResponse(BaseModel):
    id: int
    nombre: str

    model_config = ConfigDict(from_attributes=True)


class HabitacionResponse(BaseModel):
    id: int
    numero: str

    model_config = ConfigDict(from_attributes=True)


class DesgloseTarifa(BaseModel):
    temporada: str
    noches: int
    subtotal: Decimal


class DisponibilidadResponse(BaseModel):
    hotel_id: int
    hotel: str
    tipo_habitacion: str
    fecha_entrada: date
    fecha_salida: date
    noches: int
    numero_personas: int
    habitaciones_solicitadas: int
    habitaciones_disponibles: int
    capacidad_por_habitacion: int
    disponible: bool
    habitaciones: list[HabitacionResponse]
    desglose: list[DesgloseTarifa]
    tarifa_total: Decimal | None
