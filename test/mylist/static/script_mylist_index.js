console.log("Homepage js file loaded ver")

$(document).ready(function() {
    $.ajax({
        url: $SCRIPT_ROOT + '/active_list',
        dataType: 'json',
        type: 'GET',
        success: function (response) {
            $('#index_table').replaceWith(response);
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
        url: $SCRIPT_ROOT + '/active_list',
        dataType: 'json',
        type: 'POST',
        data: {
            id: id,
            value: value
        },
        success: function (response) {
            $('#index_table').replaceWith(response)
        },
        error: function () {
            console.log('error')
        }
    })
}