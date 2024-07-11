import time
from .serial import SerialHandler, SerialPortLister

class SerialPrinterHandler:
    def __init__(self, port_name, baudrate):
        self.serial_handler = SerialHandler(port_name, baudrate)

    def start(self):
        self.serial_handler.start()

    def stop(self):
        self.serial_handler.stop()
    
    def empty_recv_queue(self):
        while self.serial_handler.serial.in_waiting > 0:
            self.serial_handler.serial.read(1000)
    
    def send(self, command):
        self.empty_recv_queue()
        self.serial_handler.writeln(command)
        response = self.serial_handler.serial.readline().decode().strip()
        print("res: ", response)
        while response != "ok":
            time.sleep(0.1)
            response = self.serial_handler.serial.readline().decode().strip()
            print("res: ", response)

def create_serial_printer_handler():
    # Ask the user to select a port by index
    lister = SerialPortLister()
    ports = lister.list_ports()
    if not ports:
        print("No ports available")
        return None
    print("Available Ports:")
    for i, port in enumerate(ports):
        print(f"{i}: {port}")
    port_index = int(input("Select a port by index (default: 0): ") or 0)
    port = ports[port_index]
    print(f"Selected Port: {port}")

    # Ask the user to input the baudrate
    baudrate = int(input("Enter the baudrate (default: 115200): ") or 115200)

    # Create and return a SerialPrinterHandler instance
    return SerialPrinterHandler(port, baudrate)

if __name__ == '__main__':
    handler = create_serial_printer_handler()
    handler.start()
    #Write some data
    while True:
        data = input("Enter data to send: ")
        #If data is 'exit' then close & break
        if data.strip() == 'exit':
            break
        handler.send(data.encode())
        #Read some data
        # while handler.serial.in_waiting > 0:
        #     data = handler.serial.read(1000)
        #     print(f"Received: {data.decode('utf-8')}")
        
    handler.stop()
    print("Done")
