from ..gCodeGenerator import GCodeGenerator
from .testCaseBase import TestCaseBase
import math

class TwoColumn(TestCaseBase):
    name = "two_column"
    def __init__(self):
        self.params = {
            "height": {
                "type": "NUMBER",
                "value": 10,
            },
            "distance": {
                "type": "NUMBER",
                "value": 20 
            },
            "side": {
                "type": "NUMBER",
                "value": 5  # Default angle in degrees
            },
            "retraction":{
                "type":"NUMBER",
                "value" : 5
            },
            "retraction_prime":{
                "type":"NUMBER",
                "value" : 4
            },
            "retraction_jump":{
                "type":"NUMBER",
                "value" : 0.5
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
            'M190 S60', # wait for bed temp
            'M109 S215', # wait for extruder temp
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

        gcode_generator.set_end_gcode_list([
            'G91', # Set to Relative Positioning Mode
            'G1 Z10', # Raise the nozzle 10mm high
            'M104 S0', # set extruder temp
            'M140 S0', # set bed temp
            'M84', # disable motors
        ])

        gcode_generator.set_extrude_rate(self.params["extrude_flowrate"]["value"])

        distance = self.params["distance"]["value"]
        height = self.params["height"]["value"]
        size = self.params["size"]["value"]
        retraction = self.params["retraction"]["value"]
        retraction_prime = self.params["retraction_prime"]["value"]
        retraction_jump = self.params["retraction_jump"]["value"]
        center_dist = distance + size
        center1_x = 100 - (center_dist/2)
        cetner1_y = 100
        center2_x = 100 + (center_dist/2)
        cetner2_y = 100

        # Generate GCode for each layer
        while gcode_generator.total_z < height:
            tmp_size = (height - gcode_generator.total_z) * size / height

            p1 = (center1_x + (tmp_size/2), cetner1_y + (tmp_size/2))
            p2 = (center1_x + (tmp_size/2), cetner1_y - (tmp_size/2))
            p3 = (center1_x - (tmp_size/2), cetner1_y - (tmp_size/2))
            p4 = (center1_x - (tmp_size/2), cetner1_y + (tmp_size/2))

            p5 = (center2_x + (tmp_size/2), cetner2_y + (tmp_size/2))
            p6 = (center2_x + (tmp_size/2), cetner2_y - (tmp_size/2))
            p7 = (center2_x - (tmp_size/2), cetner2_y - (tmp_size/2))
            p8 = (center2_x - (tmp_size/2), cetner2_y + (tmp_size/2))

            gcode_generator.move(p1[0], p1[1], 0)
            gcode_generator.move_and_extrude(p2[0], p2[1])
            gcode_generator.move_and_extrude(p3[0], p3[1])
            gcode_generator.move_and_extrude(p4[0], p4[1])
            gcode_generator.move_and_extrude(p1[0], p1[1])

            gcode_generator.retract(retraction, retraction_jump)
            gcode_generator.move(p5[0], p5[1], 0)
            gcode_generator.retract(-retraction_prime, -retraction_jump)
            gcode_generator.move_and_extrude(p6[0], p6[1])
            gcode_generator.move_and_extrude(p7[0], p7[1])
            gcode_generator.move_and_extrude(p8[0], p8[1])
            gcode_generator.move_and_extrude(p5[0], p5[1])
            gcode_generator.go_to_next_layer()

            p1 = (center1_x + (tmp_size/2), cetner1_y + (tmp_size/2))
            p2 = (center1_x + (tmp_size/2), cetner1_y - (tmp_size/2))
            p3 = (center1_x - (tmp_size/2), cetner1_y - (tmp_size/2))
            p4 = (center1_x - (tmp_size/2), cetner1_y + (tmp_size/2))

            p5 = (center2_x + (tmp_size/2), cetner2_y + (tmp_size/2))
            p6 = (center2_x + (tmp_size/2), cetner2_y - (tmp_size/2))
            p7 = (center2_x - (tmp_size/2), cetner2_y - (tmp_size/2))
            p8 = (center2_x - (tmp_size/2), cetner2_y + (tmp_size/2))

            gcode_generator.move_and_extrude(p6[0], p6[1])
            gcode_generator.move_and_extrude(p7[0], p7[1])
            gcode_generator.move_and_extrude(p8[0], p8[1])
            gcode_generator.move_and_extrude(p5[0], p5[1])

            gcode_generator.retract(retraction, retraction_jump)
            gcode_generator.move(p1[0], p1[1], 0)
            gcode_generator.retract(-retraction_prime, -retraction_jump)
            gcode_generator.move_and_extrude(p2[0], p2[1])
            gcode_generator.move_and_extrude(p3[0], p3[1])
            gcode_generator.move_and_extrude(p4[0], p4[1])
            gcode_generator.move_and_extrude(p1[0], p1[1])

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
    wall_printer = TwoColumn()
    print(wall_printer.generate_gcode())
    # print("Estimated Print Time (seconds):", wall_printer.estimate_print_time())
