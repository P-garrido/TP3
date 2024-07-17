import random
import simpy

class MM1Queue:
  def __init__(self, env, arrival_rate, service_rate):
    self.env = env
    self.arrival_rate = arrival_rate
    self.service_rate = service_rate
    self.queue = simpy.Store(env)
    self.server = simpy.Resource(env, capacity=1)
    self.num_customers = 0
    self.total_waiting_time = 0

  def arrival_process(self):
    while True:
      yield self.env.timeout(random.expovariate(self.arrival_rate))
      self.num_customers += 1
      customer = (self.num_customers, self.env.now)
      self.env.process(self.service_process(customer))

  def service_process(self, customer):
    with self.server.request() as request:
      yield request
      wait_time = self.env.now - customer[1]
      self.total_waiting_time += wait_time
      yield self.env.timeout(random.expovariate(self.service_rate))

  def run_simulation(self, sim_time):
    self.env.process(self.arrival_process())
    self.env.run(until=sim_time)

    avg_waiting_time = self.total_waiting_time / self.num_customers
    print(f"Average waiting time: {avg_waiting_time:.2f} units")

# Parameters
arrival_rate = 0.5  # Mean inter-arrival time
service_rate = 0.8  # Mean service time
sim_time = 100  # Simulation time

# Create simulation environment
env = simpy.Environment()

# Create MM1 queue
mm1_queue = MM1Queue(env, arrival_rate, service_rate)

# Run simulation
mm1_queue.run_simulation(sim_time)

# Calculate average number of customers in the system
avg_customers_in_system = mm1_queue.total_waiting_time / sim_time
print(f"Average number of customers in the system: {avg_customers_in_system:.2f}")

# Calculate average number of customers in the queue
avg_customers_in_queue = mm1_queue.total_waiting_time / sim_time * arrival_rate
print(f"Average number of customers in the queue: {avg_customers_in_queue:.2f}")

# Calculate average time in the system
avg_time_in_system = mm1_queue.total_waiting_time / mm1_queue.num_customers + (1 / service_rate)
print(f"Average time in the system: {avg_time_in_system:.2f} units")

# Calculate average time in the queue
avg_time_in_queue = mm1_queue.total_waiting_time / mm1_queue.num_customers
print(f"Average time in the queue: {avg_time_in_queue:.2f} units")

# Calculate server utilization
server_utilization = mm1_queue.total_waiting_time / sim_time * service_rate
print(f"Server utilization: {server_utilization:.2f}")

# Calculate probability of finding n customers in the queue
def probability_of_n_customers_in_queue(n):
  return (arrival_rate / service_rate) ** n * (1 - (arrival_rate / service_rate))
n = 2  # Number of customers in the queue
prob_n_customers_in_queue = probability_of_n_customers_in_queue(n)
print(f"Probability of finding {n} customers in the queue: {prob_n_customers_in_queue:.2f}")

# Calculate probability of denial of service for different queue sizes
queue_sizes = [0, 2, 5, 10, 50]
for size in queue_sizes:
  prob_denial_of_service = (arrival_rate / service_rate) ** (size + 1)
  print(f"Probability of denial of service for queue size {size}: {prob_denial_of_service:.2f}")

