from .excepciones import ItemNoDisponible,PedidoVacio,PedidoNoEncontrado
from .protocolos import CalculadorDescuento, NotificadorPedido, NotificadorConsola, NotificadorSilencioso, DescuentoFijo, DescuentoPorDia
from .modelos import Pedido, ItemMenu
class ServicioPedidos:
    """Gestiona el ciclo de vida de los pedidos."""

    def __init__(self, notificador: NotificadorPedido, descuento: CalculadorDescuento) -> None:
        self._pedidos: dict[int, Pedido] = {}
        self._contador: int = 0
        self._notificador = notificador
        self._descuento = descuento

    def crear_pedido(self, cliente: str, items: list[tuple[ItemMenu, int]]) -> Pedido:
        if not items:
            raise PedidoVacio("No se puede crear un pedido sin ítems")
        for item, _ in items:
            if not item.disponible:
                raise ItemNoDisponible(f"'{item.nombre}' no está disponible")
        self._contador += 1
        pedido = Pedido(id=self._contador, cliente=cliente, items=items)
        self._pedidos[pedido.id] = pedido
        self._notificador.notificar(cliente, pedido)
        return pedido

    def avanzar_estado(self, pedido_id: int) -> str:
        pedido = self._obtener_o_lanzar(pedido_id)
        pedido.avanzar_estado()
        self._notificador.notificar(pedido.cliente, pedido)
        return pedido.estado

    def total_con_descuento(self, pedido_id: int) -> float:
        pedido = self._obtener_o_lanzar(pedido_id)
        total = pedido.total_items()
        # ❌ acoplado a DescuentoFijo
        return self._descuento.calcular(total, pedido)

    def pedidos_por_estado(self, estado: str) -> list[Pedido]:
        return [p for p in self._pedidos.values() if p.estado == estado]

    def _obtener_o_lanzar(self, pedido_id: int) -> Pedido:
        pedido = self._pedidos.get(pedido_id)
        if pedido is None:
            raise PedidoNoEncontrado(f"No existe el pedido #{pedido_id}")
        return pedido

    def contenido_de_pedido(self, pedido: Pedido) -> list[tuple[ItemMenu, int]]:
        lista = [x for x in pedido.items]
        return lista

    def cantidad_de_pedidos_por_estado(self) -> dict[str, int]:
        estados = [p.estado for p in self._pedidos.values()]
        pedidos = {estado: len(self.pedidos_por_estado(estado)) for estado in estados}

        return pedidos

    def clientes_unicos(self):
        clientes = {x.cliente for x in self._pedidos.values()}
        return clientes


