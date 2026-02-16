document.addEventListener('DOMContentLoaded', function() {
    
    // Анимация карточек
    const cards = document.querySelectorAll('.brick-card, .feature-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });

    // Кнопки "В корзину"
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const id = this.dataset.id;
            
            fetch('/api/cart/add', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({id: parseInt(id), quantity: 1})
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    showNotification('✅ Товар добавлен в корзину!');
                    updateCartCount();
                    
                    // Анимация кнопки
                    this.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        this.style.transform = 'scale(1)';
                    }, 200);
                }
            });
        });
    });

    // Фильтрация
    const filterButtons = document.querySelectorAll('.filter-btn');
    const catalogItems = document.querySelectorAll('.brick-card');
    
    if (filterButtons.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                filterButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                
                const filterValue = this.dataset.filter;
                
                catalogItems.forEach(item => {
                    if (filterValue === 'all' || item.dataset.color === filterValue) {
                        item.style.display = 'flex';
                        setTimeout(() => {
                            item.style.opacity = '1';
                            item.style.transform = 'scale(1)';
                        }, 10);
                    } else {
                        item.style.opacity = '0';
                        item.style.transform = 'scale(0.8)';
                        setTimeout(() => {
                            item.style.display = 'none';
                        }, 300);
                    }
                });
            });
        });
    }
});

// Обновление счётчика корзины
function updateCartCount() {
    fetch('/api/cart/count')
        .then(res => res.json())
        .then(data => {
            const el = document.getElementById('cart-count');
            if (el) el.textContent = data.count;
        });
}

// Уведомления
function showNotification(message) {
    const oldNotifications = document.querySelectorAll('.notification');
    oldNotifications.forEach(n => n.remove());
    
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Кнопка "Наверх"
window.addEventListener('scroll', function() {
    let btn = document.querySelector('.scroll-top');
    
    if (!btn) {
        btn = document.createElement('button');
        btn.className = 'scroll-top';
        btn.innerHTML = '⬆';
        btn.style.cssText = `
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 50px;
            height: 50px;
            background: #c41e3a;
            color: white;
            border: none;
            border-radius: 50%;
            cursor: pointer;
            display: none;
            font-size: 24px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            z-index: 999;
        `;
        
        btn.addEventListener('click', function() {
            window.scrollTo({top: 0, behavior: 'smooth'});
        });
        
        document.body.appendChild(btn);
    }
    
    btn.style.display = window.scrollY > 300 ? 'block' : 'none';
});

// Обновляем счётчик при загрузке
updateCartCount();