from datetime import date
from abc import abstractmethod, ABC
from dataclasses import dataclass, field
from typing import ClassVar
from .excepciones import TransicionInvalida

# ══════════════════════════════════════════════════════
# MENÚ — jerarquía de ítems
# ══════════════════════════════════════════════════════

class ItemMenu(ABC):
    """Contrato de todo ítem que puede aparecer en un pedido."""

    def __init__(self, id: str, nombre: str, disponible: bool = True) -> None:
        if not id.strip():
            raise ValueError("El ID del ítem no puede estar vacío")
        if not nombre.strip():
            raise ValueError("El nombre del ítem no puede estar vacío")
        self.id = id
        self.nombre = nombre
        self.disponible = disponible

    @abstractmethod
    def calcular_precio(self) -> float:
        """Precio final del ítem (puede incluir lógica propia)."""

    def resumen(self) -> str:
        estado = "✓" if self.disponible else "✗"
        return f"[{estado}] {self.nombre} — ${self.calcular_precio():.0f}"


class Plato(ItemMenu):
    """Plato individual con precio fijo y lista de adicionales opcionales."""

    def __init__(
        self,
        id: str,
        nombre: str,
        precio_base: float,
        adicionales: list[float] | None = None,
        disponible: bool = True,
    ) -> None:
        super().__init__(id, nombre, disponible)
        if precio_base <= 0:
            raise ValueError(f"El precio base debe ser positivo: {precio_base}")
        self.precio_base = precio_base
        self.adicionales: list[float] = adicionales or []

    def calcular_precio(self) -> float:
        return self.precio_base + sum(self.adicionales)


class Bebida(ItemMenu):
    """Bebida con precio que varía según el tamaño elegido."""

    MULTIPLICADORES: ClassVar[dict[str, float]] = {
        "S": 1.0,
        "M": 1.4,
        "L": 1.8,
    }

    def __init__(
        self,
        id: str,
        nombre: str,
        precio_base: float,
        tamanio: str = "M",
        disponible: bool = True,
    ) -> None:
        super().__init__(id, nombre, disponible)
        if precio_base <= 0:
            raise ValueError(f"El precio base debe ser positivo: {precio_base}")
        if tamanio not in self.MULTIPLICADORES:
            raise ValueError(f"Tamaño '{tamanio}' no válido. Use S, M o L")
        self.precio_base = precio_base
        self.tamanio = tamanio

    def calcular_precio(self) -> float:
        return round(self.precio_base * self.MULTIPLICADORES[self.tamanio], 2)


class Combo(ItemMenu):
    """Conjunto de ítems vendidos juntos con descuento."""

    def __init__(
        self,
        id: str,
        nombre: str,
        items: list[ItemMenu],
        descuento_porcentaje: float = 10.0,
        disponible: bool = True,
    ) -> None:
        super().__init__(id, nombre, disponible)
        if not items:
            raise ValueError("Un combo debe tener al menos un ítem")
        if not (0.0 <= descuento_porcentaje <= 50.0):
            raise ValueError(f"Descuento {descuento_porcentaje}% fuera del rango 0–50")
        self.items = items
        self.descuento_porcentaje = descuento_porcentaje

    def calcular_precio(self) -> float:
        total = sum(item.calcular_precio() for item in self.items)
        return round(total * (1 - self.descuento_porcentaje / 100), 2)


# ══════════════════════════════════════════════════════
# PEDIDO
# ══════════════════════════════════════════════════════

@dataclass
class Pedido:
    """Un pedido realizado por un cliente."""

    FLUJO_VALIDO: ClassVar[dict[str, list[str]]] = {
        "RECIBIDO":       ["EN_PREPARACION"],
        "EN_PREPARACION": ["EN_CAMINO"],
        "EN_CAMINO":      ["ENTREGADO"],
        "ENTREGADO":      [],
    }

    id: int
    cliente: str
    items: list[tuple[ItemMenu, int]] = field(default_factory=list)
    fecha: date = field(default_factory=date.today)
    estado: str = "RECIBIDO"

    def __post_init__(self) -> None:
        if not self.cliente.strip():
            raise ValueError("El nombre del cliente no puede estar vacío")
        if self.id <= 0:
            raise ValueError(f"ID de pedido inválido: {self.id}")

    def avanzar_estado(self) -> None:
        siguientes = self.FLUJO_VALIDO.get(self.estado, [])
        if not siguientes:
            raise TransicionInvalida(
                f"El pedido en estado '{self.estado}' no puede avanzar más"
            )
        self.estado = siguientes[0]

    def total_items(self) -> float:
        return sum(item.calcular_precio() * cant for item, cant in self.items)

