from .serialPrinterHandler import create_serial_printer_handler_by_cli_input
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
                SimpleWall()
            ]
    
    def set_serial_printer_handler(self, serial_printer_handler):
        self.serial_printer_handler = serial_printer_handler
    
    def get_test_list(self):
        return self.test_list

    def run(self, test_name, parameters):
        test_obj = self.get_test_object(test_name)
        if not test_obj:
            raise Exception("Invalid test type")

        gcode_list = []
        if not test_obj.set_parameters(parameters):
            raise Exception("Invalid parameters")
        print("final change:", test_obj.get_parameters())
        return

        gcode_list = test_obj.generate_gcode()
        
        # Wait for the printer to get ready
        time.sleep(5)

        # Feed the gcode_list to the serial port
        for gcode in gcode_list:
            self.serial_printer_handler.send(gcode)
            print(f"finished: {gcode}")

    def get_test_object(self, test_name):
        return next((test for test in self.test_list if test.name == test_name), None)

    def get_parameter_structure(self, test_name):
        test_obj = self.get_test_object(test_name)
        if test_obj is None:
            return None
        return test_obj.get_parameters()


    def check_parameter_compatibility(self, test_name, parameters):
        parameter_structure = self.get_parameter_structure(test_name)
        if parameter_structure is None:
            return False
        return self.check_substructure_compatibility(parameter_structure, parameters)


#Test the class
if __name__ == '__main__':
    # Create a serial printer handler
    # serial_printer_handler = create_serial_printer_handler_by_cli_input()

    # Create a PrinterTestRunner instance
    printer_test_runner = PrinterTestRunner()
    # printer_test_runner.set_serial_printer_handler(serial_printer_handler)

    # print("SimpleWall parameter structure:", printer_test_runner.get_parameter_structure('SimpleWall'))

    # Run the test
    printer_test_runner.run("SimpleWall", {
        "start": {'x.value':50, 'y.value':50},
        "end": {'x.value':100, 'y.value':50},
        "height.value": 3
    })

    # serial_printer_handler.stop()
    print("Done")
