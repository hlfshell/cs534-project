
from traffic_agent.null_agent import NullAgent
from traffic_agent.sumo import Simulation

simulation = Simulation("./chicago/chicago.sumocfg")
simulation.start()
agent = NullAgent()

agent.execute(simulation)