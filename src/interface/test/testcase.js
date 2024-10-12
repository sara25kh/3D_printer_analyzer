
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
            "alpha": "degree",
            "bed_temp": "degree",
            "nozzle_temp": "degree"
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


// Function to handle cancel button click
function cancelPrint() {
    console.log("Sent cancel req");
    fetch("/api/v1/test/cancel", {
        method: "POST",
        headers: {
            "Content-type": "application/json",
        }
    })
    .then((response) => response.json())
    .then((json) => {
        console.log("Cancel request response:", json);
        if (json.status === "success") {
            // Handle successful cancel, e.g., reset the form
            writable_form();
            updateProgressBar(0);
        } else {
            alert("Error canceling the print: " + json.message);
        }
    })
    .catch((error) => {
        console.log("Cancel error:", error);
    });
}

// Add an event listener to the cancel button
const cancelButton = document.querySelector('#cancel-button');
cancelButton.addEventListener('click', cancelPrint);


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
            updateProgressBar(0);
            writable_form();
        }else if (json.state == 'FINISHED') {
            updateProgressBar(100);
            writable_form();
        }else if (json.state == 'CANCELED') {
            updateProgressBar(0);   
            writable_form();  
        }
        else{
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




document.addEventListener('DOMContentLoaded', function () {
    // Function to fetch and update temperatures
    function updateTemperatures() {
        fetch('/api/v1/status/temp')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const temps = data["data"];
                    document.getElementById('bed_temp_log').innerHTML = 'Bed Temperature: ' + temps["bed_temp"] + ' °C';
                    document.getElementById('nozzle_temp_log').textContent = 'Nozzle Temperature: ' + temps["nozzle_temp"] + ' °C';
                } else {
                    console.error('Failed to fetch temperatures');
                }
            })
            .catch(error => console.error('Error fetching temperatures:', error));
    }

    // Initial fetch
    updateTemperatures();

    // Update temperatures every 3 seconds
    setInterval(updateTemperatures, 3000);
});



document.addEventListener("DOMContentLoaded", function() {
    const paramForm = document.getElementById('param-form');
    const profileSelect = document.getElementById('profile-select');
    const profileDropdown = document.getElementById('profile-dropdown'); // Custom dropdown
    const selectedProfile = document.getElementById('selected-profile'); // Display area for selected profile
    const saveProfileButton = document.getElementById('save-profile');

    // Fetch profiles and populate the dropdown
    fetch('/api/v1/test/profile/' + uri_get_param('test_name'))
    .then(response => response.json())
    .then(profiles => {
        profiles.forEach(profile => {
        //     const option = document.createElement('option');
        //     option.value = profile["profile_name"];
        //     option.textContent = profile["profile_name"];
        //     profileSelect.appendChild(option);

            // Create a list item for each profile
            const listItem = document.createElement('li');
            listItem.classList.add('dropdown-item');
            listItem.textContent = profile["profile_name"];
            listItem.dataset.profileName = profile["profile_name"];

            // Create the trashcan icon
            const trashIcon = document.createElement('span');
            trashIcon.classList.add('trash-icon');
            trashIcon.innerHTML = '🗑️'; // Use emoji or font awesome icon
            trashIcon.style.cursor = 'pointer';

            // Append the trashcan to the list item
            listItem.appendChild(trashIcon);

            // Append the list item to the custom dropdown
            profileDropdown.appendChild(listItem);

            // Add the option to the hidden original select (if needed for form submission)
            const option = document.createElement('option');
            option.value = profile["profile_name"];
            option.textContent = profile["profile_name"];
            profileSelect.appendChild(option);

            // Add click event to delete profile on trashcan click
            trashIcon.addEventListener('click', function(event) {
                event.stopPropagation(); // Prevent triggering other events on the list item

                const profileName = listItem.dataset.profileName;
                const testName = uri_get_param('test_name');  // Assuming test_name is obtained from the URL or elsewhere

                // Call API to delete the profile
                fetch(`/api/v1/test/profile/delete/${profileName}?test_name=${testName}`, {
                    method: 'DELETE',
                })
                .then(response => {
                    if (response.ok) {
                        // Remove from the custom dropdown
                        profileDropdown.removeChild(listItem);
                        // Remove from the hidden select
                        Array.from(profileSelect.options).forEach(option => {
                            if (option.value === profileName) {
                                profileSelect.removeChild(option);
                            }
                        });
                    } else {
                        alert('Error deleting profile');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });

            });

            // Add event to select profile from custom dropdown
            listItem.addEventListener('click', function() {
                selectedProfile.textContent = profile["profile_name"]; // Update the display
                profileSelect.value = profile["profile_name"]; // Set the value of hidden select
                profileDropdown.style.display = 'none'; // Close the dropdown

                fetch(`/api/v1/test/profile/${uri_get_param('test_name')}`)
                .then(response => response.json())
                .then(data => {
                    const result = data.find(item => item.profile_name === profile["profile_name"]);
                    Object.keys(result).forEach(key => {
                        const input = document.getElementById(key);
                        if (input) {
                            input.value = result[key];
                        }
                    });
                });
            });
        });
    });

    // Toggle dropdown on selected profile click
    selectedProfile.addEventListener('click', function() {
        console.log("selected Profile is clidcked!!!");
        if (profileDropdown.style.display === 'none' || profileDropdown.style.display === '') {
            profileDropdown.style.display = 'block'; // Show dropdown
        } else {
            profileDropdown.style.display = 'none'; // Hide dropdown
        }
    });


    // Close dropdown if clicked outside
    document.addEventListener('click', function(event) {
        if (!profileDropdown.contains(event.target) && event.target !== selectedProfile) {
            profileDropdown.style.display = 'none'; // Close dropdown
        }
    });

    // // Load profile when selected
    // profileSelect.addEventListener('change', function() {
    //     const selectedProfile = this.value;
    //     if (selectedProfile) {
    //         fetch(`/api/v1/test/profile/${uri_get_param('test_name')}`)
    //             .then(response => response.json())
    //             .then(data => {
    //                 const result = data.find(item => item.profile_name === selectedProfile);
    //                 Object.keys(result).forEach(key => {
    //                     const input = document.getElementById(key);
    //                     if (input) {
    //                         input.value = result[key];
    //                     }
    //                 });
    //             });
    //     }
    // });

    // Save profile
    saveProfileButton.addEventListener('click', function() {
            
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

        // Convert the form data to a JSON object
        const jsonData = {};
        for (let [key, value] of formData) {
            //Check value based on flatten_param_struct[key].type
            if (flatten_param_struct[key].type === 'NUMBER') {
                value = parseFloat(value);
            } else if (flatten_param_struct[key].type === 'STRING') {
                value = value;
            }

            jsonData[`${key}`] = value ? value : flatten_param_struct[key].value;
        }

        //Get profile name from user
        const profileName = prompt("Enter profile name:");
        if(!profileName){
            console.log("Operation Canceled");
            return;
        }
        jsonData["profile_name"] = profileName;


        console.log(`Form data is: ${JSON.stringify(jsonData, null, 2)}`);


        fetch(`/api/v1/test/profile/${uri_get_param('test_name')}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jsonData)
        }).then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const option = document.createElement('option');
                option.value = profileName;
                option.textContent = profileName;
                profileSelect.appendChild(option);
            }
        });
    });
});