

function uri_get_param(name){
    if(name=(new RegExp('[?&]'+encodeURIComponent(name)+'=([^&]*)')).exec(location.search))
        return decodeURIComponent(name[1]);
}
 
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
    
        // Create the input textbox
        const input = document.createElement('input');
        input.setAttribute('type', 'text');
        input.setAttribute('id', key_label);
        input.setAttribute('name', key_label);
        input.setAttribute('placeholder', `default: ${param.value}`);
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

        jsonData[key] = value ? value : flatten_param_struct[key].value;
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
    .then((json) => console.log(json));

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


// Get the submit button
const submitButton = document.getElementById('submit-form');

// Add an event listener to the submit button
submitButton.addEventListener('click', submit_form_data);


