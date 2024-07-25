
//Retrieves the value of a URL query parameter by its name
function uri_get_param(name){
    if(name=(new RegExp('[?&]'+encodeURIComponent(name)+'=([^&]*)')).exec(location.search))
        return decodeURIComponent(name[1]);
}

//Set title of the page
document.title = uri_get_param('test_name');
 
//Fetches the parameters for the test case and updates the form
var param_struct = {}
fetch("/api/v1/test/get_params/" + uri_get_param('test_name'),
{
    method: "GET",
    headers: {
        "Content-type": "application/json",
    },
})
.then((response) => response.json())
.then((json) => {
    param_struct = json;
    update_form(document.getElementById("param-form"), 0);
});

//Dynamically creates input fields for the parameters
function update_form(targetElement, level) {
    let params = param_struct;
    console.log('params:', params);

    // Get the target element where the textboxes will be added
    // const targetElement = document.getElementById(element);

    // Clear the target element's existing content
    //targetElement.innerHTML = '';

    function createInputWithLabel(key_label, param, targetFormElement) {
        // Create a row
        const rowDiv = document.createElement('div');
        rowDiv.classList.add('form-row');
        rowDiv.classList.add('g-0');
    
        // Create a column for the label
        const labelDiv = document.createElement('div');
        labelDiv.classList.add('col-md-3');
        labelDiv.classList.add('form-group');
    
        // Create a label for the input
        const label = document.createElement('label');
        label.setAttribute('for', key_label);
        label.textContent = `${key_label}:`;
        label.classList.add('form-label'); // Bootstrap class for labels
        labelDiv.appendChild(label);
        labelDiv.style.margin = '0';
        rowDiv.appendChild(labelDiv);
    
        // Create a column for the input
        const inputDiv = document.createElement('div');
        inputDiv.classList.add('col-md-9');
        inputDiv.classList.add('form-group');

        // Define a mapping of parameter keys to their units
        const paramUnits = {
            "length": "mm",
            "height": "mm",
            "alpha": "degree"
        };
    
        // Create the input textbox
        const input = document.createElement('input');
        input.setAttribute('type', 'text');
        input.setAttribute('id', key_label);
        input.setAttribute('name', key_label);
        const unit = paramUnits[key_label.split('.')[0]] || ''; // split is used to handle nested keys if any
        const placeholderText = unit ? `default: ${param.value} ${unit}` : `default: ${param.value}`;
        // Set the placeholder with the appropriate unit
        input.setAttribute('placeholder', placeholderText);
        input.classList.add('form-control-sm');
        inputDiv.appendChild(input);
        inputDiv.style.margin = '0';
        rowDiv.appendChild(inputDiv);
    
        // Append the container div to the target element
        targetFormElement.appendChild(rowDiv);
    }

    // Iterate over the keys in the params object
    for (let key in params) {
        if (params.hasOwnProperty(key)) {
            // Check if params[key] has the property 'type'
            if (!params[key].hasOwnProperty('type')) {
                // Treat params[key] as a set of other params

                // Iterate over the keys in params[key]
                for (let subKey in params[key]) {
                    if (params[key].hasOwnProperty(subKey)) {
                        // Create an input textbox with a label
                        createInputWithLabel(`${key}.${subKey}`, params[key][subKey], targetElement);
                    }
                }
            } else {
                // Create an input textbox with a label
                createInputWithLabel(`${key}`, params[key], targetElement);
            }
        }
    }

    //Set the "test-img-description" source image
    const img = document.getElementById('test-img-description');
    img.src = "../img/" + uri_get_param('test_name') + ".png";
}

