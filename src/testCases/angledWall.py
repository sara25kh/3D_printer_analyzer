from ..gCodeGenerator import GCodeGenerator
import math
from .testCaseBase import TestCaseBase

class AngledWall(TestCaseBase):
    name = "angled_wall"
    def __init__(self):
        self.params = {
            "length": {
                "type": "NUMBER",
                "value": 50
            },
            "height": {
                "type": "NUMBER",
                "value": 5
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
                "value" : 0.5
            }
        }

    def generate_gcode(self):
        gcode_generator = GCodeGenerator()
        gcode_generator.set_start_gcode_list([

            f'M104 S{self.params["nozzle_temp"]["value"]}', # set extruder temp
            f'M140 S{self.params["bed_temp"]["value"]}', # set bed temp
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

        gcode_generator.set_extrude_rate(self.params["extrude_flowrate"]["value"])

        start_x = 50
        start_y = 100
        length = self.params["length"]["value"]
        alpha = self.params["alpha"]["value"]
        height = self.params["height"]["value"]

        angle_radians = math.radians(alpha)
        # dx = length * math.cos(angle_radians)
        # dy = length * math.sin(angle_radians)

        gcode_generator.move(start_x, start_y, 0)
        # gcode_generator.set_extrude_rate(0)
        dy = gcode_generator.layer_height / math.tan(angle_radians)
        print('dy=' , dy)
        print('tan = ', math.tan(angle_radians))
        # Move to the starting position
        gcode_generator.move(start_x - 5 , start_y + 10)
        x = start_x - 5
        y = start_y + 10
        dx = 0.4
        counter = 4
        while counter > 0 :
            if counter % 2 == 0:
                y = start_y + 10
                while x < (start_x + length + 10):
                    gcode_generator.move_and_extrude(x + dx, y)
                    gcode_generator.move_and_extrude(x + dx , y - 20)
                    gcode_generator.move_and_extrude(x + (2 * dx) , y - 20)
                    gcode_generator.move_and_extrude(x + (2 * dx) , y)
                    x = (2 * dx) + x
            else :
                x = start_x -5 
                while y > start_y -10:
                    gcode_generator.move_and_extrude(x , y - dx)
                    gcode_generator.move_and_extrude(x + length + 10, y - dx)
                    gcode_generator.move_and_extrude(x + length + 10, y - (2*dx))
                    gcode_generator.move_and_extrude(x , y - (2*dx))
                    y = y - (2 * dx)

            counter -= 1
            gcode_generator.go_to_next_layer()        
        # gcode_generator.move_and_extrude(start_x -5 + dx, )
        # gcode_generator.move_and_extrude(start_x -10 , start_y + 10)
        # gcode_generator.move_and_extrude(start_x + 20 + length , start_y + 10)
        # gcode_generator.move_and_extrude(start_x + 20 + length , start_y - 20 )
        # gcode_generator.move_and_extrude(start_x -10 , start_y - 10)

        # Generate GCode for each layer
        while gcode_generator.total_z < height:
            gcode_generator.move_and_extrude(start_x + length, start_y )
            gcode_generator.go_to_next_layer()
            gcode_generator.move_and_extrude(start_x + length, start_y + dy)
            gcode_generator.move_and_extrude(start_x , start_y + dy)
            gcode_generator.go_to_next_layer()
            start_y = start_y + dy

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
    wall_printer = AngledWall()
    print(wall_printer.generate_gcode())
    # print("Estimated Print Time (seconds):", wall_printer.estimate_print_time())
