async function checkAuth() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        showLoginForm();
        return;
    }
    // validate token by fetching user info (optional)
    document.getElementById('logout-btn').style.display = 'inline-block';
    document.getElementById('auth-section').innerHTML = `
        <span id="user-email">Logged in</span>
        <button id="logout-btn">Logout</button>
    `;
    document.getElementById('logout-btn').addEventListener('click', logout);
    showIncidents(); // default page
}

async function showLoginForm() {
    document.getElementById('main-content').innerHTML = `
        <div class="page active">
            <h2>Login</h2>
            <div id="login-error" style="color:red"></div>
            <form id="login-form">
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" name="email" required />
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password" required />
                </div>
                <button type="submit">Login</button>
            </form>
            <p style="margin-top:1rem">Don't have an account? <a href="#" id="show-register">Register</a></p>
        </div>
    `;
    document.getElementById('login-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        try {
            const response = await fetch(API_BASE + '/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams({ username: formData.get('email'), password: formData.get('password') })
            });
            if (!response.ok) throw new Error('Invalid credentials');
            const data = await response.json();
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);
            window.location.reload();
        } catch (err) {
            document.getElementById('login-error').textContent = err.message;
        }
    });
    document.getElementById('show-register').addEventListener('click', showRegisterForm);
}

async function showRegisterForm() {
    document.getElementById('main-content').innerHTML = `
        <div class="page active">
            <h2>Register</h2>
            <div id="register-error" style="color:red"></div>
            <form id="register-form">
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" name="email" required />
                </div>
                <div class="form-group">
                    <label>Full Name</label>
                    <input type="text" name="full_name" />
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password" required />
                </div>
                <button type="submit">Register</button>
            </form>
            <p>Already have an account? <a href="#" id="show-login">Login</a></p>
        </div>
    `;
    document.getElementById('register-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        try {
            const response = await fetch(API_BASE + '/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(Object.fromEntries(formData))
            });
            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail);
            }
            alert('Registration successful. Please login.');
            showLoginForm();
        } catch (err) {
            document.getElementById('register-error').textContent = err.message;
        }
    });
    document.getElementById('show-login').addEventListener('click', showLoginForm);
}