async function showDashboard() {
    document.getElementById('main-content').innerHTML = `
        <div class="page active">
            <h2>Dashboard</h2>
            <div class="dashboard-grid" id="widget-container">
                <!-- widgets loaded dynamically -->
            </div>
        </div>
    `;
    try {
        const response = await apiFetch('/dashboards/widgets');
        const widgets = await response.json();
        const container = document.getElementById('widget-container');
        if (widgets.length === 0) {
            container.innerHTML = '<p>No widgets configured. Add some from API.</p>';
            return;
        }
        // simple widget rendering (mock data)
        widgets.forEach(w => {
            const div = document.createElement('div');
            div.className = 'widget';
            div.innerHTML = `<h3>${w.name}</h3><canvas id="chart-${w.id}"></canvas>`;
            container.appendChild(div);
            // draw placeholder chart with Chart.js (CDN already assumed or we can add)
            const ctx = document.getElementById(`chart-${w.id}`).getContext('2d');
            new Chart(ctx, {
                type: w.widget_type === 'bar' ? 'bar' : 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr'],
                    datasets: [{
                        label: w.name,
                        data: [12, 19, 3, 5],
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: { scales: { y: { beginAtZero: true } } }
            });
        });
    } catch (err) {
        alert('Dashboard error: ' + err.message);
    }
}

// include Chart.js via CDN in index.html (added below)