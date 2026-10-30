from typing import Protocol
from .modelos import Pedido

class NotificadorPedido(Protocol):
    def notificar(self, cliente: str, pedido: Pedido) -> str:
        pass

class NotificadorConsola:
    def notificar(self, cliente: str, pedido: Pedido) -> str:
        mensaje = f"[CONSOLA] {cliente} - Pedido #{pedido.id}: {pedido.estado}"
        print(mensaje)
        return mensaje


class NotificadorSilencioso:
    def notificar(self, cliente: str, pedido: Pedido) -> str:
        return f"[SHHH] {cliente} - {pedido}"

class CalculadorDescuento(Protocol):
    def calcular(self, total: float, pedido: Pedido) -> float:
        pass

class DescuentoFijo:
    def __init__(self, porcentaje: float) -> None:
        if not 0 <= porcentaje <= 100:
            raise ValueError("El porcentaje esta fuera del rango")
        self.porcentaje = porcentaje

    def calcular(self, total: float, pedido: Pedido) -> float:
        return round(total * (1 - self.porcentaje / 100), 2)


class DescuentoPorDia:

    def __init__(self, porcentaje_semana: float, porcentaje_fin_semana: float) -> None:
        if not 0 <= porcentaje_semana <= 100:
            raise ValueError("El porcentaje entre semana esta fuera del rango")
        if not 0 <= porcentaje_fin_semana <= 100:
            raise ValueError("El porcentaje de fin de semana esta fuera del rango")

        self.porcentaje_semana = porcentaje_semana
        self.porcentaje_fin_semana = porcentaje_fin_semana

    def calcular(self, total: float, pedido: Pedido) -> float:
        es_fin_de_semana = pedido.fecha.weekday() >= 5

        if es_fin_de_semana == True:
            porcentaje_aplicado = self.porcentaje_fin_semana
        else:
            porcentaje_aplicado = self.porcentaje_semana

        return round(total * (1 - porcentaje_aplicado / 100), 2)




