const API_BASE = '/api/v1';

async function apiFetch(url, options = {}) {
    const token = localStorage.getItem('access_token');
    const headers = {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
    };
    const response = await fetch(API_BASE + url, { ...options, headers });
    if (response.status === 401) {
        // attempt token refresh
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
            const refreshResponse = await fetch(API_BASE + '/auth/refresh', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh_token: refreshToken })
            });
            if (refreshResponse.ok) {
                const data = await refreshResponse.json();
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('refresh_token', data.refresh_token);
                // retry original request
                headers.Authorization = `Bearer ${data.access_token}`;
                return fetch(API_BASE + url, { ...options, headers });
            }
        }
        logout();
        throw new Error('Session expired');
    }
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || response.statusText);
    }
    return response;
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.reload();
}