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
            command = self.expand_variables(instructions[0])
            # var = self.get_variable_value("one")
            os.system(command.strip())

    def expand_variables(self, script : str) -> str:
        template_syntax_pattern ='\$\{\{[^}]*\}\}' 
        macro_syntax_pattern = '\$\([^)]*\)'

        var_type = ""
        if re.search(template_syntax_pattern, script):
            var_names = re.finditer(template_syntax_pattern, script)
            var_type = "template" 
        
        elif re.search(macro_syntax_pattern, script):
            var_names = re.finditer(macro_syntax_pattern, script)
            var_type = "macro" 

        values = []
        for name in var_names: 
            print(name.group())
            values.append((name.group(), self.get_variable_value(name.group(), var_type))) #(variable, value) 

        for val in values: 
            script = script.replace(val[0], val[1], 1) 
        return script 

    def get_variable_value(self, string_to_expand, var_type): 
        var_name = ""
        if var_type == "template": 
            var_name = re.findall('\.\S*?(?=\s|\})', string_to_expand)
            var_name = var_name[0].replace(".", "") # findall returns a list so we only care about the first element 
            print(var_name)

        elif var_type == "macro": 
            var_name = re.findall('\(([^)]*)\)', string_to_expand)
            var_name = var_name[0].strip()
            print(var_name)
        for pair in self.variables:
            if pair["name"] == var_name:
                return pair["value"]
        return f"Could not find property variables.{var_name}"
        
file = open("./input.yaml", "r")
file = yaml.safe_load(file)

steps = list(file["steps"][0].items())



inputFile = YamlFile(file["variables"], file["steps"])

inputFile.run_step(steps[0])

