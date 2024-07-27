from .serialPrinterHandler import * 
import time
from .testCases.simpleWall import SimpleWall
from .testCases.angledWall import AngledWall
from .testCases.sharpEdge import SharpEdge
import threading

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
                SimpleWall(),
                AngledWall(),
                SharpEdge()
            ]
        self.state = "READY"
        self.current_gcode_count_len = 0 #The amount of Gcode commands that have to run to get the test completed
        self.current_gcode_idx = -1 #The index of the current Gcode command that is running (Updates in the testrun_thread)
        self.testrun_thread = None
        self.testrun_thread_log = []
        self.max_thread_log = 100
        self.serial_printer_handler = None
        self.should_stop = False

    def is_connected_to_printer(self):
        return self.serial_printer_handler is not None
    
    def set_serial_printer_handler(self, serial_printer_handler):
        self.serial_printer_handler = serial_printer_handler

    def unset_serial_printer_handler(self):
        self.serial_printer_handler = None
    
    def get_test_list(self):
        return self.test_list
    
    def get_status(self):
        output = {}
        output["state"] = self.state
        output["progress"] = {
            "current_gcode_count_len": self.current_gcode_count_len,
            "current_gcode_idx": self.current_gcode_idx
        }
        return output

    def launch_testrun(self, test_name, parameters):

        if self.serial_printer_handler is None:
            raise Exception("Serial printer not connected")
        if self.state == "RUNNING":
            raise Exception("Printer is running")
        
        test_obj = self.get_test_object(test_name)
        if not test_obj:
            raise Exception("Invalid test type")

        gcode_list = []
        if not test_obj.set_parameters(parameters):
            raise Exception("Invalid parameters")
        print("final change:", test_obj.get_parameters())

        self.should_stop = False
        self.testrun_thread = threading.Thread(target=self.testrun, args=(test_obj,))
        self.testrun_thread.start()
    
    # The thread function that feeds the generated GCode to the printer
    def testrun(self, test_obj):
        self.state = "RUNNING"
        gcode_list = test_obj.generate_gcode()
        self.current_gcode_idx = 0
        
        # Wait for the printer to get ready
        time.sleep(5)

        # Update the current_gcode_count_len
        self.current_gcode_count_len = len(gcode_list)

        # Feed the gcode_list to the serial port
        for idx, gcode in enumerate(gcode_list):
            if self.should_stop == True:
                self.state = "CANCELED"
                printer_log = self.serial_printer_handler.send("G91")
                printer_log = self.serial_printer_handler.send("G1 Z10")
                return
            print(f"Sent: {gcode}")
            self.testrun_thread_log.append(f"Sent: {gcode}")
            printer_log = self.serial_printer_handler.send(gcode)
            # Update the current_gcode_idx
            self.current_gcode_idx = idx
            
            # print(f"printer_log: {printer_log}")
            self.testrun_thread_log.extend(printer_log)
            # Remove the logs if it exceeds the max_thread_log
            if len(self.testrun_thread_log) > self.max_thread_log:
                self.testrun_thread_log = self.testrun_thread_log[-self.max_thread_log:]
        
        #Done!!!
        self.state = "FINISHED"

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
    
    def cancel_testrun(self):
        self.should_stop = True  # Signal the test run to stop
        # if self.serial_printer_handler:
        #     self.serial_printer_handler.stop_printing()
        print("sent cancel signal")


#Test the class
if __name__ == '__main__':
    # Create a serial printer handler
    serial_printer_handler = create_serial_printer_handler_by_cli_input()

    # Create a PrinterTestRunner instance
    printer_test_runner = PrinterTestRunner()
    printer_test_runner.set_serial_printer_handler(serial_printer_handler)

    # print("SimpleWall parameter structure:", printer_test_runner.get_parameter_structure('SimpleWall'))
# Example: Run the SimpleWall test
    printer_test_runner.launch_testrun("simple_wall", {
        "length.value": 50,
        "height.value": 5
    })

    while(True):
        time.sleep(1)
        while printer_test_runner.testrun_thread_log:
            log = printer_test_runner.testrun_thread_log.pop(0)
            print(log)

        if printer_test_runner.state == "READY":
            break

    # Example: Run the AngledWall test
    printer_test_runner.launch_testrun("angled_wall", {
        "length.value": 50,
        "height.value": 5,
        "alpha.value": 45
    })

    while(True):
        time.sleep(1)
        while printer_test_runner.testrun_thread_log:
            log = printer_test_runner.testrun_thread_log.pop(0)
            print(log)

        if printer_test_runner.state == "READY":
            break

    # serial_printer_handler.stop()
    print("Done")
