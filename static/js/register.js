
function showError(message) {
    document.getElementById('error-message').innerText = message;
    // remove the d-none class if it is there
    document.getElementById('error-message').classList.remove('d-none');
}

function clearError() {
    document.getElementById('error').innerText = '';
    // add the d-none class if it is not there
    document.getElementById('error').classList.add('d-none');
}


function handleSubmit(e) {
    e.preventDefault(); // This prevents the page from refreshing which is the default action of the form element   


    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    const data = {
        firstName: firstName,
        lastName: lastName,
        email: email,
        password: password,
        confirmPassword: confirmPassword
    }

    fetch('/api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    })
    .then(response => response.json()) // parses response to JSON object which js can use
    .then(data => {
        if (data.success) {
            window.location.href = '/'; // redirect to home page. TODO: decide where you want to redirect to
        } else {
            showError(data.message);
        }

    })
}



// listen for the form to be submitted and handle it
document.getElementById('register-form').addEventListener('submit', handleSubmit);