
// JavaScript para GameStore - Funciones básicas
console.log("🎮 GameStore Frontend cargado correctamente");

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM completamente cargado");
    
    // Auto-ocultar alerts después de 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.style.transition = 'opacity 0.5s';
                alert.style.opacity = '0';
                setTimeout(() => {
                    if (alert.parentNode) alert.remove();
                }, 500);
            }
        }, 5000);
    });
    
    // Mejorar botones de agregar al carrito
    const addToCartButtons = document.querySelectorAll('.btn-outline-primary');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const card = this.closest('.card');
            const title = card.querySelector('.card-title')?.textContent || 'Producto';
            
            // Feedback visual
            const originalText = this.textContent;
            this.textContent = '✅ Agregado!';
            this.classList.remove('btn-outline-primary');
            this.classList.add('btn-success');
            
            setTimeout(() => {
                this.textContent = originalText;
                this.classList.remove('btn-success');
                this.classList.add('btn-outline-primary');
            }, 2000);
            
            console.log(`🛒 ${title} agregado al carrito`);
        });
    });
    
    // Validación de formularios en tiempo real
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input[required]');
        
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (!this.value.trim()) {
                    this.classList.add('is-invalid');
                } else {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                }
            });
            
            input.addEventListener('input', function() {
                if (this.value.trim()) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                }
            });
        });
    });
    
    console.log("✅ JavaScript inicializado correctamente");
});

// Función para mostrar loading en botones
function showLoading(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Cargando...';
    button.disabled = true;
    return originalText;
}

// Función para restaurar botón
function restoreButton(button, originalText) {
    button.innerHTML = originalText;
    button.disabled = false;
}
