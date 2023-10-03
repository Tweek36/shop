$('#product-category').children().first().attr('disabled', true)
const clone = $('#attributes-form').clone()
const csrftoken = $.cookie('csrftoken');
$('#attributes-form').remove()
const baseURL = window.location.protocol + '//' + window.location.hostname;
let prev_attributes = new Set()
let attributes_to_del = new Set()

if ($('#product-form').attr('method') === "PUT") {
    $("#attributes-list option").each(function(index) {
        const form = clone.clone()
        form.attr('id', form.attr('id')+$(this).attr('id'))
        prev_attributes.add(form.attr('id'))
        form.children("#product-attribute-value").val($(this).val())
        form.children("#product-attribute-value").attr('name', 'value'+$(this).attr('id'))
        form.children("#product-attribute-value").attr('id', 'product-attribute-value'+$(this).attr('id'))
        form.children("#product-attribute-name").text($(this).text())
        form.children("#product-attribute-name").attr('id', 'product-attribute-name' + $(this).attr('id'))
        form.attr('hidden', false)
        form.appendTo($(".attributes__list"));
    })
}

$('#product-attributes').on('mousedown', 'option', function(e) {
    e.preventDefault();
    $(this).attr('selected', !$(this).attr('selected'));
    const form = clone.clone()
    if($(this).prop('selected')) {
        if (attributes_to_del.has(form.attr('id')+$(this).val())) {
            attributes_to_del.delete(form.attr('id')+$(this).val())
            $("#attributes-form"+$(this).val()).removeClass('del-attribute')
        } else {
            form.attr('id', form.attr('id')+$(this).val())
            form.children("#product-attribute-value").attr('name', 'value'+$(this).val())
            form.children("#product-attribute-value").attr('id', 'product-attribute-value'+$(this).val())
            form.children("#product-attribute-name").text($(this).text())
            form.children("#product-attribute-name").attr('id', 'product-attribute-name' + $(this).val())
            form.attr('hidden', false)
            form.appendTo($(".attributes__list"));
        }
    } else {
        if (prev_attributes.has(form.attr('id')+$(this).val())) {
            $("#attributes-form"+$(this).val()).toggleClass('del-attribute')
            attributes_to_del.add(form.attr('id')+$(this).val())
        } else {
            $("#attributes-form"+$(this).val()).remove()
        }
        if($('#category-check').is(':checked') && $(this).attr('category') !== $("#product-category").val()) {
            $(this).attr('hidden', true)
        }
    }
});

function hide_attributes(select, category) {
    select.find('option[category="' + category + '"]').attr('hidden', false)
    select.find('option:not([category="' + category + '"]):not([selected])').attr('hidden', true)
}

$('#category-check').change(function() {
    if ($(this).is(':checked')) {
        hide_attributes($('#product-attributes'), $("#product-category").val())
        console.log('Чекбокс отмечен');
    } else {
        $('#product-attributes').children().attr('hidden', false)
    }
});

$("#product-category").change(function() {
    $('#category-check').attr('disabled', false);
    if ($('#category-check').is(':checked')) {
        hide_attributes($('#product-attributes'), $(this).val())
    }
});

$("#product-form").submit(function(event) {
    event.preventDefault();
    for (attribute of attributes_to_del) {
        $('#'+attribute).children('input').val('del')
    }
    let data = $(this).serialize()
    console.log(data);
    $.ajax({
        type: $(this).attr('method'),
        url: $(this).attr('action'),
        headers: {
          'X-CSRFToken': csrftoken,
        },
        data: data,
        success: function(response) {
            console.log(response);
            window.location.href = baseURL + '/product/' + response.id;
        },
        error: function(response) {
            console.error(response);
        }
    });
  });