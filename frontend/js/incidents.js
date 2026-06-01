async function showIncidents() {
    document.getElementById('main-content').innerHTML = `
        <div class="page active">
            <h2>Incidents</h2>
            <button id="new-incident-btn">Create New</button>
            <table class="table" id="incidents-table">
                <thead><tr><th>ID</th><th>Title</th><th>Status</th><th>Severity</th><th>Created</th><th>Actions</th></tr></thead>
                <tbody></tbody>
            </table>
        </div>
    `;
    document.getElementById('new-incident-btn').addEventListener('click', showIncidentForm);
    await loadIncidents();
}

async function loadIncidents() {
    try {
        const response = await apiFetch('/incidents/');
        const incidents = await response.json();
        const tbody = document.querySelector('#incidents-table tbody');
        tbody.innerHTML = incidents.map(inc => `
            <tr>
                <td>${inc.id}</td>
                <td><a href="#" class="incident-link" data-id="${inc.id}">${inc.title}</a></td>
                <td><span class="status-badge status-${inc.status}">${inc.status}</span></td>
                <td class="severity-${inc.severity}">${inc.severity}</td>
                <td>${new Date(inc.created_at).toLocaleString()}</td>
                <td><button class="delete-incident" data-id="${inc.id}">Delete</button></td>
            </tr>
        `).join('');
        document.querySelectorAll('.incident-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                viewIncident(link.dataset.id);
            });
        });
        document.querySelectorAll('.delete-incident').forEach(btn => {
            btn.addEventListener('click', async () => {
                if (confirm('Delete incident?')) {
                    await apiFetch(`/incidents/${btn.dataset.id}`, { method: 'DELETE' });
                    loadIncidents();
                }
            });
        });
    } catch (err) {
        alert('Failed to load incidents: ' + err.message);
    }
}

function showIncidentForm() {
    document.getElementById('main-content').innerHTML = `
        <div class="page active">
            <h2>New Incident</h2>
            <form id="incident-form">
                <div class="form-group"><label>Title</label><input name="title" required /></div>
                <div class="form-group"><label>Description</label><textarea name="description"></textarea></div>
                <div class="form-group"><label>Status</label>
                    <select name="status">
                        <option value="open">Open</option>
                        <option value="in_progress">In Progress</option>
                        <option value="resolved">Resolved</option>
                    </select>
                </div>
                <div class="form-group"><label>Severity</label>
                    <select name="severity">
                        <option value="low">Low</option>
                        <option value="medium" selected>Medium</option>
                        <option value="high">High</option>
                        <option value="critical">Critical</option>
                    </select>
                </div>
                <button type="submit">Create</button>
            </form>
        </div>
    `;
    document.getElementById('incident-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData);
        try {
            await apiFetch('/incidents/', { method: 'POST', body: JSON.stringify(data) });
            showIncidents();
        } catch (err) {
            alert('Error: ' + err.message);
        }
    });
}

async function viewIncident(id) {
    try {
        const response = await apiFetch(`/incidents/${id}`);
        const inc = await response.json();
        // also fetch logs
        const logsResponse = await apiFetch(`/logs/?incident_id=${id}`);
        const logs = await logsResponse.json();
        // AI analysis placeholder (triggered or fetched)
        document.getElementById('main-content').innerHTML = `
            <div class="page active">
                <h2>Incident #${inc.id}: ${inc.title}</h2>
                <div class="incident-detail">
                    <p><strong>Status:</strong> ${inc.status}</p>
                    <p><strong>Severity:</strong> ${inc.severity}</p>
                    <p><strong>Description:</strong> ${inc.description || 'N/A'}</p>
                </div>
                <button id="run-ai-analysis">Run AI Analysis</button>
                <div id="analysis-result"></div>
                <h3>Logs</h3>
                <ul class="log-list" id="log-list">
                    ${logs.map(log => `<li class="log-entry"><span class="log-level">${log.level}</span> ${log.message} <small>${new Date(log.timestamp).toLocaleString()}</small></li>`).join('')}
                </ul>
            </div>
        `;
        document.getElementById('run-ai-analysis').addEventListener('click', async () => {
            // Trigger AI analysis via API or worker; for demo we'll call a mock endpoint (not implemented yet)
            // In production, we'd send a message to queue; here we'll simulate:
            alert('AI analysis triggered! Check back soon.');
        });
    } catch (err) {
        alert('Error viewing incident: ' + err.message);
    }
}