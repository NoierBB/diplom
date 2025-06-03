document.addEventListener('DOMContentLoaded', function() {
    // Анимация появления элементов
    const neonContainer = document.querySelector('.neon-container');
    if (neonContainer) {
        neonContainer.style.opacity = '0';
        setTimeout(() => {
            neonContainer.style.transition = 'opacity 0.8s ease';
            neonContainer.style.opacity = '1';
        }, 100);
    }
    
    // Удаление flash-сообщений через 5 секунд
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.transition = 'opacity 0.5s ease';
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 500);
        }, 5000);
    });
    
    // Добавление эффекта при наведении на кнопки
    const neonButtons = document.querySelectorAll('.neon-btn, .neon-link-btn');
    neonButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transition = 'all 0.3s ease';
        });
    });

    // Функционал для ленты новостей
document.addEventListener('DOMContentLoaded', function() {
    // Анимация загрузки
    animateElements();
    
    // Обработчик для кнопки "Опубликовать"
    const postButton = document.querySelector('.neon-post-input + .neon-btn');
    if (postButton) {
        postButton.addEventListener('click', function() {
            const postText = document.querySelector('.neon-post-input').value;
            if (postText.trim() !== '') {
                createPost('Вы', postText);
                document.querySelector('.neon-post-input').value = '';
            }
        });
    }
    
    // Обработчики для лайков
    document.querySelectorAll('.post-like').forEach(likeBtn => {
        likeBtn.addEventListener('click', function() {
            this.classList.toggle('liked');
            if (this.classList.contains('liked')) {
                const currentLikes = parseInt(this.textContent.match(/\d+/) || 0);
                this.innerHTML = '❤️ ' + (currentLikes + 1);
            } else {
                const currentLikes = parseInt(this.textContent.match(/\d+/) || 1);
                this.innerHTML = '❤️ ' + (currentLikes - 1);
            }
        });
    });
    
    // Обработчик для отправки сообщений
    const sendMessageBtn = document.querySelector('.message-compose .neon-btn');
    if (sendMessageBtn) {
        sendMessageBtn.addEventListener('click', function() {
            const messageText = document.querySelector('.message-compose textarea').value;
            if (messageText.trim() !== '') {
                // В реальном приложении здесь был бы AJAX-запрос
                alert('Сообщение отправлено: ' + messageText);
                document.querySelector('.message-compose textarea').value = '';
            }
        });
    }
});

function animateElements() {
    const elements = document.querySelectorAll('.neon-sidebar, .neon-main > *');
    elements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        setTimeout(() => {
            el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, 100 + index * 100);
    });
}

function createPost(author, content) {
    const feed = document.querySelector('.neon-feed');
    if (!feed) return;
    
    const postHTML = `
        <div class="post" style="opacity: 0; transform: translateY(20px);">
            <div class="post-header">
                <div class="post-avatar">${author[0].toUpperCase()}</div>
                <div class="post-author">${author}</div>
                <div class="post-time">только что</div>
            </div>
            <div class="post-content">${content}</div>
            <div class="post-actions">
                <button class="post-like">❤️ 0</button>
                <button class="post-comment">💬 0</button>
                <button class="post-share">↗️ Поделиться</button>
            </div>
        </div>
    `;
    
    const postContainer = document.createElement('div');
    postContainer.innerHTML = postHTML;
    const newPost = postContainer.firstChild;
    
    feed.insertBefore(newPost, feed.children[2]); // Вставляем после формы создания
    
    setTimeout(() => {
        newPost.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        newPost.style.opacity = '1';
        newPost.style.transform = 'translateY(0)';
    }, 100);
    
    // Добавляем обработчики для новых кнопок
    newPost.querySelector('.post-like').addEventListener('click', function() {
        this.classList.toggle('liked');
        if (this.classList.contains('liked')) {
            const currentLikes = parseInt(this.textContent.match(/\d+/) || 0);
            this.innerHTML = '❤️ ' + (currentLikes + 1);
        } else {
            const currentLikes = parseInt(this.textContent.match(/\d+/) || 1);
            this.innerHTML = '❤️ ' + (currentLikes - 1);
        }
    });
}
});
