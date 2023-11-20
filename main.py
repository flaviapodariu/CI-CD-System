import yaml
from typing import Tuple, List, Dict
import os
import re

class Job(): 
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

        template_vars = []
        macro_vars = []
        if re.search(template_syntax_pattern, script):
            template_vars = re.finditer(template_syntax_pattern, script)
        
        if re.search(macro_syntax_pattern, script):
            macro_vars = re.finditer(macro_syntax_pattern, script)

        values = []
        for name in template_vars: 
            values.append((name.group(), self.get_variable_value(name.group(), "template"))) #(variable, value) 

        for name in macro_vars: 
            values.append((name.group(), self.get_variable_value(name.group(), "macro"))) #(variable, value) 

        for val in values: 
            script = script.replace(val[0], val[1], 1) 
        return script 

    def get_variable_value(self, string_to_expand, var_type): 
        var_name = ""
        if var_type == "template": 
            var_name = re.findall('\.\S*?(?=\s|\})', string_to_expand)
            var_name = var_name[0].replace(".", "") # findall returns a list so we only care about the first element 

        elif var_type == "macro": 
            var_name = re.findall('\(([^)]*)\)', string_to_expand)
            var_name = var_name[0].strip()
        for pair in self.variables:
            if pair["name"] == var_name:
                return pair["value"]
        return f"Could not find property variables.{var_name}"
        
file = open("./input.yaml", "r")
file = yaml.safe_load(file)

steps = list(file["steps"][0].items())



inputFile = Job(file["variables"], file["steps"])

inputFile.run_step(steps[0])

