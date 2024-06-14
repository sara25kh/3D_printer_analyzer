
# Here the main application is built. It will run a webserver 
# using flask and it will call the needed functions to the 
# utilize PrinterTestRunner class. The main page of the 
# interface is index.html (in the Interface dir) and after 
# that it will navigate to pages that are related to the 
# specific printer test

from flask import Flask, render_template, send_from_directory
import os
from .PrinterTestRunner import PrinterTestRunner
from .SerialPrinterHandler import create_serial_printer_handler

script_dir = os.path.dirname(os.path.realpath(__file__))
interface_dir = os.path.join(script_dir, 'Interface')

app = Flask(__name__, static_folder=interface_dir, template_folder=interface_dir)

# Create an instance of PrinterTestRunner
# serial_printer_handler = create_serial_printer_handler()
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

@app.route('/test/<test_name>.html')
def test_page(test_name):
    # Get the test list
    test_list = printer_test_runner.get_test_list()

    if os.path.isfile(f'{interface_dir}/test/{test_name}.html'):
        test_data = next((test for test in test_list if test['name'] == 'SimpleWall'), None)
        print("Parameters: ", test_data['parameters'])
        return render_template(f'test/{test_name}.html', test_list=test_list, parameters=test_data['parameters'])
    else:
        return "Test not found", 404

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('./Interface/css', filename)

@app.route('/img/<path:filename>')
def serve_img(filename):
    return send_from_directory('./Interface/img', filename)

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/test/<test_name2>.html')
def test_page2(test_name2):
    if os.path.isfile(f'./Interface/test/{test_name2}.html'):
        return render_template(f'{test_name2}.html')
    else:
        return "Test not found", 404

if __name__ == '__main__':
    app.run(debug=True)

