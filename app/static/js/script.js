// Modern SaaS Login Form JavaScript login
class ModernSaaSLoginForm {
    constructor() {
        this.form = document.getElementById('loginForm');
        this.emailInput = document.getElementById('email');
        this.passwordInput = document.getElementById('password');
        this.passwordToggle = document.getElementById('passwordToggle');
        this.submitButton = this.form.querySelector('.submit-btn');
        this.successMessage = document.getElementById('successMessage');
        this.socialButtons = document.querySelectorAll('.social-btn');
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.setupPasswordToggle();
        this.setupSocialButtons();
    }
    
    bindEvents() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        this.emailInput.addEventListener('blur', () => this.validateEmail());
        this.passwordInput.addEventListener('blur', () => this.validatePassword());
        this.emailInput.addEventListener('input', () => this.clearError('email'));
        this.passwordInput.addEventListener('input', () => this.clearError('password'));
    }
    
    setupPasswordToggle() {

        if (!this.passwordToggle) {
            return;
        }
        this.passwordToggle.addEventListener('click', () => {
            const type = this.passwordInput.type === 'password' ? 'text' : 'password';
            this.passwordInput.type = type;
            
            // Simple visual feedback
            this.passwordToggle.style.color = type === 'text' ? '#635BFF' : '#8792a2';
        });
    }
    
    setupSocialButtons() {
        this.socialButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const provider = button.textContent.trim();
                this.handleSocialLogin(provider, button);
            });
        });
    }
    
    validateEmail() {
        const email = this.emailInput.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        if (!email) {
            this.showError('email', 'Se requiere correo electrónico');
            return false;
        }
        
        if (!emailRegex.test(email)) {
            this.showError('email', 'Por favor, introduce una dirección de correo electrónico válida');
            return false;
        }
        
        this.clearError('email');
        return true;
    }
    
    validatePassword() {
        const password = this.passwordInput.value;
        
        if (!password) {
            this.showError('password', 'Se requiere contraseña');
            return false;
        }
        
        if (password.length < 6) {
            this.showError('password', 'La contraseña debe tener al menos 6 caracteres');
            return false;
        }
        
        this.clearError('password');
        return true;
    }
    
    showError(field, message) {
        const inputGroup = document.getElementById(field).closest('.input-group');
        const errorElement = document.getElementById(`${field}Error`);
        
        inputGroup.classList.add('error');
        errorElement.textContent = message;
        errorElement.classList.add('show');
    }
    
    clearError(field) {
        const inputGroup = document.getElementById(field).closest('.input-group');
        const errorElement = document.getElementById(`${field}Error`);
        
        inputGroup.classList.remove('error');
        errorElement.classList.remove('show');
        setTimeout(() => {
            errorElement.textContent = '';
        }, 200);
    }
    
    async handleSubmit(e) {
        e.preventDefault();
        
        const isEmailValid = this.validateEmail();
        const isPasswordValid = this.validatePassword();
        
        if (!isEmailValid || !isPasswordValid) {
            return;
        }
        
        this.setLoading(true);
        
        try {
            // Simulate authentication
            await new Promise(resolve => setTimeout(resolve, 1800));
            
            // Show success
            this.showSuccess();
        } catch (error) {
            this.showError('password', 'Error al iniciar sesión. Inténtalo de nuevo.');
        } finally {
            this.setLoading(false);
        }
    }
    
    async handleSocialLogin(provider, button) {
        console.log(`Signing in with ${provider}...`);
        
        // Simple loading state
        const originalHTML = button.innerHTML;
        button.style.pointerEvents = 'none';
        button.style.opacity = '0.7';
        button.innerHTML = `
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                <circle cx="7" cy="7" r="5.5" stroke="currentColor" stroke-width="1.5" opacity="0.25"/>
                <path d="M12.5 7a5.5 5.5 0 01-5.5 5.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
                    <animateTransform attributeName="transform" type="rotate" dur="1s" values="0 7 7;360 7 7" repeatCount="indefinite"/>
                </path>
            </svg>
            Connecting...
        `;
        
        try {
            await new Promise(resolve => setTimeout(resolve, 1500));
            console.log(`Redirecting to ${provider} authentication...`);
            // window.location.href = `/auth/${provider.toLowerCase()}`;
        } catch (error) {
            console.error(`${provider} sign in failed: ${error.message}`);
        } finally {
            button.style.pointerEvents = 'auto';
            button.style.opacity = '1';
            button.innerHTML = originalHTML;
        }
    }
    
    setLoading(loading) {
        this.submitButton.classList.toggle('loading', loading);
        this.submitButton.disabled = loading;
        
        // Disable social buttons during loading
        this.socialButtons.forEach(button => {
            button.style.pointerEvents = loading ? 'none' : 'auto';
            button.style.opacity = loading ? '0.6' : '1';
        });
    }
    
    showSuccess() {
        // Hide form with smooth transition
        this.form.style.transform = 'scale(0.95)';
        this.form.style.opacity = '0';
        
        setTimeout(() => {
            this.form.style.display = 'none';
            document.querySelector('.social-buttons').style.display = 'none';
            document.querySelector('.signup-link').style.display = 'none';
            document.querySelector('.divider').style.display = 'none';
            
            // Show success message
            this.successMessage.classList.add('show');
            
        }, 300);
        
        // Redirect after success display
        setTimeout(() => {
            console.log('Redirecting to dashboard...');
            // window.location.href = '/dashboard';
        }, 2500);
    }
}

// Initialize the form when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ModernSaaSLoginForm();
    const form = document.getElementById('loginForm');
    if (!form) {
        return;
    }

    const formType = form.dataset.formType || 'login';

    if (formType === 'login') {
        new ModernSaaSLoginForm();
    } else {
        setupRegisterForm(form);
    }
});

    function setupRegisterForm(form) {
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const requiredFields = form.querySelectorAll('input[required], select[required], textarea[required]');
        for (const field of requiredFields) {
            if (!field.value || !field.value.trim()) {
                const label = field.dataset.label || field.name;
                flashMessage(`Por favor, completa el campo "${label}".`, 'danger');
                field.focus();
                return;
            }
        }
    
        const emailInput = form.querySelector('#email');
        if (emailInput && !isValidEmail(emailInput.value)) {
            flashMessage('Por favor, ingresa un correo electrónico válido.', 'danger');
            emailInput.focus();
            return;
        }

        const passwordInput = form.querySelector('#password');
        const confirmPasswordInput = form.querySelector('#confirm_password');
        const password = passwordInput ? passwordInput.value : '';
        const confirmPassword = confirmPasswordInput ? confirmPasswordInput.value : '';
   
        if (passwordInput && password.length < 6) {
            flashMessage('La contraseña debe tener al menos 6 caracteres.', 'danger');
            passwordInput.focus();
            return;
        }
    
        if (confirmPasswordInput && password !== confirmPassword) {
            flashMessage('Las contraseñas no coinciden.', 'danger');
            confirmPasswordInput.focus();
            return;
        }
        const submitBtn = form.querySelector('.submit-btn');
        const loader = form.querySelector('.btn-loader');

        if (submitBtn) {
            submitBtn.disabled = true;
        }

        if (loader) {
            loader.style.display = 'block';
        }

        setTimeout(() => {
            form.submit();
        }, 500);
    });
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}


// Función para mostrar los mensajes de error
function flashMessage(message, type) {
    var messageContainer = document.createElement('div');
    messageContainer.classList.add('alert', `alert-${type}`);
    messageContainer.textContent = message;

    document.querySelector('.login-container').prepend(messageContainer);
    setTimeout(() => messageContainer.remove(), 3000);
}