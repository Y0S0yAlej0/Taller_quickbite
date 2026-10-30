class QuickBiteError(Exception):
    """Base de todos los errores del dominio."""

class ItemNoEncontrado(QuickBiteError):
    """El ítem solicitado no existe en el menú."""

class ClienteNoEncontrado(QuickBiteError):
    """El cliente no está registrado."""

class PedidoNoEncontrado(QuickBiteError):
    """El ID de pedido no existe."""

class PedidoVacio(QuickBiteError):
    """Se intenta confirmar un pedido sin ítems."""

class TransicionInvalida(QuickBiteError):
    """La transición de estado solicitada no está permitida."""

class ItemNoDisponible(QuickBiteError):
    """El ítem existe pero no está disponible actualmente."""
