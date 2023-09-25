$(document).ready(function() {
  const btn_login = $("#open_login");
  const modal_registration = $("#registration");
  const modal_authentication = $("#authentication");
  const closeBtn = $("#close-modal");
  const btn_logout = $("#logout");
  const change_registration = $("#change_registration");
  const change_authentication = $("#change_authentication");
  const csrftoken = $.cookie('csrftoken');

  change_registration.on("click", function() {
    modal_registration.get(0).close();
    modal_authentication.get(0).showModal();
  });

  change_authentication.on("click", function() {
    modal_authentication.get(0).close();
    modal_registration.get(0).showModal();
  });

  $("#login").submit(function(event) {
    event.preventDefault();  // Предотвращаем стандартное поведение отправки формы
    // Отправляем данные формы на сервер через AJAX
    $.ajax({
        type: "POST",
        url: $(this).attr('action'),  // Замените на правильный URL
        headers: {
          'X-CSRFToken': csrftoken, // Передача CSRF-токена в заголовке
        },
        data: $(this).serialize(),
        success: function(response) {
            // Обработка успешного ответа от сервера (например, вывод сообщения)
            console.log(response);
            location.reload();
        },
        error: function(response) {
            // Обработка ошибки (например, вывод сообщения об ошибке)
            console.error(response);
        }
    });
  });

  $("#register").submit(function(event) {
    event.preventDefault();  // Предотвращаем стандартное поведение отправки формы

    // Отправляем данные формы на сервер через AJAX
    $.ajax({
        type: "POST",
        url: $(this).attr('action'),  // Замените на правильный URL
        headers: {
          'X-CSRFToken': csrftoken, // Передача CSRF-токена в заголовке
        },
        data: $(this).serialize(),
        success: function(response) {
            // Обработка успешного ответа от сервера (например, вывод сообщения)
            console.log(response);
            location.reload();
        },
        error: function(response) {
            // Обработка ошибки (например, вывод сообщения об ошибке)
            console.error(response);
        }
    });
  });

  if (btn_login.length > 0) {
    btn_login.on("click", function() {
      modal_registration.get(0).showModal();
    });
  }

  if (btn_logout.length > 0) {
    btn_logout.on("click", function() {
      $.ajax({
        url: '/logout/',
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken, // Передача CSRF-токена в заголовке
        },
        success: function(response) {
          console.log('Вы успешно вышли из системы.');
          location.reload();
        },
        error: function(error) {
          console.error('Произошла ошибка при выходе из системы.');
        }
      });
    });
  }

  if (closeBtn.length > 0) {
    closeBtn.on("click", function() {
      modal_registration.get(0).close();
      modal_authentication.get(0).close();
    });
  }

  modal_registration.on("click", function(e) {
    if (!$(e.target).closest('form').length) {
      modal_registration.get(0).close();
    }
  });

  modal_authentication.on("click", function(e) {
    if (!$(e.target).closest('form').length) {
      modal_authentication.get(0).close();
    }
  });
});
