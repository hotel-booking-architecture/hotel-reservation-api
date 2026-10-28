from datetime import datetime, date
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Hotel(Base):
    __tablename__ = "hoteles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    ciudad: Mapped[str] = mapped_column(String(100))
    capacidad_por_habitacion: Mapped[int] = mapped_column(Integer)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    habitaciones = relationship("Habitacion", back_populates="hotel")
    tarifas = relationship("Tarifa", back_populates="hotel")


class TipoHabitacion(Base):
    __tablename__ = "tipos_habitacion"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(45))
    descripcion: Mapped[str | None] = mapped_column(String(255), nullable=True)

    habitaciones = relationship("Habitacion", back_populates="tipo")
    tarifas = relationship("Tarifa", back_populates="tipo")


class Habitacion(Base):
    __tablename__ = "habitaciones"
    __table_args__ = (UniqueConstraint("hotel_id", "numero"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hoteles.id"))
    tipo_habitacion_id: Mapped[int] = mapped_column(ForeignKey("tipos_habitacion.id"))
    numero: Mapped[str] = mapped_column(String(10))
    activa: Mapped[bool] = mapped_column(Boolean, default=True)

    hotel = relationship("Hotel", back_populates="habitaciones")
    tipo = relationship("TipoHabitacion", back_populates="habitaciones")
    reservas = relationship("ReservaHabitacion", back_populates="habitacion")


class Temporada(Base):
    __tablename__ = "temporadas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(45))
    descripcion: Mapped[str | None] = mapped_column(String(255), nullable=True)

    periodos = relationship("PeriodoTemporada", back_populates="temporada")
    tarifas = relationship("Tarifa", back_populates="temporada")


class PeriodoTemporada(Base):
    __tablename__ = "periodos_temporada"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    temporada_id: Mapped[int] = mapped_column(ForeignKey("temporadas.id"))
    fecha_inicio: Mapped[date] = mapped_column(Date)
    fecha_fin: Mapped[date] = mapped_column(Date)

    temporada = relationship("Temporada", back_populates="periodos")


class Tarifa(Base):
    __tablename__ = "tarifas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hoteles.id"))
    tipo_habitacion_id: Mapped[int] = mapped_column(ForeignKey("tipos_habitacion.id"))
    temporada_id: Mapped[int] = mapped_column(ForeignKey("temporadas.id"))
    precio_base_habitacion: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    precio_por_persona: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    hotel = relationship("Hotel", back_populates="tarifas")
    tipo = relationship("TipoHabitacion", back_populates="tarifas")
    temporada = relationship("Temporada", back_populates="tarifas")


class Reserva(Base):
    __tablename__ = "reservas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha_entrada: Mapped[date] = mapped_column(Date)
    fecha_salida: Mapped[date] = mapped_column(Date)
    numero_personas: Mapped[int] = mapped_column(Integer)
    estado: Mapped[str] = mapped_column(Enum("PENDIENTE", "CONFIRMADA", "CANCELADA"))
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    habitaciones = relationship("ReservaHabitacion", back_populates="reserva")


class ReservaHabitacion(Base):
    __tablename__ = "reserva_habitaciones"
    __table_args__ = (UniqueConstraint("reserva_id", "habitacion_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reserva_id: Mapped[int] = mapped_column(ForeignKey("reservas.id"))
    habitacion_id: Mapped[int] = mapped_column(ForeignKey("habitaciones.id"))

    reserva = relationship("Reserva", back_populates="habitaciones")
    habitacion = relationship("Habitacion", back_populates="reservas")
