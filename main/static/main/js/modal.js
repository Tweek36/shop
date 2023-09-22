const btn = document.getElementById("open_login");
const modal = document.getElementById("registration");
const closeBtn = document.getElementById("close-modal");
const btn_logout = document.getElementById("logout");

// Функция для получения CSRF-токена из cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    console.log(cookies);
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

if(btn){
  btn.onclick = function() {
    modal.showModal();
  }
} 
if (btn_logout) {
  btn_logout.onclick = function() {
    // Получаем CSRF-токен из cookies
    const csrftoken = getCookie('csrftoken');
  
    fetch('/logout/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken, // Передача CSRF-токена в заголовке
      },
    })
    .then(response => {
      if (response.ok) {
        console.log('Вы успешно вышли из системы.');
      } else {
        console.error('Произошла ошибка при выходе из системы.');
      }
    })
    .catch(error => {
      console.error('Произошла ошибка при выполнении запроса:', error);
    });
  }
}


if (closeBtn) {
  closeBtn.onclick = function() {
    modal.close();
  }
}

modal.addEventListener('click', function (e) {
    if(!e.target.closest('form')) {
        e.target.close();
    }  
});