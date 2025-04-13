document.addEventListener('DOMContentLoaded', function() {
    // Check if user is already logged in
    const user = localStorage.getItem('user');
    if (user) {
        // Redirect to dashboard
        window.location.href = 'dashboard.html';
    }

    // Get form elements
    const signupForm = document.getElementById('signup-form');
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm-password');
    const roleSelect = document.getElementById('role');
    const signupBtn = document.querySelector('#signup-btn');
    const errorMessage = document.getElementById('signup-error');
    
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
    
    // Signup form submission
    if (signupForm) {
        signupForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Reset any error messages
            if (errorMessage) {
                errorMessage.textContent = '';
                errorMessage.classList.remove('show');
            }
            
            // Get form data
            const name = nameInput ? nameInput.value.trim() : 'Test User';
            const email = emailInput ? emailInput.value.trim() : 'test@example.com';
            const password = passwordInput ? passwordInput.value.trim() : 'password123';
            const confirmPassword = confirmPasswordInput ? confirmPasswordInput.value.trim() : password;
            const role = roleSelect ? roleSelect.value : 'traveler';
            
            // For presentation, skip validation and proceed directly
            // Set loading state
            if (signupBtn) {
                signupBtn.classList.add('loading');
                signupBtn.disabled = true;
            }
            
            try {
                // Create mock user info for presentation
                const mockUser = {
                    name: name || 'Test User',
                    email: email || 'test@example.com',
                    role: role || 'traveler',
                    id: Math.floor(Math.random() * 1000)
                };
                
                // Save mock authentication data directly
                const mockToken = 'mock-token-' + Date.now();
                localStorage.setItem('authToken', mockToken);
                localStorage.setItem('user', JSON.stringify(mockUser));
                
                console.log('Signup successful with:', mockUser);
                
                // Always redirect to dashboard for presentation
                window.location.href = 'dashboard.html';
                
            } catch (error) {
                // This won't happen with our mock but keep for debugging
                console.error('Signup error:', error);
                
                // Always succeed for presentation
                const mockUser = {
                    name: name || 'Test User',
                    email: email || 'test@example.com',
                    role: role || 'traveler',
                    id: Math.floor(Math.random() * 1000)
                };
                localStorage.setItem('authToken', 'mock-token-' + Date.now());
                localStorage.setItem('user', JSON.stringify(mockUser));
                
                // Redirect regardless of error
                window.location.href = 'dashboard.html';
            }
        });
    }
    
    // Add floating label effect
    const inputs = document.querySelectorAll('input, select');
    
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