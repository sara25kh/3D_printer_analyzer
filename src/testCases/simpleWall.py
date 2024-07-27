from ..gCodeGenerator import GCodeGenerator
from .testCaseBase import TestCaseBase

class SimpleWall(TestCaseBase):
    name = "simple_wall"
    def __init__(self):
        self.params = {
            "length": {
                "type": "NUMBER",
                "value": 50
            },
            "height": {
                "type": "NUMBER",
                "value": 5,
                "unit":"mm"
            }
        }

    def generate_gcode(self):
        gcode_generator = GCodeGenerator()
        gcode_generator.set_start_gcode_list([

            'M104 S215', # set extruder temp
            'M140 S60', # set bed temp
            'M190 S60', # wait for bed temp
            'M109 S215', # wait for extruder temp
            'G28', # home all axes
            'G90', # set to Absolute Positioning
            'G92 E0', # reset extruder
            'G1 Z0.2',
        ])

        gcode_generator.set_end_gcode_list([
            'M104 S0', # set extruder temp
            'M140 S0', # set bed temp
            'G91', # Set to Relative Positioning Mode
            'G1 Z10', # Raise the nozzle 10mm high
            'M84', # disable motors
        ])

        start_x = 50
        start_y = 100
        length = self.params["length"]["value"]

        gcode_generator.move(start_x, start_y, 0)
        # gcode_generator.set_extrude_rate(0)

        # Move to the starting position
        gcode_generator.move(start_x, start_y)

        # Generate GCode for each layer
        while gcode_generator.total_z < self.params["height"]["value"]:
            gcode_generator.move_and_extrude(start_x + length, start_y)
            gcode_generator.go_to_next_layer()
            gcode_generator.move_and_extrude(start_x, start_y)
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
    wall_printer = SimpleWall()
    print(wall_printer.generate_gcode())
    # print("Estimated Print Time (seconds):", wall_printer.estimate_print_time())
