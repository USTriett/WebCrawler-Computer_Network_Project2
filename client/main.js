const pElement = document.getElementById('demo')

function postMethod() {
    console.log('hi')
    fetch('http://127.0.0.1:8000/testGet', {method : 'POST'})
    .then(res => res.json())
    .then(response => console.log('Success:', JSON.stringify(response)))
    .catch(error => console.error('Error:', error))
}

