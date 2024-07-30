

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
