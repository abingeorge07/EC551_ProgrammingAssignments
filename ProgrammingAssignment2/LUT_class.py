import sympy as sp
import sympy.logic as logic
import random
import re

# Updated SOP Conversion Function
from sympy.logic.inference import satisfiable

class LUT_class:
    def __init__(self, num_inputs, logic_expression=None):
        self.num_inputs = num_inputs
        self.logic_expression = logic_expression
        self.connections = []

    def connect_to(self, other_LUT):
        self.connections.append(other_LUT)

class FPGA:
    def __init__(self, num_LUTs, lut_type, connectivity):
        self.luts = [LUT_class(lut_type) for _ in range(num_LUTs)]
        self.connectivity = connectivity
        self.external_inputs = {}
        self.external_outputs = {}

        if self.connectivity == 'fully':
            self.fully_connect()
        elif self.connectivity == 'partially':
            self.setup_partial_connectivity()

    def fully_connect(self):
        for lut in self.luts:
            lut.connections = [other_lut for other_lut in self.luts if other_lut != lut]

    def setup_partial_connectivity(self):
        for i in range(len(self.luts) - 1):
            self.luts[i].connect_to(self.luts[i + 1])

    def map_logic_expressions(self, logic_expressions):
        for i, expression in enumerate(logic_expressions):
            if i < len(self.luts):
                self.luts[i].logic_expression = expression
            else:
                print(f"Warning: Not enough LUTs to map expression: {expression}")

    def show_internal_connections(self):
        print("Internal Connections:")
        for i, lut in enumerate(self.luts):
            connected_to = ', '.join([f'LUT {self.luts.index(conn)}' for conn in lut.connections])
            print(f'LUT {i} -> {connected_to or "None"}')

    def assign_random_external_io(self, num_vars):
        self.external_inputs = {chr(65 + i): random.randint(0, self.luts[0].num_inputs - 1) for i in range(num_vars)}
        self.external_outputs = {i: f'LUT {random.randint(0, len(self.luts) - 1)}' for i in range(num_vars)}

    def show_external_io(self):
        print("External Input Assignments:")
        for var, input_num in self.external_inputs.items():
            print(f'Variable {var} -> Input {input_num}')

        print("External Output Assignments:")
        for output_num, lut_name in self.external_outputs.items():
            print(f'Output {output_num} -> {lut_name}')

    def show_all_lut_assignments(self):
        print("All LUT Assignments:")
        for i, lut in enumerate(self.luts):
            print(f"LUT {i}: Expression = {lut.logic_expression or 'Not Assigned'}")
    
    def setup_custom_connectivity(self):

        for i in range(len(self.luts)):
            connections = input(f"Enter connections for LUT {i} (as indices separated by spaces): ")
            self.luts[i].connections = [self.luts[int(index)] for index in connections.split() if int(index) != i]



# Function to format expressions
def format_expression(expression):
    # Remove outer brackets if present
    expression = expression.strip('[]')

    # Split the expression into individual terms
    terms = expression.split('|')
    
    # Format each term
    formatted_terms = []
    for term in terms:
        # Remove spaces and keep logical operators adjacent to variables
        formatted_term = term.replace(' ', '').replace('&', '').strip()
        formatted_terms.append(formatted_term)

    return formatted_terms