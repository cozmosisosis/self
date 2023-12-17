console.log("ajax testing js file")


$(document).ready(function() {
    $.ajax({
        url: $SCRIPT_ROOT + '/ajax_test_submit',
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
    console.log(id)
    console.log(value)
    $.ajax({
        url: $SCRIPT_ROOT + '/ajax_test_submit',
        dataType: 'json',
        type: 'POST',
        data: {
            id: id,
            value: value
        },
        success: function (response) {
            $('#index_table').replaceWith(response)
            console.log('success')
        },
        error: function () {
            console.log('error')
        }
    })

}