import random
import simpy

# Parameters
tasa_llegada = 0.5  # Mean inter-arrival time
tasa_servicio = 0.8  # Mean service time
tiempo_simulacion = 100  # Simulation time

env = simpy.Environment()

cola = simpy.Store(env)
servidor = simpy.Resource(env, capacity=1)
num_clientes = 0
tiempo_espera_total = 0


def llegada():
    global num_clientes
    while True:
        yield env.timeout(random.expovariate(tasa_llegada))
        num_clientes += 1
        cliente = (num_clientes, env.now)
        env.process(servicio(cliente))


def servicio(cliente):
    global tiempo_espera_total
    with servidor.request() as request:
        yield request
        tiempo_espera = env.now - cliente[1]
        tiempo_espera_total += tiempo_espera
        yield env.timeout(random.expovariate(tasa_servicio))


def correr_simulacion(tiempo_simulacion):
    env.process(llegada())
    env.run(until=tiempo_simulacion)

    tiempo_espera_promedio = tiempo_espera_total / num_clientes
    print(f"Tiempo de espera promedio: {tiempo_espera_promedio:.2f}")


# Run simulation
correr_simulacion(tiempo_simulacion)

# Calculate average number of customers in the system
clientes_promedio_en_sistema = tiempo_espera_total / tiempo_simulacion
print(f"Numero promedio de clientes en el sistema: {clientes_promedio_en_sistema:.2f}")

# Calculate average number of customers in the queue
clientes_promedio_en_cola = tiempo_espera_total / tiempo_simulacion * tasa_llegada
print(f"Numero promedio de clientes en la cola: {clientes_promedio_en_cola:.2f}")

# Calculate average time in the system
tiempo_promedio_en_sistema = tiempo_espera_total / num_clientes + (1 / tasa_servicio)
print(f"Tiempo promedio en el sistema: {tiempo_promedio_en_sistema:.2f}")

# Calculate average time in the queue
tiempo_promedio_en_cola = tiempo_espera_total / num_clientes
print(f"Tiempo promedio en cola: {tiempo_promedio_en_cola:.2f}")

# Calculate server utilization
utilizacion_servidor = tiempo_espera_total / tiempo_simulacion * tasa_servicio
print(f"Utilizacion del servidor: {utilizacion_servidor:.2f}")


# Calculate probability of finding n customers in the queue
def probabilidad_n_clientes_en_cola(n):
    return (tasa_llegada / tasa_servicio) ** n * (1 - (tasa_llegada / tasa_servicio))


n = 2  # Number of customers in the queue
probabilidad_2_clientes_en_cola = probabilidad_n_clientes_en_cola(n)
print(
    f"Probabilidad de que haya {n} clientes en cola: {probabilidad_2_clientes_en_cola:.2f}"
)

# Calculate probability of denial of service for different queue sizes
tamanios_cola = [0, 2, 5, 10, 50]
for tam in tamanios_cola:
    probabilidad_denegacion_servicio = (tasa_llegada / tasa_servicio) ** (tam + 1)
    print(
        f"Probabilidad de denegación de servicio para una cola de tamanio {tam}: {probabilidad_denegacion_servicio:.2f}"
    )
