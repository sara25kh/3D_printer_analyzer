
# Here the main application is built. It will run a webserver 
# using flask and it will call the needed functions to the 
# utilize PrinterTestRunner class. The main page of the 
# interface is index.html (in the Interface dir) and after 
# that it will navigate to pages that are related to the 
# specific printer test

from flask import Flask, render_template, send_from_directory, request
import os
from .printerTestRunner import PrinterTestRunner

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
    printer_test_runner.run(test_name, request.get_json())

    return {"status": "success"}

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
    app.run(debug=True)

