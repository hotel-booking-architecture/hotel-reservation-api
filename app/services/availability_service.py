from datetime import date, timedelta
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.hotel_repository import HotelRepository
from app.repositories.disponibilidad_repository import DisponibilidadRepository


class AvailabilityService:
    def __init__(self, session: Session):
        self.hotel_repository = HotelRepository(session)
        self.disponibilidad_repository = DisponibilidadRepository(session)

    def consultar(
        self,
        hotel_id: int,
        tipo_habitacion_id: int,
        fecha_entrada: date,
        fecha_salida: date,
        numero_personas: int,
        numero_habitaciones: int,
    ):
        if fecha_salida <= fecha_entrada:
            raise HTTPException(400, "Las fechas de viaje no son válidas")

        if numero_personas < 1 or numero_habitaciones < 1:
            raise HTTPException(400, "Personas y habitaciones deben ser mayores a cero")

        hotel = self.hotel_repository.obtener_por_id(hotel_id)

        if not hotel or not hotel.activo:
            raise HTTPException(404, "Hotel no encontrado")

        tipos = self.hotel_repository.obtener_tipos_habitacion()
        tipo = next((item for item in tipos if item.id == tipo_habitacion_id), None)

        if not tipo:
            raise HTTPException(404, "Tipo de habitación no encontrado")

        capacidad = hotel.capacidad_por_habitacion

        if numero_personas > numero_habitaciones * capacidad:
            raise HTTPException(
                400, "El número de personas supera la capacidad solicitada"
            )

        habitaciones = self.disponibilidad_repository.buscar_habitaciones(
            hotel_id, tipo_habitacion_id, fecha_entrada, fecha_salida
        )

        disponible = len(habitaciones) >= numero_habitaciones
        noches = (fecha_salida - fecha_entrada).days

        desglose = []
        total = Decimal("0.00")

        if disponible:
            acumulado = {}

            for indice in range(noches):
                fecha = fecha_entrada + timedelta(days=indice)

                temporada = self.disponibilidad_repository.obtener_temporada(fecha)

                if not temporada:
                    raise HTTPException(
                        422, f"No existe temporada configurada para {fecha}"
                    )

                tarifa = self.disponibilidad_repository.obtener_tarifa(
                    hotel_id, tipo_habitacion_id, temporada.id
                )

                if not tarifa:
                    raise HTTPException(
                        422, f"No existe tarifa para la temporada {temporada.nombre}"
                    )

                subtotal = (
                    tarifa.precio_base_habitacion * numero_habitaciones
                    + tarifa.precio_por_persona * numero_personas
                )

                total += subtotal

                if temporada.id not in acumulado:
                    acumulado[temporada.id] = {
                        "temporada": temporada.nombre,
                        "noches": 0,
                        "subtotal": Decimal("0.00"),
                    }

                acumulado[temporada.id]["noches"] += 1
                acumulado[temporada.id]["subtotal"] += subtotal

            desglose = list(acumulado.values())

        return {
            "hotel_id": hotel.id,
            "hotel": hotel.nombre,
            "tipo_habitacion": tipo.nombre,
            "fecha_entrada": fecha_entrada,
            "fecha_salida": fecha_salida,
            "noches": noches,
            "numero_personas": numero_personas,
            "habitaciones_solicitadas": numero_habitaciones,
            "habitaciones_disponibles": len(habitaciones),
            "capacidad_por_habitacion": capacidad,
            "disponible": disponible,
            "habitaciones": (
                [
                    {"id": habitacion.id, "numero": habitacion.numero}
                    for habitacion in habitaciones[:numero_habitaciones]
                ]
                if disponible
                else []
            ),
            "desglose": desglose,
            "tarifa_total": total if disponible else None,
        }
