async function callAPI(endpoint) {
    try {
        const response = await fetch(`${endpoint}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log(data); 
    } catch (error) {
        console.error('Error:', error);
    }
}

document.getElementById('start-btn').addEventListener('click', () => {
    callAPI('start');
});

document.getElementById('close-btn').addEventListener('click', () => {
    callAPI('close');
});

document.getElementById('home-btn').addEventListener('click', () => {
    callAPI('home'); 
});

document.getElementById('position-btn').addEventListener('click', () => {
    callAPI('position');
});