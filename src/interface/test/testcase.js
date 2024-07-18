

function uri_get_param(name){
    if(name=(new RegExp('[?&]'+encodeURIComponent(name)+'=([^&]*)')).exec(location.search))
        return decodeURIComponent(name[1]);
}
 

fetch("/api/v1/test/get_params/" + uri_get_param('test_name'),
{
    method: "GET",
    headers: {
        "Content-type": "application/json",
    },
})
.then((response) => response.json())
.then((json) => update_form(json, document.getElementById("param-form"), 0));

function update_form(params, targetElement, level) {
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

// //The function which validates and processes the form data when submit is clicked
// function process_form_data() {
//     // Get the form element
//     const formElement = document.getElementById('param-form');

//     // Get the form data
//     const formData = new FormData(formElement);

//     // Convert the form data to a JSON object
//     const jsonData = {};
//     for (let [key, value] of formData) {
//         jsonData[key] = value;
//     }

//     // Log the JSON object to the console
//     console.log(jsonData);

//     // Send the JSON object to the server
//     fetch("/api/v1/test/process_params/" + uri_get_param('test_name'),
//     {
//         method: "POST",
//         headers: {
//             "Content-type": "application/json",
//         },
//         body: JSON.stringify(jsonData),
//     })
//     .then((response) => response.json())
//     .then((json) => console.log(json));
// }


