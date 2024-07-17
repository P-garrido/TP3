import random

# FALTA VARIAR LOS PARAMETROS DE NIVEL MINIMO DE INVENTARIO Y CANTIDAD PEDIDA

# parámetros
tiempo_simulacion = 50
demanda_promedio = 70
demanda_desviacion = 12
tiempo_arribo_pedido_promedio = 2
tiempo_arribo_pedido_desviacion = 0.5
inventario_inicial = 200
limite_pedido = 50
cantidad_pedida = 150

# costos
costo_unitario = 50
costo_preparacion = 20
costo_shortage = 100
costo_holding = 10

# inicializamos variables
costo_mantenimiento_final = 0
costo_por_faltante_final = 0
demora_hasta_proximo_pedido = None

# Corrida de la simulación
inventario = inventario_inicial
demanda_total = 0
nro_pedidos = 0

for _ in range(tiempo_simulacion):
    demanda = max(0, int(random.normalvariate(demanda_promedio, demanda_desviacion)))

    # paso del tiempo actualiza tiempos de arribo
    if demora_hasta_proximo_pedido is not None:
        demora_hasta_proximo_pedido -= 1

    # llego un pedido?
    if demora_hasta_proximo_pedido is not None and demora_hasta_proximo_pedido == 0:

        inventario += cantidad_pedida
        print("llego un pedido")
        demora_hasta_proximo_pedido = None

    # hace falta un pedido?
    tiempo_arribo_pedido = 0
    if inventario <= limite_pedido:
        # no se realiza un pedido si ya se realizo uno
        if (
            demora_hasta_proximo_pedido is None
        ):  #  no hay pedidos sin agregar al inventario
            print("realice un pedido")
            tiempo_arribo_pedido = max(
                1,
                int(
                    random.normalvariate(
                        tiempo_arribo_pedido_promedio, tiempo_arribo_pedido_desviacion
                    )
                ),
            )
            demora_hasta_proximo_pedido = tiempo_arribo_pedido
            nro_pedidos += 1
    # actualizar inventario
    inventario -= demanda
    demanda_total += demanda
    print(
        f"Inventario: {inventario}, Demanda: {demanda}, Tiempo de arribo del pedido: {tiempo_arribo_pedido}"
    )

    # Actualizar costos
    costo_mantenimiento_final += max(0, inventario * costo_holding)
    costo_por_faltante_final += (
        max(0, -inventario) * costo_shortage
    )  # es un costo positivo si hay faltante

print(f"Demanda Total: {demanda_total}")
print(f"Cantidad de pedidos realizados: {nro_pedidos}")

# Medidas de desempeño
costo_por_pedidos = costo_unitario * nro_pedidos + costo_preparacion
costo_total = costo_por_pedidos + costo_mantenimiento_final + costo_por_faltante_final


print(f"Costo por pedidos: {costo_por_pedidos}")
print(f"Costos de mantenimiento: {costo_mantenimiento_final}")
print(f"Costos por faltante: {costo_por_faltante_final}")
print(f"Costos totales: {costo_total}")