//The function which validates and processes the form data when submit is clicked
function submit_form_data() {
    // Get the form element
    const formElement = document.getElementById('param-form');

    // Get the form data
    const formData = new FormData(formElement);

    // Get the flatten version of param struct:
    let flatten_param_struct = {};
    function flatten_params(params, prefix) {
        for (let key in params) {
            if (params.hasOwnProperty(key)) {
                if (params[key].hasOwnProperty('type')) {
                    flatten_param_struct[prefix + key] = params[key];
                } else {
                    flatten_params(params[key], prefix + key + '.');
                }
            }
        }
    }
    flatten_params(param_struct, '');
    // console.log("flatten_param_struct:", flatten_param_struct);

    // Convert the form data to a JSON object
    const jsonData = {};
    for (let [key, value] of formData) {
        //Check value based on flatten_param_struct[key].type
        if (flatten_param_struct[key].type === 'NUMBER') {
            value = parseFloat(value);
        } else if (flatten_param_struct[key].type === 'STRING') {
            value = value;
        }

        jsonData[`${key}.value`] = value ? value : flatten_param_struct[key].value;
    }

    // Log the JSON object to the console
    console.log(jsonData);

    // Send the JSON object to the server
    fetch("/api/v1/test/run_test/" + uri_get_param('test_name'),
    {
        method: "POST",
        headers: {
            "Content-type": "application/json",
        },
        body: JSON.stringify(jsonData),
    })
    .then((response) => response.json())
    .then((json) => {
        // If json['status'] is 'error', display the error message
        if (json['status'] === 'error') {
            alert(json['message']);
        }
    });

    //Put the form in readonly mode
    readonly_form();
}

//Function that puts the form in readonly mode:
function readonly_form() {
    // Get the form element
    const formElement = document.getElementById('param-form');

    //Put the form in readonly mode
    let inputs = formElement.getElementsByTagName('input');
    for (let i = 0; i < inputs.length; i++) {
        inputs[i].readOnly = true;
        //Change the style of the input
        inputs[i].style.backgroundColor = '#f8f9fa';
    }

    //Change the style of the submit button
    const submitButton = document.getElementById('submit-form');
    submitButton.textContent = 'Submitted';
}

//This function puts the form in writable mode
function writable_form(){
    // Get the form element
    const formElement = document.getElementById('param-form');

    //Put the form in readonly mode
    let inputs = formElement.getElementsByTagName('input');
    for (let i = 0; i < inputs.length; i++) {
        inputs[i].readOnly = false;
        //Change the style of the input
        inputs[i].style.backgroundColor = '#ffffff';
    }

    //Change the style of the submit button
    const submitButton = document.getElementById('submit-form');
    submitButton.textContent = 'Submit';

}


// Get the submit button
const submitButton = document.getElementById('submit-form');

// Add an event listener to the submit button
submitButton.addEventListener('click', submit_form_data);


// Function to handle disconnect button click
function disconnectSerial() {
    // Make a POST request to /api/v1/printer with param "cmd": "disconnect"
    fetch("/api/v1/printer/disconnect", {
        method: "POST",
        headers: {
            "Content-type": "application/json",
        },
        body: JSON.stringify({ 'cmd': 'disconnect' }),
    })
    .then((response) => response.json())
    .then((json) => {
        console.log("Disconnect request response:", json);
        // Get the connect button
        const connectButton = document.getElementById('connect-serial');

        // Change the text of the connect button
        connectButton.textContent = 'Connect to Printer\'s Serial';

        // Enable the connect button
        connectButton.disabled = false;

        // Enable the disconnect button
        disconnectButton.disabled = true;

        // Make serial settings changeable
        document.getElementById('serial-port').disabled = false;
        document.getElementById('serial-baudrate').readOnly = false;
    })
    .catch((error) => {
        console.log("Disconnect error:", error);
    });
}

// Get the disconnect button
const disconnectButton = document.getElementById('disconnect-serial');

// Add an event listener to the disconnect button
disconnectButton.addEventListener('click', disconnectSerial);


function connectSerial() {

    // Get the serial selected port from the dropdown list
    const serialPortDropdown = document.getElementById('serial-port');
    const port = serialPortDropdown.value;

    // Get the baudrate from input serial-baudrate
    const baudrate = document.getElementById('serial-baudrate').value;

    // Make a POST request to /api/v1/printer with param "cmd": "connect"
    fetch("/api/v1/printer/connect", {
        method: "POST",
        headers: {
            "Content-type": "application/json",
        },
        body: JSON.stringify({ 'port': port, 'baudrate': baudrate }),
    })
    .then((response) => response.json())
    .then((json) => {
        console.log("Connect request response:", json);
        // Get the connect button
        const connectButton = document.getElementById('connect-serial');

        // Change the text of the connect button
        connectButton.textContent = 'Connected';

        // Disable the connect button
        connectButton.disabled = true;

        // Enable the disconnect button
        disconnectButton.disabled = false;

         // Make serial settings unchangeable
         document.getElementById('serial-port').disabled = true;
         document.getElementById('serial-baudrate').readOnly = true;
    })
    .catch((error) => {
        const connectButton = document.getElementById('connect-serial');
        connectButton.textContent = 'Connect to Printer\'s Serial';
        
        // Disable the connect button
        connectButton.disabled = false;
    });
}
// Get the connect button
const connectButton = document.getElementById('connect-serial');
// Add an event listener to the connect button
connectButton.addEventListener('click', connectSerial);

