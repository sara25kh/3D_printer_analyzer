

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

function update_form(params, element, level) {
    console.log('params:', params);

    // Get the target element where the textboxes will be added
    const targetElement = document.getElementById(element);

    // Clear the target element's existing content
    //targetElement.innerHTML = '';

    // Iterate over the keys in the params object
    for (let key in params) {
        if (params.hasOwnProperty(key)) {
            // Create a container div for each input field
            const containerDiv = document.createElement('div');

            // Create a label for the input
            const label = document.createElement('label');
            label.setAttribute('for', key);
            label.textContent = key;
            containerDiv.appendChild(label);

            // Create the input textbox
            const input = document.createElement('input');
            input.setAttribute('type', 'text');
            input.setAttribute('id', key);
            input.setAttribute('name', key);
            input.setAttribute('value', params[key]);

            // Append the input textbox to the container div
            containerDiv.appendChild(input);

            // Append the container div to the target element
            targetElement.appendChild(containerDiv);
        }
    }
}


