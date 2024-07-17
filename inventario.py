import random

# Define the parameters
demand_mean = 100  # Mean demand per time period
demand_std = 20  # Standard deviation of demand per time period
lead_time_mean = 2  # Mean lead time
lead_time_std = 0.5  # Standard deviation of lead time
initial_inventory = 100  # Initial inventory level
reorder_point = 50  # Reorder point
order_quantity = 100  # Order quantity

# Simulate the inventory model
inventory = initial_inventory
total_demand = 0
total_orders = 0

while inventory > 0:
  # Generate demand and lead time
  demand = max(0, int(random.normalvariate(demand_mean, demand_std)))
  lead_time = max(0, random.normalvariate(lead_time_mean, lead_time_std))
  
  # Check if reorder is needed
  if inventory <= reorder_point:
    inventory += order_quantity
    total_orders += 1
  
  # Update inventory level
  inventory -= demand
  total_demand += demand
  
  # Print current inventory status
  print(f"Inventory: {inventory}, Demand: {demand}, Lead Time: {lead_time}")

# Print simulation results
print(f"Total demand: {total_demand}")
print(f"Total orders placed: {total_orders}")


# Calculate performance measures
order_cost = total_orders * order_quantity
maintenance_cost = (initial_inventory + total_orders * order_quantity) / 2
shortage_cost = total_demand - initial_inventory
total_cost = order_cost + maintenance_cost + shortage_cost

# Print performance measures
print(f"Order cost: {order_cost}")
print(f"Maintenance cost: {maintenance_cost}")
print(f"Shortage cost: {shortage_cost}")
print(f"Total cost: {total_cost}")