//Function to check if the serial is already connected or not
function updateSerialStatus(){
    // Make a GET request
    fetch("/api/v1/status/connected", {
        method: "GET",
        headers: {
            "Content-type": "application/json",
        },
    })
    .then((response) => response.json())
    .then((json) => {
        console.log("Serial status:", json);
        // Get the connect button
        const connectButton = document.getElementById('connect-serial');

        //If the serial is already connected
        if(json.status === 'connected'){
            // Change the text of the connect button
            connectButton.textContent = 'Connected';

            // Disable the connect button
            connectButton.disabled = true;

            // Enable the disconnect button
            disconnectButton.disabled = false;

            // Make serial settings unchangeable
            document.getElementById('serial-port').disabled = true;
            document.getElementById('serial-baudrate').readOnly = true;

        }else{
            // Change the text of the connect button
            connectButton.textContent = 'Connect to Printer\'s Serial';

            // Enable the connect button
            connectButton.disabled = false

            // Disable the disconnect button
            disconnectButton.disabled = true;

            // Make serial settings changeable
            document.getElementById('serial-port').disabled = false;
            document.getElementById('serial-baudrate').readOnly = false;
        }
    });
}

//Function to update the serial port dropdown list
function updateSerialPorts() {
    // Make a GET request to /api/v1/printer/port_list
    fetch("/api/v1/printer/port_list", {
        method: "GET",
        headers: {
            "Content-type": "application/json",
        },
    })
    .then((response) => response.json())
    .then((json) => {
        console.log("Serial ports:", json);
        // Get the serial port dropdown list
        const serialPortDropdown = document.getElementById('serial-port');

        //Save previous selected value
        let previous_selected = serialPortDropdown.value;

        // Clear the dropdown list
        serialPortDropdown.innerHTML = '';

        // Create an option for each serial port
        for (let port of json.ports) {
            const option = document.createElement('option');
            option.value = port;
            option.textContent = port;
            serialPortDropdown.appendChild(option);
        }

        //If there is any option put the first option as selected
        if (json.ports.length > 0) {
            //If the previous selected value is in the list, select it
            if(json.ports.includes(previous_selected)){
                serialPortDropdown.value = previous_selected;
                serialPortDropdown.selectedIndex = json.ports.indexOf(previous_selected);
            }else{
                serialPortDropdown.selectedIndex = 0;
            }
        }else{
            const option = document.createElement('option');
            option.value = "No ports";
            option.textContent = "No ports";
            serialPortDropdown.appendChild(option);
            serialPortDropdown.selectedIndex = 0;

            //Disable the connect button
            const connectButton = document.getElementById('connect-serial');
            connectButton.disabled = true;
        }
    });
}

// Call a function to update the serial port_list every 5 seconds
function update_cycle_interval_func(){
    updateSerialStatus();
    updateSerialPorts();
    updatePrintStatus();
}
update_cycle_interval_func();
setInterval(update_cycle_interval_func, 5000);


// Function to update the progress bar
function updateProgressBar(percentage) {
    const progressBar = document.getElementById('progress-bar');
    progressBar.style.width = percentage + '%';
    progressBar.setAttribute('aria-valuenow', percentage);
    progressBar.textContent = percentage + '%';
}

// Function to simulate work progress
function updatePrintStatus() {
    //First call the api to get the print status
    fetch("/api/v1/status", {
        method: "GET",
        headers: {
            "Content-type": "application/json",
        },
    }).then((response) => response.json())
    .then((json) => {
        console.log("Print status:", json);
        // if the status is ready it means the progressbar should be 100%
        if(json.state === 'READY'){
            updateProgressBar(100);
            writable_form();
        }else{
            idx = json["progress"]["current_gcode_idx"]
            if(idx < 0){
                updateProgressBar(0);
            }
            total = json["progress"]["current_gcode_count_len"]
            updateProgressBar(idx*100/total);
        }
    });
        
}

// Function to go back to the previous page
function goBack() {
    window.history.back();
}

// Get the home button
const homeButton = document.getElementById('home-button');

// Add an event listener to the home button
homeButton.addEventListener('click', goBack);