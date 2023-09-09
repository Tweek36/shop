$( document ).ready(function(){
    const csrftoken = getCookie('csrftoken');

    $('.product__del').click(function(){
        const id = $(this).parent().prop('id')
        $.ajax({
            url: "/edit/edit_ajax/",
            headers: {'X-CSRFToken': csrftoken},
            data: {'url': id},
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(xhr, status, error) {
                console.log("Error:", error, status, xhr);
            }
        });
    })
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Имя начинается с csrftoken=
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}