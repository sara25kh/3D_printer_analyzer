import serial.tools.list_ports

class SerialHandler:
    def __init__(self, port_name, baudrate):
        self.baudrate = baudrate
        self.port_name = port_name
        self.serial = None
        self.receive_handler = None

    def start(self):
        # Implement the logic to start the serial connection
        if self.serial is None:
            self.serial = serial.Serial(port=self.port_name, baudrate=self.baudrate)
            self.serial.timeout = 0

    def stop(self):
        # Implement the logic to stop the serial connection
        if self.serial is not None:
            self.serial.close()
            self.serial = None

    def list_ports(self):
        # Get the list of available ports (COM or tty*)
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def write(self, data):
        # Implement the logic to write data to the serial connection
        if self.serial is not None:
            if isinstance(data, str):
                data = data.encode()
            self.serial.write(data)
    
    def writeln(self, data):
        # Write data with newline character
        if self.serial is not None:
            if isinstance(data, str):
                data = data.encode()
            self.serial.write(data + b'\n')

    def set_receive_handler(self, handler):
        self.receive_handler = handler



# A Class to give list of ports
class SerialPortLister:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        pass

    def list_ports(self):
        # Get the list of available ports (COM or tty*)
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

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
    handler = SerialHandler(port, baudrate)
    handler.start()
    #Write some data
    while True:
        data = input("Enter data to send: ")
        #If data is 'exit' then close & break
        if data.strip() == 'exit':
            break
        handler.writeln(data.encode())
        #Read some data
        while handler.serial.in_waiting > 0:
            data = handler.serial.read(1000)
            print(f"Received: {data.decode('utf-8')}")
        
    handler.stop()
    print("Done")

