
# This application is going to be a G code generator for 3D printers.
# -It will generate G-Code series from scratch.
# -The g-code output that is going to be generated can be decided by the user. For example:
#   -Simple wall
#   -Simple wall with a hole
#   -Wall with angles
#   -Curved wall
#   -Curved roofs

from src.app import app




if __name__ == '__main__':
    print("This is a G-Code generator for 3D printers")
    # app = App()
    app.run(debug=True,port = 3000)