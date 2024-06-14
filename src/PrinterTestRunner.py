from .SimpleWall import SimpleWall
from .SerialPrinterHandler import create_serial_printer_handler
import time

class PrinterTestRunner:
    # This class recognizes the different tests and gives the output that 
    # are needed to be given to the printer
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PrinterTestRunner, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, serial_printer_handler):
        self._init__()
        self.serial_printer_handler = serial_printer_handler
    
    def __init__(self):
        self.test_list = [
                {
                    "name": "SimpleWall",
                    "parameters": {
                        "start": ["NUMBER", "NUMBER"],
                        "end": ["NUMBER", "NUMBER"],
                        "width": "NUMBER"
                    }
                }
            ]
    
    def get_test_list(self):
        return self.test_list

    def run(self, test_type):
        gcode_list = []
        if test_type == "SimpleWall":
            simple_wall = SimpleWall((50, 100), (100, 100), 1)
            gcode_list = simple_wall.generate_gcode()
        else:
            raise Exception("Invalid test type")
        
        # Wait for the printer to get ready
        time.sleep(5)

        # Feed the gcode_list to the serial port
        for gcode in gcode_list:
            self.serial_printer_handler.send(gcode)
            print(f"finished: {gcode}")


#Test the class
if __name__ == '__main__':
    # Create a serial printer handler
    serial_printer_handler = create_serial_printer_handler()
    serial_printer_handler.start()

    # Create a PrinterTestRunner instance
    printer_test_runner = PrinterTestRunner(serial_printer_handler)

    # Run the test
    printer_test_runner.run("SimpleWall")

    serial_printer_handler.stop()
    print("Done")
