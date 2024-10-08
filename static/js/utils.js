
function sendRequest(url, method, data=null, success_url=null) {
    const options = {
        method: method,
        headers: {
            'X-CSRFToken': getCsrfToken(),
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
    }        

    if(method === 'POST' || method === 'PUT'){
        options.body = data;
    }

    fetch(url, options)
    .then(response => {
        const contentType = response.headers.get('Content-Type');
        if(response.ok){
            if(contentType && contentType.includes('application/json')) 
                return response.json();
            return response.text();
        }
        else{
            throw new Error("Request failed with status code: " + response.status);
        }
    })
    .then(data => {
        if(data.message){
            showAlert(data.message);
            if(success_url){
                setTimeout(() => {
                    window.location.href = success_url;
                }, 2000);
            }
        }
        else if(success_url)
            window.location.href = success_url;
    })
    .catch(error => {
        console.log("Error: ", error);
        showAlert("An error has occurred", 'danger');
    })
}

function getCsrfToken(){
    const tokenElement = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return tokenElement ? tokenElement.value : '';
}

function showAlert(message, type='success'){
    const alertContainer = document.body;

    const myAlert = document.createElement('div');
    myAlert.textContent = message;
    myAlert.style.backgroundColor = type === 'success' ? '#28a745' : '#dc3545';
    myAlert.style.color = '#fff';
    myAlert.style.padding = '10px';
    myAlert.style.borderRadius = '5px';
    myAlert.style.position = 'fixed';
    myAlert.style.top = '10px';
    myAlert.style.right = '10px';
    myAlert.style.zIndex = '1000';
    myAlert.style.display = 'inline-block';
    myAlert.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';

    alertContainer.appendChild(myAlert);

    setTimeout(() => {
        alertContainer.removeChild(myAlert);
    }, 2000);
}