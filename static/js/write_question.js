
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


    const title = document.getElementById('title').value;
    const mainText = document.getElementById('main_text').value;
    const subject = document.getElementById('subject').value;

    const data = {
        title: title,
        main_text: mainText,
        subject: subject
    }

    fetch('/api/write_question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    })
    .then(response => response.json()) // parses response to JSON object which js can use
    .then(data => {
        if (data.success) {
            window.location.href = '/question_list'; 
        } else {
            showError(data.message);
        }

    })
}



// listen for the form to be submitted and handle it
document.getElementById('writeQuestion-form').addEventListener('submit', handleSubmit);