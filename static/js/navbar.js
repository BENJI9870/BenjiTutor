fetch("/api/is_logged_in")
.then(response => response.json())
.then(data => {
    if (data.success) {
        // logged in
        showLogout();

    } else {
        // not logged in
        showLogin();
    }
})



function showLogin() {
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');

    if (loginLink.classList.contains('d-none')) {
        loginLink.classList.remove('d-none');
    }
    if (!logoutLink.classList.contains('d-none')) {
        logoutLink.classList.add('d-none');
    }
    
}

function showLogout() {
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');

    if (!loginLink.classList.contains('d-none')) {
        loginLink.classList.add('d-none');
    }
    if (logoutLink.classList.contains('d-none')) {
        logoutLink.classList.remove('d-none');
    }
    
}