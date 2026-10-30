from .excepciones import TransicionInvalida
from .modelos import Plato, Bebida, Combo
from .protocolos import NotificadorConsola, NotificadorSilencioso, DescuentoPorDia, DescuentoFijo
from .servicio import ServicioPedidos


if __name__ == "__main__":
    # se inyectan las implementaciones
    notificador_inicial = NotificadorConsola()
    descuento_inicial = DescuentoPorDia(porcentaje_semana=10.0, porcentaje_fin_semana=20.0)

    servicio = ServicioPedidos(notificador=notificador_inicial, descuento=descuento_inicial)

    # creacion de items del menu
    hamburguesa = Plato(id="P1", nombre="Hamburguesa Doble", precio_base=12.0)
    papas = Plato(id="P2", nombre="Papas Fritas", precio_base=4.0)
    gaseosa = Bebida(id="B1", nombre="Coca Cola", precio_base=2.5, tamanio="M")

    # item tipo Combo
    combo_familiar = Combo(
        id="C1",
        nombre="Combo Familiar",
        items=[hamburguesa, papas, gaseosa],
        descuento_porcentaje=15.0
    )

    #Crear pedidos
    p1 = servicio.crear_pedido(
        cliente="mario",
        items=[(combo_familiar, 1), (gaseosa, 1)]
    )
    print(f"ID: {p1.id} creado para: {p1.cliente} - total con descuento: {servicio.total_con_descuento(p1.id)}")

    p2 = servicio.crear_pedido(
        cliente="carlitos",
        items=[(hamburguesa, 2), (papas, 1)]
    )
    print(f"ID: {p2.id} creado para: {p2.cliente} - total con descuento: {servicio.total_con_descuento(p2.id)}")

    p3 = servicio.crear_pedido(
        cliente="carlitos",
        items=[(papas, 2)]
    )
    print(f"ID: {p3.id} creado para: {p3.cliente} - total con descuento: {servicio.total_con_descuento(p3.id)}")

    #Avanzar un pedido hasta entregaso

    print(f"Estado inicial ={p1.id}: {p1.estado}")
    print(f"Avance 1: {servicio.avanzar_estado(p1.id)}")
    print(f"Avance 2: {servicio.avanzar_estado(p1.id)}")
    print(f"Avance 3: {servicio.avanzar_estado(p1.id)}")

    #intentar avanzar un pedido ya entregado
    try:
        print(f"avanzando pedido: {p1.id} desde el estado '{p1.estado}'")
        servicio.avanzar_estado(p1.id)
    except TransicionInvalida as e:
        print(f"Error: {e}\n")

    #metodos de comprehensions

    #  List
    entregados = servicio.pedidos_por_estado("ENTREGADO")
    recibidos = servicio.pedidos_por_estado("RECIBIDO")
    print(f"Pedidos [ENTREGADOS] : {[p.id for p in entregados]}")
    print(f"Pedidos [RECIBIDOS] : {[p.id for p in recibidos]}")

    # Dict
    conteo_estados = servicio.cantidad_de_pedidos_por_estado()
    print(f"Cantidad de pedidos por estado: {conteo_estados}")

    # Set
    clientes = servicio.clientes_unicos()
    print(f"Conjunto de clientes unicos: {clientes}\n")

    # Cambiamos la dependencia
    servicio_silencioso = ServicioPedidos(
        notificador=NotificadorSilencioso(),
        descuento=DescuentoFijo(porcentaje=10.0)
    )

    p_silencioso = servicio_silencioso.crear_pedido(
        cliente="maradona",
        items=[(hamburguesa, 1)]
    )
    print(f"Pedido #{p_silencioso.id} creado en silencio para {p_silencioso.cliente}.")
