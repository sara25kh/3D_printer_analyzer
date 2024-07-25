
from ..gCodeGenerator import GCodeGenerator
from ..helper import flatten
import re


class TestCaseBase:

    def __init__(self):
        self.params = {}

    def get_parameters(self):
        return self.params
    
    def set_parameters(self, values):
        flat_params = flatten(self.params)
        flat_values = flatten(values)
        print("\nflat_params", flat_params)
        print("\nflat_values", flat_values)

        try:
            for given_val_key, given_val_value in flat_values.items():
                if(given_val_key.endswith("value")):
                    param_type_key = re.sub(r'\.value', '.type', given_val_key)
                    if(param_type_key in flat_params.keys()):
                        type_check_result = None
                        if flat_params[param_type_key] == "NUMBER":
                            if(isinstance(given_val_value, str)):
                                try:
                                    given_val_value = float(given_val_value)
                                except:
                                    type_check_result = False
                            type_check_result = isinstance(given_val_value, (int, float))
                        elif flat_params[param_type_key] == "STRING":
                            type_check_result = isinstance(given_val_value, str)
                        else:
                            raise(Exception(f"Undefined type for {param_type_key}"))
                        
                        if not type_check_result:
                            raise(Exception(f"Value '{given_val_value}' in '{given_val_key}' is not a '{flat_params[param_type_key]}'"))
                    else:
                        key_name = re.sub(r'\.value', '', given_val_key)
                        raise(Exception(f"Key '{key_name}' is not defined"))
                    
                    # Ok, lets write it to the params
                    tmp_sub_param = self.params
                    for key in given_val_key.split("."):
                        if(isinstance(tmp_sub_param[key], dict)):
                            tmp_sub_param = tmp_sub_param[key]
                        else:
                            tmp_sub_param[key] = given_val_value
                    
        except Exception as e:
            print(e)
            return False
        
        flat_params = flatten(self.params)
        flat_values = flatten(values)
        print("\nflat_params2:", flat_params)
        print("\nflat_values2", flat_values)
        
        return True
    
    def generate_gcode(self):
        raise(Exception("generate_gcode(): Not implemented"))

class SimpleWall(TestCaseBase):
    name = "SimpleWall"
    def __init__(self):
        self.params = {
            "start": {
                'x':{
                    "type":"NUMBER", 
                    "value": 50
                },
                'y':{
                    "type":"NUMBER",
                    "value": 100
                }
            },
            "end": {
                'x':{
                    "type":"NUMBER", 
                    "value": 100
                },
                'y':{
                    "type":"NUMBER",
                    "value": 100
                }
            },
            "height": {
                "type":"NUMBER",
                "value": 5
            }
        }

    def generate_gcode(self):
        gcode_generator = GCodeGenerator()
        gcode_generator.set_start_gcode_list([
            # 'M104 S150                                    ; start heating the extruder a bit to save some time but prevent oozing',
            # 'M140 S[first_layer_bed_temperature]          ; heatbed temperature',
            # 'M190 S[first_layer_bed_temperature]          ; wait for the bed to heat up',
            # 'M83                                          ; extruder relative mode',
            'G28                                          ',#; home all axes,
            'G90                                          ',# ;Set to Absolute Positioning
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

        gcode_generator.set_end_gcode_list([
            'G91                                          ',#; Set to Relative Positioning Mode',
            'G1 Z10                                       ',#; Rase the nozzle 10mm high',
            # 'M104 S0                                      ; turn off temperature',
            # 'M140 S0                                      ; turn off heatbed',
            # 'G28                                          ; home all axes',
            'M84                                          ',#; disable motors',
            # 'M107                                         ; turn off fan',
            # 'M42 P4 S255                                  ; Turn on LED (optional)',
            # 'M42 P5 S255',
            # 'M42 P6 S255',
            # 'M42 P7 S255'
        ])

        gcode_generator.move(self.params["start"]["x"]["value"], self.params["start"]["y"]["value"], 0)
        gcode_generator.set_extrude_rate(0)

        # Move to the starting position
        gcode_generator.move(self.params["start"]["x"]["value"], self.params["start"]["y"]["value"])

        # Generate GCode for each layer
        while gcode_generator.total_z < self.params["height"]["value"]:
            gcode_generator.move_and_extrude(self.params["end"]["x"]["value"], self.params["end"]["y"]["value"])
            gcode_generator.go_to_next_layer()
            gcode_generator.move_and_extrude(self.params["start"]["x"]["value"], self.params["start"]["y"]["value"])
            gcode_generator.go_to_next_layer()

        return gcode_generator.generate()

# Run test that prints the generated gcode of this class:
if __name__ == '__main__':
    wall_printer = SimpleWall()
    print(wall_printer.generate_gcode())
    # print("Estimated Print Time (seconds):", wall_printer.estimate_print_time())