

from traffic_agent.sumo import Simulation

stats = []

for i in range(0,5):
    # simulation = Simulation("./sim/test.sumocfg")
    simulation = Simulation("./chicago/chicago.sumocfg")
    simulation.start()

    while not simulation.complete():
        simulation.step()

    simulation.stop()
    stats.append(simulation.get_stats())
    simulation.shutdown()

print(stats)