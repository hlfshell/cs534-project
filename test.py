

from traffic_agent.sumo import Simulation

simulation = Simulation("./sim/test.sumocfg")
print(simulation.get_stats())