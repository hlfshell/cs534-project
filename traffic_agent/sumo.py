from os import remove
import sys
import traci
from sumolib import checkBinary
import xml.etree.ElementTree as ET
from os.path import dirname, join


class Simulation():

    def __init__(
        self,
        simulation_config: str
    ):
        self.binary = checkBinary('sumo')
        self.simulation_config = simulation_config
        self.steps = 0
        self.stats_file = self.get_stats_file()
    
    def get_stats_file(self):
        tree = ET.parse(self.simulation_config)
        root = tree.getroot()
        for item in root.findall("output/statistic-output"):
            filepath = item.get("value")
            dirpath = dirname(self.simulation_config)
            return join(dirpath, filepath)


    def start(self):
        traci.start([self.binary, "-c", self.simulation_config])

    def step(self):
        traci.simulationStep()
        self.steps += 1

    def complete(self) -> bool:
        return not traci.simulation.getMinExpectedNumber() > 0

    def stop(self):
        traci.close()

    def shutdown(self):
        # Erase stats if it exists
        try:
            self.stop()
        except:
            pass
        remove(self.stats_file)
        sys.stdout.flush()

    def get_stats(self):
        tree = ET.parse(self.stats_file)
        root = tree.getroot()

        for item in root.findall("vehicleTripStatistics"):
            stats = {}
            stats['totalTravelTime'] = item.get('totalTravelTime')
            stats['routeLength'] = item.get('routeLength')
            stats['speed'] = item.get('speed')
            stats['waiting'] = item.get('waiting')
            stats['timeLoss'] = item.get('timeLoss')
            stats['departDelay'] = item.get('departDelay')
            stats['departDelayWaiting'] = item.get('departDelayWaiting')
            stats['totalDepartDelay'] = item.get('totalDepartDelay')

            return stats
