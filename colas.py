import random
import simpy

# FALTA VARIAR LOS PARAMETROS DE TASA DE LLEGADA Y TASA DE SERVICIO

# Parámetros
tasa_llegada = 0.5
tasa_servicio = 0.8
tiempo_simulacion = 100


# configuración de la simulación
env = simpy.Environment()
cola = simpy.Store(env)
servidor = simpy.Resource(env, capacity=1)
num_clientes = 0
tiempo_espera_total = 0


# genera las llegadas al sistema
def llegada():
    global num_clientes
    while True:
        yield env.timeout(random.expovariate(tasa_llegada))
        num_clientes += 1
        cliente = (num_clientes, env.now)
        env.process(servicio(cliente))


# genera los tiempos de atencion en el servidor
def servicio(cliente):
    global tiempo_espera_total
    with servidor.request() as request:
        yield request
        tiempo_espera = env.now - cliente[1]
        tiempo_espera_total += tiempo_espera
        yield env.timeout(random.expovariate(tasa_servicio))


# corre la simulación
def correr_simulacion(tiempo_simulacion):
    env.process(llegada())
    env.run(until=tiempo_simulacion)
    tiempo_espera_promedio = tiempo_espera_total / num_clientes  # en cola
    print(f"Tiempo de espera promedio: {tiempo_espera_promedio:.2f}")


correr_simulacion(tiempo_simulacion)

# Medidas de desempeño
utilizacion_servidor = tasa_llegada / tasa_servicio
print(f"Utilizacion del servidor: {utilizacion_servidor:.2f}")

clientes_promedio_en_sistema = tasa_llegada * tiempo_espera_total
print(f"Numero promedio de clientes en el sistema: {clientes_promedio_en_sistema:.2f}")

clientes_promedio_en_cola = (utilizacion_servidor**2) / (1 - utilizacion_servidor)
print(f"Numero promedio de clientes en la cola: {clientes_promedio_en_cola:.2f}")

tiempo_promedio_en_sistema = tiempo_espera_total / num_clientes + 1 / tasa_servicio
print(f"Tiempo promedio en el sistema: {tiempo_promedio_en_sistema:.2f}")

tiempo_promedio_en_cola = tiempo_espera_total / num_clientes
print(f"Tiempo promedio en cola: {tiempo_promedio_en_cola:.2f}")


# calcula la probabilidad de que haya n clientes en cola en un deteminado momento
def probabilidad_n_clientes_en_cola(n):
    return (tasa_llegada / tasa_servicio) ** n * (1 - (tasa_llegada / tasa_servicio))


probabilidad_2_clientes_en_cola = probabilidad_n_clientes_en_cola(2)
print(
    f"Probabilidad de que haya 2 clientes en cola: {probabilidad_2_clientes_en_cola:.2f}"
)

# calcula la probabilidad de denegar servicio para distintos tamaños de la cola
tamanios_cola = [0, 2, 5, 10, 50]
for tam in tamanios_cola:
    acum = 0
    for i in range(tam):
        acum += probabilidad_n_clientes_en_cola(i)
    probabilidad_denegacion_servicio = 1 - acum
    print(
        f"Probabilidad de denegación de servicio para una cola de tamaño {tam}: {probabilidad_denegacion_servicio:.2f}"
    )
