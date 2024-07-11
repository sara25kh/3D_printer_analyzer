from .serialPrinterHandler import create_serial_printer_handler
import time
from .testCases.simpleWall import SimpleWall

class PrinterTestRunner:
    # This class recognizes the different tests and gives the output that 
    # are needed to be given to the printer
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.test_list = [
                {
                    "name": "SimpleWall",
                    "parameters": {
                        "start": {'x':"NUMBER", 'y':"NUMBER"},
                        "end": {'x':"NUMBER", 'y':"NUMBER"},
                        "height": "NUMBER"
                    }
                }
            ]
    
    def set_serial_printer_handler(self, serial_printer_handler):
        self.serial_printer_handler = serial_printer_handler
    
    def get_test_list(self):
        return self.test_list

    def run(self, test_type, parameters):
        gcode_list = []
        if test_type == "SimpleWall":
            if not self.check_parameter_compatibility(test_type, parameters):
                raise Exception("Invalid parameters")
            simple_wall = SimpleWall(
                (parameters['start']['x'], parameters['start']['y']), 
                (parameters['end']['x'], parameters['end']['y']), 
                parameters['height'])
            gcode_list = simple_wall.generate_gcode()
        else:
            raise Exception("Invalid test type")
        
        # Wait for the printer to get ready
        time.sleep(5)

        # Feed the gcode_list to the serial port
        for gcode in gcode_list:
            self.serial_printer_handler.send(gcode)
            print(f"finished: {gcode}")

    def get_parameter_structure(self, test_name):
        test_data = next((test for test in self.test_list if test['name'] == test_name), None)
        if test_data is None:
            return None
        return test_data['parameters']

    def check_substructure_compatibility(self, parameter_structure, parameters):
        # This is a recursive function
        if isinstance(parameter_structure, dict):
            for struct_key, struct_value in parameter_structure.items():
                if struct_key not in parameters:
                    return False
                if not self.check_substructure_compatibility(struct_value, parameters[struct_key]):
                    return False
            return True
        elif isinstance(parameter_structure, list):
            if not isinstance(parameters, list):
                return False
            for parameter in parameters:
                if not self.check_substructure_compatibility(parameter_structure[0], parameter):
                    return False
            return True
        elif parameter_structure == "NUMBER":
            return isinstance(parameters, (int, float))
        elif parameter_structure == "STRING":
            return isinstance(parameters, str)
        else:
            print("Invalid parameter structure: ", parameter_structure, " > ", parameters)
            return False

    def check_parameter_compatibility(self, test_name, parameters):
        parameter_structure = self.get_parameter_structure(test_name)
        if parameter_structure is None:
            return False
        return self.check_substructure_compatibility(parameter_structure, parameters)


#Test the class
if __name__ == '__main__':
    # Create a serial printer handler
    serial_printer_handler = create_serial_printer_handler()
    serial_printer_handler.start()

    # Create a PrinterTestRunner instance
    printer_test_runner = PrinterTestRunner()
    printer_test_runner.set_serial_printer_handler(serial_printer_handler)

    # Run the test
    printer_test_runner.run("SimpleWall", {
        "start": {'x':50, 'y':50},
        "end": {'x':100, 'y':50},
        "height": 10
    
    })

    serial_printer_handler.stop()
    print("Done")
