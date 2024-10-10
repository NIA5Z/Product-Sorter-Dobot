document.getElementById('fetchPosition').addEventListener('click', async () => {
    try {
        const response = await fetch('/BotPosition');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        
        const tableBody = document.getElementById('positionTable').getElementsByTagName('tbody')[0];
        tableBody.innerHTML = ''; // Clear previous data

        const newRow = tableBody.insertRow();
        newRow.insertCell(0).textContent = data.x || 'N/A';
        newRow.insertCell(1).textContent = data.y || 'N/A';
        newRow.insertCell(2).textContent = data.z || 'N/A';
        newRow.insertCell(3).textContent = data.r || 'N/A';
        newRow.insertCell(4).textContent = data.j1 || 'N/A';
        newRow.insertCell(5).textContent = data.j2 || 'N/A';
        newRow.insertCell(6).textContent = data.j3 || 'N/A';
        newRow.insertCell(7).textContent = data.j4 || 'N/A';
    } catch (error) {
        console.error('Error fetching bot position:', error);
        alert('Failed to fetch position data.');
    }
});