import yaml
from typing import Tuple
import os 

class YamlFile(): 
    def __init__(self, variables, steps) -> None:
        self.variables = variables
        self.steps = steps


    def run_step(self, step : Tuple[str, str]): 
        if step[0] == "script":
            instructions = step[1].strip().split("\n")
            command = instructions[0].split(" ")[0] + " " +  self.variables[0]["value"]
            os.system(command)


file = open("./input.yaml", "r")


file = yaml.safe_load(file)

# print(type(file["variables"][0]))

# print(file["steps"][0].items())

steps = list(file["steps"][0].items())

# print(steps)

inputFile = YamlFile(file["variables"], file["steps"])

inputFile.run_step(steps[0])

