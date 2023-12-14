console.log('Edit groups js file loaded')


$(document).ready(function() {
    $.ajax({
        url: $SCRIPT_ROOT + '/change_quantity_in_group',
        dataType: 'json',
        success: function (response) {
            $('#groups_table').replaceWith(response);
        },
        error:  function (response) {
            alert('Server side error with input');
            location.reload();
        }
    })
})



function testing(id) {
    value = $("#" + id).val()
    if (value === "") {
        console.log('Current quantity value is empty')
        return;
    }
    $.ajax({
        url: $SCRIPT_ROOT + '/change_quantity_in_group',
        dataType: 'json',
        data: {
            id: id,
            value: value
        },
        success: function (response) {
            $('#groups_table').replaceWith(response);
        },
        error:  function (response) {
            alert('Server side error with input');
            location.reload();
        }
    });
    return false;
}