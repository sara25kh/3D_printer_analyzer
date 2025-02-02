from ..gCodeGenerator import GCodeGenerator
from .testCaseBase import TestCaseBase
import math

class SharpEdge(TestCaseBase):
    name = "sharp_edge"
    def __init__(self):
        self.params = {
            "height": {
                "type": "NUMBER",
                "value": 5,
            },
            "length": {
                "type": "NUMBER",
                "value": 20 
            },
            "alpha": {
                "type": "NUMBER",
                "value": 45  # Default angle in degrees
            },
            "bed_temp":{
                "type":"NUMBER",
                "value" : 60
            },
            "nozzle_temp":{
                "type":"NUMBER",
                "value" : 215
            },
            "extrude_flowrate":{
                "type":"NUMBER",
                "value" : 0.07
            }
        }

    def generate_gcode(self):
        gcode_generator = GCodeGenerator()
        gcode_generator.set_start_gcode_list([

            f'M104 S{self.params["nozzle_temp"]["value"]}', # set extruder temp
            f'M140 S{self.params["bed_temp"]["value"]}', # set bed temp
            f'M190 S{self.params["bed_temp"]["value"]}', # wait for bed temp
            f'M109 S{self.params["nozzle_temp"]["value"]}', # wait for extruder temp
            'G28', # home all axes
            'G90', # set to Absolute Positioning
            "G1 Z0.2 F720",
            "G1 Y-3 F1000", # go outside print area
            "G92 E0",
            "G1 X60 E9 F1000", # intro line
            "G1 X100 E12.5 F1000", # intro line
            'G92 E0', # reset extruder
            'G1 Z0.2',
        ])
        print("bed temp:",self.params["bed_temp"]["value"] )
        gcode_generator.set_end_gcode_list([
            'G91', # Set to Relative Positioning Mode
            'G1 Z10', # Raise the nozzle 10mm high
            'M104 S0', # set extruder temp
            'M140 S0', # set bed temp
            'M84', # disable motors
        ])

        gcode_generator.set_extrude_rate(self.params["extrude_flowrate"]["value"])

        start_x = 50
        start_y = 100
        length = self.params["length"]["value"]
        angle_radians = math.radians(self.params["alpha"]["value"])
        print("alpha:",self.params["alpha"]["value"])
        u1 = (1,0)
        u2 = (math.cos(angle_radians), math.sin(angle_radians))

        p1 = (start_x + (length*u1[0]), start_y + (length*u1[1]))
        p2 = (start_x, start_y)
        p3 = (start_x + (length*u2[0]), start_y + (length*u2[1]))
        print("p1:",p1)
        print("p2:",p2)
        print("p3:",p3)
        

        # Move to the starting position
        gcode_generator.move(p1[0], p1[1], 0)

        # Generate GCode for each layer
        while gcode_generator.total_z < self.params["height"]["value"]:
            #We're at p1
            gcode_generator.move_and_extrude(p2[0], p2[1])
            gcode_generator.move_and_extrude(p3[0], p3[1])
            gcode_generator.go_to_next_layer()
            #We're at p3
            gcode_generator.move_and_extrude(p2[0], p2[1])
            gcode_generator.move_and_extrude(p1[0], p1[1])
            gcode_generator.go_to_next_layer()

        return gcode_generator.generate()

    def estimate_print_time(self):
        # Simple estimation logic based on distance and height
        length = self.params["length"]["value"]
        height = self.params["height"]["value"]

        # Calculate distances
        total_distance = length * height

        # Estimate time (in seconds) based on some speed factor, for example, 10 mm/s
        speed = 10
        estimated_time = total_distance / speed

        return estimated_time
# Run test that prints the generated gcode of this class:
if __name__ == '__main__':
    wall_printer = SharpEdge()
    print(wall_printer.generate_gcode())
    # print("Estimated Print Time (seconds):", wall_printer.estimate_print_time())
