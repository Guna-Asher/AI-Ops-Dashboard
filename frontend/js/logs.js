async function showLogs() {
    document.getElementById('main-content').innerHTML = `
        <div class="page active">
            <h2>Logs</h2>
            <table class="table" id="logs-table">
                <thead><tr><th>ID</th><th>Timestamp</th><th>Level</th><th>Message</th><th>Source</th></tr></thead>
                <tbody></tbody>
            </table>
        </div>
    `;
    try {
        const response = await apiFetch('/logs/');
        const logs = await response.json();
        const tbody = document.querySelector('#logs-table tbody');
        tbody.innerHTML = logs.map(log => `
            <tr>
                <td>${log.id}</td>
                <td>${new Date(log.timestamp).toLocaleString()}</td>
                <td>${log.level}</td>
                <td>${log.message}</td>
                <td>${log.source || ''}</td>
            </tr>
        `).join('');
    } catch (err) {
        alert('Failed to load logs: ' + err.message);
    }
}