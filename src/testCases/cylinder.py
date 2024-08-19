from ..gCodeGenerator import GCodeGenerator
from .testCaseBase import TestCaseBase
import math

class Cylinder(TestCaseBase):
    name = "cylinder"

    def __init__(self):
        self.params = {
            "radius": {
                "type": "NUMBER",
                "value": 10,  # Default radius in mm
            },
            "height": {
                "type": "NUMBER",
                "value": 20,  # Default height in mm
            },
            "bed_temp": {
                "type": "NUMBER",
                "value": 60,
            },
            "nozzle_temp": {
                "type": "NUMBER",
                "value": 215,
            },
            "extrude_flowrate": {
                "type": "NUMBER",
                "value": 0.07,
            },
            "layer_height": {
                "type": "NUMBER",
                "value": 0.2,  # Default layer height in mm
            },
            "circle_resolution": {
                "type": "NUMBER",
                "value": 36,  # Number of segments to approximate the circle
            },
        }

    def generate_gcode(self):
        gcode_generator = GCodeGenerator()
        gcode_generator.set_start_gcode_list([
            f'M104 S{self.params["nozzle_temp"]["value"]}',  # set extruder temp
            f'M140 S{self.params["bed_temp"]["value"]}',  # set bed temp
            'M190 S60',  # wait for bed temp
            'M109 S215',  # wait for extruder temp
            'G28',  # home all axes
            'G90',  # set to Absolute Positioning
            "G1 Z0.2 F720",
            "G1 Y-3 F1000",  # go outside print area
            "G92 E0",
            "G1 X60 E9 F1000",  # intro line
            "G1 X100 E12.5 F1000",  # intro line
            'G92 E0',  # reset extruder
            'G1 Z0.2',
        ])

        gcode_generator.set_end_gcode_list([
            'G91',  # Set to Relative Positioning Mode
            'G1 Z10',  # Raise the nozzle 10mm high
            'M104 S0',  # set extruder temp
            'M140 S0',  # set bed temp
            'M84',  # disable motors
        ])

        gcode_generator.set_extrude_rate(self.params["extrude_flowrate"]["value"])

        radius = self.params["radius"]["value"]
        height = self.params["height"]["value"]
        layer_height = self.params["layer_height"]["value"]
        circle_resolution = self.params["circle_resolution"]["value"]
        angle_increment = 360 / circle_resolution

        start_x = 50  # Start position X
        start_y = 50  # Start position Y

        # Generate GCode for each layer
        while gcode_generator.total_z < height:
            # Start at the top of the cylinder
            gcode_generator.move(start_x + radius, start_y, 0)

            for i in range(circle_resolution):
                angle = math.radians(i * angle_increment)
                x = start_x + radius * math.cos(angle)
                y = start_y + radius * math.sin(angle)
                gcode_generator.move_and_extrude(x, y)

            # Close the loop
            gcode_generator.move_and_extrude(start_x + radius, start_y)
            gcode_generator.go_to_next_layer()

        return gcode_generator.generate()

    def estimate_print_time(self):
        # Simple estimation logic based on circumference, height, and number of layers
        radius = self.params["radius"]["value"]
        height = self.params["height"]["value"]
        layer_height = self.params["layer_height"]["value"]

        # Calculate the circumference of the circle
        circumference = 2 * math.pi * radius

        # Calculate the total distance extruded
        total_distance = circumference * (height / layer_height)

        # Estimate time (in seconds) based on some speed factor, for example, 10 mm/s
        speed = 10
        estimated_time = total_distance / speed

        return estimated_time

# Run test that prints the generated gcode of this class:
if __name__ == '__main__':
    cylinder_printer = Cylinder()
    print(cylinder_printer.generate_gcode())
    # print("Estimated Print Time (seconds):", cylinder_printer.estimate_print_time())
