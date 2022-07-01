

from traffic_agent.sumo import Simulation

simulation = Simulation("./sim/test.sumocfg")
simulation.start()

while not simulation.complete():
    simulation.step()

simulation.stop()
print(simulation.get_stats())
simulation.shutdown()