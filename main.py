import yaml
from typing import Tuple, List, Dict
import os
import re

class YamlFile(): 
    def __init__(self, variables: List[Dict[str, str]], steps) -> None:
        self.variables = variables 
        self.steps = steps


    def run_step(self, step : Tuple[str, str]): 
        if step[0] == "script":
            instructions = step[1].strip().split("\n")
            self.expand_variables(instructions[0])
            var = self.get_variable_value("one")
            command = instructions[0].split(" ")[0] + " " +  var
            os.system(command)

    def expand_variables(self, script : str):
        var_names = re.finditer('(v[^}\s]+)', script)
        values = []
        for name in var_names: 
            print(name.span())
            values.append(self.get_variable_value(name.group().split(".")[1])) 
        print(values) 
    
    def get_variable_value(self, var_name):
        for pair in self.variables:
            if pair["name"] == var_name:
                return pair["value"]
        return f"Could not find property variables.{var_name}"
        
file = open("./input.yaml", "r")


file = yaml.safe_load(file)

print(file["variables"])

# print(file["steps"][0].items())

steps = list(file["steps"][0].items())

# print(steps)


inputFile = YamlFile(file["variables"], file["steps"])

inputFile.run_step(steps[0])

