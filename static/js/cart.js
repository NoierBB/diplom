document.addEventListener('DOMContentLoaded', function() {
    // Обработчик для кнопок "В корзину"
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            const productId = this.closest('.product-card').dataset.productId;
            
            try {
                const response = await fetch(`/add-to-cart/${productId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                const data = await response.json();
                
                if (data.success) {
                    updateCartCounter(data.cart_total);
                    showAddToCartSuccess();
                }
            } catch (error) {
                console.error('Ошибка при добавлении в корзину:', error);
            }
        });
    });
    
    // Обновление счетчика корзины
    function updateCartCounter(count) {
        const cartCounter = document.querySelector('.cart-count');
        if (cartCounter) {
            cartCounter.textContent = count;
            cartCounter.style.display = count > 0 ? 'inline-block' : 'none';
        }
    }
    
    // Показ уведомления о добавлении
    function showAddToCartSuccess() {
        const notification = document.createElement('div');
        notification.className = 'cart-notification';
        notification.innerHTML = `
            <div class="notification-content">
                <i class="bi bi-check-circle"></i>
                Товар добавлен в корзину
            </div>
        `;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
        button.classList.add('added');
        setTimeout(() => button.classList.remove('added'), 1000);
    }


});