document.addEventListener('DOMContentLoaded', function() {
    // Check if user is already logged in
    const user = localStorage.getItem('user');
    if (user) {
        // Redirect to dashboard
        window.location.href = 'dashboard.html';
    }

    // Get form elements
    const loginForm = document.getElementById('login-form');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const loginButton = document.querySelector('#login-btn');
    const errorMessage = document.getElementById('login-error');
    
    // Toggle password visibility
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
    
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const input = this.previousElementSibling;
            
            // Toggle password visibility
            if (input.type === 'password') {
                input.type = 'text';
                this.classList.remove('fa-eye-slash');
                this.classList.add('fa-eye');
            } else {
                input.type = 'password';
                this.classList.remove('fa-eye');
                this.classList.add('fa-eye-slash');
            }
        });
    });
    
    // Login form submission
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Reset any error messages
            if (errorMessage) {
                errorMessage.textContent = '';
                errorMessage.classList.remove('show');
            }
            
            // Get form data
            const email = emailInput ? emailInput.value.trim() : 'test@example.com';
            const password = passwordInput ? passwordInput.value.trim() : 'password123';
            
            // For presentation, skip validation and proceed directly
            // Set loading state
            if (loginButton) {
                loginButton.classList.add('loading');
                loginButton.disabled = true;
            }
            
            // Create mock user info for presentation
            const mockUser = {
                name: email.split('@')[0],
                email: email || 'test@example.com',
                id: Math.floor(Math.random() * 1000)
            };
            
            // Save mock authentication data directly
            const mockToken = 'mock-token-' + Date.now();
            localStorage.setItem('authToken', mockToken);
            localStorage.setItem('user', JSON.stringify(mockUser));
            
            console.log('Login successful with:', mockUser);
            
            // Always redirect to dashboard for presentation
            window.location.href = 'dashboard.html';
        });
    }
    
    // Add floating label effect
    const inputs = document.querySelectorAll('input');
    
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            const parent = this.closest('.input-container');
            if (parent) parent.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            const parent = this.closest('.input-container');
            if (parent && this.value === '') {
                parent.classList.remove('focused');
            }
        });
        
        // Check if input has value on page load
        if (input.value !== '') {
            const parent = input.closest('.input-container');
            if (parent) parent.classList.add('focused');
        }
    });
});