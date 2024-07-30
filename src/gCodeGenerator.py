class GCodeGenerator:
    def __init__(self):
        self.commands = []
        self.extrude_rate = 0.1
        self.total_extrude = 0
        self.default_speed = 1000
        self.ending_commands = []
        self.layer_height = 0.2
        self.total_z = 0.2
        self.last_position = (0, 0)

    def set_extrude_rate(self, rate):
        self.extrude_rate = rate
    
    def set_default_speed(self, speed):
        self.default_speed = speed

    def set_layer_height(self, height):
        self.layer_height = height

    def move(self, x, y, speed = None):
        self.commands.append(f"G0 X{x} Y{y} F{speed or self.default_speed}")
        self.last_position = (x, y)

    def move_and_extrude(self, x, y, speed = None):
        dist = ((x - self.last_position[0]) ** 2 + (y - self.last_position[1]) ** 2) ** 0.5
        self.total_extrude += self.extrude_rate * dist
        self.commands.append("G0 X{:.2f} Y{:.2f} F{:.0f} E{:.2f}".format(x, y, speed or self.default_speed, self.total_extrude))
        self.last_position = (x, y)

    def go_to_next_layer(self):
        self.total_z += self.layer_height
        self.total_z = round(self.total_z, 4)  # Update the precision to 4 digits
        self.commands.append(f"G0 Z{self.total_z:.4f}")  # Print with 4 digits of precision

    def set_start_gcode_list(self, start_gcode_list):
        self.commands = start_gcode_list + self.commands
    
    def set_end_gcode_list(self, end_gcode_list):
        self.ending_commands = end_gcode_list
    
    def retract(self, amount, rise_amount = 0):
        self.total_extrude -= amount
        self.total_z += rise_amount
        self.commands.append("G0 E{:.2f} Z{:.2f}".format(self.total_extrude, self.total_z))

    def generate(self):
        return self.commands + self.ending_commands
