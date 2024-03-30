import time
from Serial import SerialHandler, SerialPortLister

class SerialPrinterHandler:
    def __init__(self, port_name, baudrate):
        self.serial_handler = SerialHandler(port_name, baudrate)

    def start(self):
        self.serial_handler.start()

    def stop(self):
        self.serial_handler.stop()
    
    def send(self, command):
        self.serial_handler.writeln(command)
        response = self.serial_handler.serial.readline().decode().strip()
        # print("res: ", response)
        while response != "ok":
            time.sleep(0.1)
            response = self.serial_handler.serial.readline().decode().strip()
            # print("res: ", response)

if __name__ == '__main__':
    #Testing the Serial Classes
    #First list the available serials
    lister = SerialPortLister()
    #Ask the user to select a port by index
    ports = lister.list_ports()
    print("Available Ports:")
    for i, port in enumerate(ports):
        print(f"{i}: {port}")
    port_index = int(input("Select a port by index (default: 0): ") or 0)
    port = ports[port_index]
    print(f"Selected Port: {port}")
    #Create a SerialHandler
    #Ask the user to input the baudrate
    baudrate = int(input("Enter the baudrate (default: 115200): ") or 115200)
    handler = SerialPrinterHandler(port, baudrate)
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
