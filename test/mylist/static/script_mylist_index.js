console.log("Homepage js file loaded ver")

$(document).ready(function() {
    $.ajax({
        url: $SCRIPT_ROOT + '/active_list_data',
        dataType: 'json',
        type: 'GET',
        success: function (response) {
            $('#index_data').replaceWith(response);
        },
        error: function (response) {
            alert('Server side error with input');
            location.reload();
        }
    })
})



function change_quantity(id) {
    value = $('#' + id).val()
    if (value === '') {
        console.log('empty textbox')
        return;
    }
    $.ajax({
        url: $SCRIPT_ROOT + '/active_list_quantity',
        dataType: 'json',
        type: 'POST',
        data: {
            id: id,
            value: value
        },
        success: function (response) {
            $('#index_data').replaceWith(response)
        },
        error: function () {
            console.log('error')
        }
    })
}


$(document).on("submit", "form", function(e) {
    
    console.log('test')
    var form = $(this);
    var formId = form.attr("id");
    e.preventDefault();

    $.ajax({
        url: $SCRIPT_ROOT + '/' + formId,
        dataType: 'json',
        type: 'POST',
        data: form.serialize(),
        success: function(response) {
            $('#index_data').replaceWith(response);
        },
        error: function(response) {
            location.reload();
        }
    })
})