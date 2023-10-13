$('#product-category').children().first().attr('disabled', true)
const csrftoken = $.cookie('csrftoken');
const baseURL = window.location.protocol + '//' + window.location.hostname;
let prev_attributes = new Set()
let attributes_to_del = new Set()

const attributes_form = $('.attributes__form').clone()
attributes_form.removeAttr('hidden')
$('.attributes__form').remove()

const variations_form = $('#variations-form').clone()
variations_form.removeAttr('hidden')
$('#variations-form').remove()


if ($('#attributes-list').length > 0) {
    $("#attributes-list option").each(function(index) {
        const form = attributes_form.clone()
        const form_p = form.children("p")
        const form_value = form.children("#product-attribute-value")
        const form_priority = form.children("#product-attribute-priority")
        form.attr("id", form.attr("id") + $(this).attr("id"))
        form_p.text($(this).text())
        form_value.val($(this).val())
        form_value.attr("name", form_value.attr("name") + $(this).attr("id"))
        form_value.attr("id", form_value.attr("id") + $(this).attr("id"))
        form_priority.attr("name", form_priority.attr("name") + $(this).attr("id"))
        form_priority.attr("id", form_priority.attr("id") + $(this).attr("id"))
        form.appendTo(".attributes__list")
        prev_attributes.add(form.attr("id"))
    })
    $("#attributes-list").remove()

    $("#variations-list option").each(function(index) {
        const form = variations_form.clone()
        const form_p = form.children("p")
        const form_value = form.children("#product-variation-value")
        const form_additional_value = form.children("#product-variation-additional_value")
        form.attr("id", form.attr("id") + $(this).attr("id"))
        form.attr("variation", $(this).attr("variation"))
        form_p.text($(this).text())
        form_value.val($(this).val())
        form_value.attr("name", form_value.attr("name") + $(this).attr("variation") + '-old-' + $(this).attr("id"))
        form_value.attr("id", form_value.attr("id") + $(this).attr("variation") + '-old-' + $(this).attr("id"))
        form_additional_value.val($(this).attr("additional_value"))
        form_additional_value.attr("name", form_additional_value.attr("name") + $(this).attr("variation") + '-old-' + $(this).attr("id"))
        form_additional_value.attr("id", form_additional_value.attr("id") + $(this).attr("variation") + '-old-' + $(this).attr("id"))
        form.appendTo(".variations__list")
    })
    $("#variations-list").remove()
}

$('#product-attributes').on('mousedown', 'option', function(e) {
    e.preventDefault();
    $(this).attr('selected', !$(this).attr('selected'));
    const form = attributes_form.clone()
    const form_p = form.children("p")
    const form_value = form.children("#product-attribute-value")
    const form_priority = form.children("#product-attribute-priority")
    form.attr("id", form.attr("id") + $(this).val())
    form_p.text($(this).text())
    form_value.attr("name", form_value.attr("name") + $(this).val())
    form_value.attr("id", form_value.attr("id") + $(this).val())
    form_priority.attr("name", form_priority.attr("name") + $(this).val())
    form_priority.attr("id", form_priority.attr("id") + $(this).val())
    if($(this).attr('selected')) {
        if (attributes_to_del.has(form.attr('id'))) {
            attributes_to_del.delete(form.attr('id'))
            $("#" + form.attr("id")).removeClass('del-attribute')
        } else {
            form.appendTo($(".attributes__list"));
        }
    } else {
        if (prev_attributes.has(form.attr('id'))) {
            $("#" + form.attr('id')).toggleClass('del-attribute')
            attributes_to_del.add(form.attr('id'))
        } else {
            $("#" + form.attr('id')).remove()
        }
        if($('#category-check').is(':checked') && $(this).attr('category') !== $("#product-category").val()) {
            $(this).attr('hidden', true)
        }
    }
});

variations_iterator = 0

$('#product-variations').on('mousedown', 'option', function(e) {
    e.preventDefault();
    $(this).attr('selected', true);
    const form = variations_form.clone()
    const form_p = form.children("p")
    const form_value = form.children("#product-variation-value")
    const form_additional_value = form.children("#product-variation-additional_value")
    form.attr("id", form.attr("id") + ++variations_iterator)
    form.attr("variation", $(this).val())
    form_p.text($(this).text())
    form_value.attr("name", form_value.attr("name") + $(this).val() + "-new-" + variations_iterator)
    form_value.attr("id", form_value.attr("id") + $(this).val() + "-new-" + variations_iterator)
    form_additional_value.attr("name", form_additional_value.attr("name") + $(this).val() + "-new-" + variations_iterator)
    form_additional_value.attr("id", form_additional_value.attr("id") + $(this).val() + "-new-" + variations_iterator)
    form.appendTo($(".variations__list"));
});

$(document).on('click', '.del-variation', function(e) {
    const form = $(this).parent()
    const variation_list = form.parent()
    const variation_id = form.children("input[required]").attr("id").split('-old-')[1]
    console.log(variation_id);
    if (variation_id) {
        form.children("input").val('del')
        form.attr("hidden", true)
    } else {
        form.remove()
    }
    if(variation_list.children(".variations__form[variation='" + form.attr("variation") + "']:not([hidden])").length === 0) {
        $("#product-variations option[value='" + form.attr("variation") + "']").removeAttr('selected');
    }
})

function hide_attributes(select, category) {
    select.find('option[category="' + category + '"]').removeAttr("hidden")
    select.find('option:not([category="' + category + '"]):not([selected])').attr('hidden', true)
}

$('#category-check').change(function() {
    if ($(this).is(':checked')) {
        hide_attributes($('#product-attributes'), $("#product-category").val())
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
    priority_i = 0
    $('.priority').each(function() {
        ++priority_i
        $(this).val(priority_i)
    })
    
    let formData = new FormData(this);

    for (attribute of attributes_to_del) {
        formData.append(attribute, 'del');
    }
    

    console.log(formData);
    
    $.ajax({
        type: $(this).attr('method'),
        url: window.location.pathname,
        headers: {
            'X-CSRFToken': csrftoken,
        },
        data: formData,
        contentType: false,
        processData: false,
        success: function(response) {
            console.log(response);
            window.location.href = baseURL + '/product/' + response.id;
        },
        error: function(response) {
            console.error(response);
        }
    });
});

$( function() {
    $( ".attributes__list" ).sortable({
        revert: false
    });
} );