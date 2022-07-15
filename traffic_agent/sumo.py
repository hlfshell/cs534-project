from os import remove
import os
import sys
from typing import Any, Dict, List
from os.path import dirname, join
sys.path.append(os.path.join(os.environ.get("SUMO_HOME"), 'tools'))

import traci
from sumolib import checkBinary
import xml.etree.ElementTree as ET
from os.path import dirname, join


class Simulation():

    def __init__(
        self,
        simulation_config: str,
        gui: bool = False
    ):
        if gui:
            self.binary = checkBinary('sumo-gui')
        else:
            self.binary = checkBinary('sumo')
        self.simulation_config = simulation_config
        self.steps = 0
        self.stats_file = self.get_stats_file()
        self.osm_file = self.get_osm_file()
        self.running = False
    
    def get_stats_file(self):
        tree = ET.parse(self.simulation_config)
        root = tree.getroot()
        for item in root.findall("output/statistic-output"):
            filepath = item.get("value")
            dirpath = dirname(self.simulation_config)
            return join(dirpath, filepath)

    def get_osm_file(self):
        tree = ET.parse(self.simulation_config)
        root = tree.getroot()
        for item in root.findall("input/net-file"):
            filepath = item.get("value")
            dirpath = dirname(self.simulation_config)
            return join(dirpath, filepath)

    def start(self):
        if self.running:
            return
        traci.start([self.binary, "-c", self.simulation_config, "--no-warnings"])
        self.running = True

    def step(self):
        traci.simulationStep()
        self.steps += 1

    def complete(self) -> bool:
        return not traci.simulation.getMinExpectedNumber() > 0

    def stop(self):
        if not self.running:
            return
        self.running = False
        traci.close()

    def shutdown(self):
        # Erase stats if it exists
        try:
            self.stop()
            remove(self.stats_file)
        except:
            pass
        sys.stdout.flush()

    def get_detector_ids(self) -> List[str]:
        return traci.inductionloop.getIDList()
    
    def get_detectors(self) -> Dict[str, Dict[str, float]]:
        detectors: Dict[str, Dict[str, float]] = {}
        for id in self.get_detector_ids():
            speed: float = traci.inductionloop.getLastStepMeanSpeed(id)
            occupancy: float = traci.inductionloop.getLastStepOccupancy(id)

            detectors[id] = {
                "speed": speed,
                "occupancy": occupancy
            }

        return detectors     


    def get_traffic_light_ids(self) -> List[str]:
        return traci.trafficlight.getIDList()

    def get_traffic_lights(self) -> Dict[str, Dict[str, Any]]:
        lights: Dict[str, Dict[str, Any]] = {}
        for id in self.get_traffic_light_ids():
            phase = traci.trafficlight.getPhase(id)
            duration = traci.trafficlight.getNextSwitch(id)-traci.simulation.getTime()
            state = traci.trafficlight.getRedYellowGreenState(id)

            lights[id] = {
                "phase": phase,
                "duration": duration,
                "state": state
            }
        
        return lights
    
    def get_traffic_light_phase(self, id: str):
        return traci.trafficlight.getPhase(id)

    def set_traffic_light_duration(self, id:str, duration: int):
        traci.trafficlight.setPhaseDuration(id, duration)

    def get_stats(self):
        tree = ET.parse(self.stats_file)
        root = tree.getroot()

        for item in root.findall("vehicleTripStatistics"):
            stats = {}
            stats['totalTravelTime'] = float(item.get('totalTravelTime'))
            stats['routeLength'] = float(item.get('routeLength'))
            stats['speed'] = float(item.get('speed'))
            # stats['waiting'] = float(item.get('waiting'))
            stats['timeLoss'] = float(item.get('timeLoss'))
            stats['departDelay'] = float(item.get('departDelay'))
            stats['departDelayWaiting'] = float(item.get('departDelayWaiting'))
            stats['totalDepartDelay'] = float(item.get('totalDepartDelay'))

            return stats

    def get_light_durations(self):
        tree = ET.parse(self.osm_file)
        root = tree.getroot()
        
        lights = {}

        for item in root.findall("tlLogic"):
            id = item.get("id")
            phases = []
            for phase in item.findall("phase"):
                phases.append({
                    "duration": phase.get("duration"),
                    "min_duration": phase.get("maxDur"),
                    "max_duration": phase.get("maxDur")
                })
            lights[id] = phases
        
        return lights
        