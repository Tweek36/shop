const btn = document.getElementById("open_login");
const modal = document.getElementById("login");
const closeBtn = document.getElementById("close-modal");

// открываем модальное окно при нажатии на кнопку
btn.onclick = function() {
  modal.showModal();
}
  

// закрываем модальное окно при нажатии на кнопку "Закрыть"
closeBtn.onclick = function() {
  modal.close();
}

modal.addEventListener('click', function (e) {
    if(!e.target.closest('form')) {
        e.target.close();
    }  
});