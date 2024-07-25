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
                if given_val_key.endswith("value"):
                    param_type_key = re.sub(r'\.value', '.type', given_val_key)
                    if param_type_key in flat_params.keys():
                        type_check_result = None
                        if flat_params[param_type_key] == "NUMBER":
                            if isinstance(given_val_value, str):
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
                        if isinstance(tmp_sub_param[key], dict):
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
    name = "simple_wall"
    def __init__(self):
        self.params = {
            "length": {
                "type": "NUMBER",
                "value": 50
            },
            "height": {
                "type": "NUMBER",
                "value": 5
            }
        }

    def generate_gcode(self):
        gcode_generator = GCodeGenerator()
        gcode_generator.set_start_gcode_list([
            'G28', # home all axes
            'G90', # set to Absolute Positioning
            'G92 E0', # reset extruder
            'G1 Z0.2',
        ])

        gcode_generator.set_end_gcode_list([
            'G91', # Set to Relative Positioning Mode
            'G1 Z10', # Raise the nozzle 10mm high
            'M84', # disable motors
        ])

        start_x = 50
        start_y = 100
        length = self.params["length"]["value"]

        gcode_generator.move(start_x, start_y, 0)
        gcode_generator.set_extrude_rate(0)

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
