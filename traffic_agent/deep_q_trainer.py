from collections import deque
from copy import copy
from time import perf_counter
import torch
from torch.optim import Adam
from torch.nn import MSELoss

from traffic_agent.sumo import Simulation
from traffic_agent.deep_q_agent import DeepQAgent


MAX_ALLOWED_STEPS = 5000
PRINT_EVERY = 250


error = MSELoss()
optimizer = Adam()
episodes = 1000
experience_memory_size = 100_000
batch_size = 16
sync_evey_steps = 1e3
gamma = 0.99
epsilon = 1.0
epsilon_minimum = 0.10
epsilon_minimum_at_episode = 500
learning_rate = 5e-4

# Create our agent
simulation = Simulation("./chicago_02/chicago_02.sumocfg")
simulation.start()
agent = DeepQAgent(simulation)

rewards = []
steps = []

# GPU or CPU?
if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

# This math is derived on the idea that we want the
# decay, over epsilon_minimum_at_episode episodes
# to equal our epsilon minimum.
epsilon_decay = (epsilon_minimum / epsilon) ** (1/epsilon_minimum_at_episode)

experience_memory = deque(maxlen=experience_memory_size)

target_model = copy.deepcopy(agent.model)
target_model.load_state_dict(agent.model.state_dict())
optimizer_steps = 0

# Prepare our optimizer
optimizer = Adam(agent.model.parameters(), lr=learning_rate)

save_every_n_episodes = 100

# Start at episode 0
episode = 0
rewards = []

for episdoe in range(0, episodes):
    simulation.shutdown()
    simulation.start()

    steps = 0
    step_times = 0.0
    while not simulation.complete():
        steps += 1
        if steps % PRINT_EVERY == 0:
            print(f"Step {steps}")
            print(f"Average of {simulation_times/PRINT_EVERY}s per simulation step and {agent_times/PRINT_EVERY}s per agent step")
            simulation_times = 0.0
            agent_times = 0.0
        if steps >= MAX_ALLOWED_STEPS:
            print(f"Exceeded max steps allowed - {MAX_ALLOWED_STEPS}")
            break
    
        # Take a step
        step_start = perf_counter()
        simulation.step()
        agent.step()
        step_end = perf_counter()
        step_times += step_end - step_start

    stats = simulation.get_stats()
    # Now we convert the stats to a reward
    # For now we'll say every 1000 seconds of
    # travel time is -1 reward points
    reward = -1 * (stats["totalTravelTime"]/1000)

    rewards.append(reward)

    if episode + 1 % save_every_n_episodes == 0:
        agent.save(f"model_episode_{episode+1}.pt")
    
    if epsilon > epsilon_minimum:
        epsilon *= epsilon_decay
    else:
        epsilon = epsilon_minimum
    
    