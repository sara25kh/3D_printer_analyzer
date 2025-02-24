
# Here the main application is built. It will run a webserver 
# using flask and it will call the needed functions to the 
# utilize PrinterTestRunner class. The main page of the 
# interface is index.html (in the Interface dir) and after 
# that it will navigate to pages that are related to the 
# specific printer test

from flask import Flask, render_template, send_from_directory, request
import os
from .printerTestRunner import PrinterTestRunner
from .serialPrinterHandler import SingletonSerialPrinterHandler

from . import database

script_dir = os.path.dirname(os.path.realpath(__file__))
interface_dir = os.path.join(script_dir, 'interface')

app = Flask(__name__, static_folder=interface_dir, template_folder=interface_dir)

# Create an instance of PrinterTestRunner
printer_test_runner = PrinterTestRunner()

# Add custom filters to the Jinja2 environment
@app.template_filter('is_string')
def is_string(value):
    return isinstance(value, str)

@app.template_filter('is_iterable')
def is_iterable(value):
    return isinstance(value, (list, tuple))


@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route('/api/v1/status')
def status():
    return printer_test_runner.get_status()

@app.route('/api/v1/status/temp')
def status_temp():
    temp_res = printer_test_runner.get_temps()
    if temp_res:
        return {"status":"success", "data":temp_res}
    return {"status":"fail"}

@app.route('/api/v1/status/connected')
def connected():
    if printer_test_runner.is_connected_to_printer():
        return {"status": "connected"}
    return {"status": "disconnected"}

@app.route('/api/v1/printer/port_list', methods=['GET'])
def get_port_list():
    return {"status":"success", "ports": SingletonSerialPrinterHandler().get_serial_ports_list()}

@app.route('/api/v1/printer/connect', methods=['POST'])
def connect_printer():
    data = request.get_json()
    port = data['port']
    baudrate = data['baudrate']
    try:
        print(f"Trying to connect to port: {port} with baudrate: {baudrate}")
        SingletonSerialPrinterHandler().start(port, baudrate)
        printer_test_runner.set_serial_printer_handler(SingletonSerialPrinterHandler())
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {"status": "success"}

@app.route('/api/v1/printer/disconnect', methods=['POST'])
def disconnect_printer():
    try:
        SingletonSerialPrinterHandler().stop()
        printer_test_runner.unset_serial_printer_handler()
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {"status": "success"}


@app.route('/api/v1/test/get_params/<test_name>')
def test_page(test_name):
    # Get the test list
    print(f"api:: received test_name: {test_name}")
    test_obj = printer_test_runner.get_test_object(test_name)
    print(f"api:: found test_obj: {test_obj}")

    return test_obj.get_parameters()

@app.route('/api/v1/test/run_test/<test_name>', methods=['POST'])
def process_test(test_name):
    # Process the test
    print(f"api:: Processing test_name: {test_name}")
    print(f"api:: request.get_json():", request.get_json())
    try:
        printer_test_runner.launch_testrun(test_name, request.get_json())
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {"status": "success"}

@app.route('/api/v1/test/cancel', methods=['POST'])
def cancel_test():
    try:
        printer_test_runner.cancel_testrun()
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {"status": "success"}

#Profile
@app.route('/api/v1/test/profile/<test_name>', methods=["POST"])
def insert_profile(test_name):
    
    print(f"api:: received test_name: {test_name}")
    print(f"api:: request.get_json():", request.get_json())
    database.insert_row(test_name, request.get_json())

    return {"status": "success"}

@app.route('/api/v1/test/profile/delete/<profile_name>', methods=["DELETE"])
def delete_profile(profile_name):
    test_name = request.args.get('test_name')  # Assuming test_name is sent as a query parameter

    if not test_name:
        return {"status": "error", "message": "test_name is required"}, 400

    print(f"api:: received test_name: {test_name}, profile_name: {profile_name}")

    try:
        # Call the delete_row function to delete the profile
        database.delete_row(test_name, profile_name)
        return {"status": "success", "message": f"Profile '{profile_name}' deleted successfully"}
    except Exception as e:
        print(f"Error deleting profile: {e}")
        return {"status": "error", "message": "An error occurred while deleting the profile"}, 500



@app.route('/api/v1/test/profile/<test_name>', methods=["GET"])
def query_profile(test_name):

    return database.fetch_test_data(test_name)


    

@app.route('/test/testcase.html')
def serve_test():
    return app.send_static_file('./test/testcase.html')

@app.route('/test/<path:filename>')
def serve_test_all(filename):
    return send_from_directory('./interface/test', filename)

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('./interface/css', filename)

@app.route('/img/<path:filename>')
def serve_img(filename):
    return send_from_directory('./interface/img', filename)

@app.route('/test/<test_name2>.html')
def test_page2(test_name2):
    if os.path.isfile(f'./Interface/test/{test_name2}.html'):
        return render_template(f'{test_name2}.html')
    else:
        return "Test not found", 404

if __name__ == '__main__':
    app.run(debug=True,port = 3000)



