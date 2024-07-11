
from ..gCodeGenerator import GCodeGenerator

class SimpleWall:
    def __init__(self, p1, p2, height):
        self.p1 = p1
        self.p2 = p2
        self.height = height

    def generate_gcode(self):
        gcode_generator = GCodeGenerator()
        gcode_generator.set_start_gcode_list([
            # 'M104 S150                                    ; start heating the extruder a bit to save some time but prevent oozing',
            # 'M140 S[first_layer_bed_temperature]          ; heatbed temperature',
            # 'M190 S[first_layer_bed_temperature]          ; wait for the bed to heat up',
            # 'M83                                          ; extruder relative mode',
            'G28                                          ',#; home all axes,
            # 'G29                                          ; Bed autolevel (optional, for BLTouch only)',
            'G92 E0                                       ',#; reset extruder',
            # 'G1 X0 Y0 F5000                               ; move to 0/0/0',
            'G1 Z0.2',
            # 'M109 S[first_layer_temperature]              ; Heat up extruder',
            # 'M42 P4 S0                                    ; Turn off LED (optional)',
            # 'M42 P5 S0',
            # 'M42 P6 S0',
            # 'G1 X20 Y5 Z0.3 F5000.0                       ; move to start-line position',
            # 'G1 Z0.3 F1000                                ; print height',
            # 'G1 X200 Y5 F1500.0 E15                       ; draw 1st line',
            # 'G1 X200 Y5.3 Z0.3 F5000.0                    ; move to side a little',
            # 'G1 X5.3  Y5.3 Z0.3 F1500.0 E30               ; draw 2nd line'
        ])
        gcode_generator.move(self.p1[0], self.p1[1], 0)
        gcode_generator.set_extrude_rate(0)

        # Move to the starting position
        gcode_generator.move(self.p1[0], self.p1[1])

        # Generate GCode for each layer
        while gcode_generator.total_z < self.height:
            gcode_generator.move_and_extrude(self.p2[0], self.p2[1])
            gcode_generator.go_to_next_layer()
            gcode_generator.move_and_extrude(self.p1[0], self.p1[1])
            gcode_generator.go_to_next_layer()

        return gcode_generator.generate()



# Run test that prints the generated gcode of this class:
if __name__ == '__main__':
    wall_printer = SimpleWall((0, 0), (100, 0), 10)
    print(wall_printer.generate_gcode())