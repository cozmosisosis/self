console.log('Edit groups js file loaded')


$(document).ready(function() {
    $.ajax({
        url: $SCRIPT_ROOT + '/change_quantity_in_group',
        dataType: 'json',
        type: 'GET',
        success: function (response) {
            $('#groups_table').replaceWith(response);
        },
        error:  function (response) {
            alert('Server side error with input');
            location.reload();
        }
    })
})



function update_quantity(id) {
    value = $("#" + id).val()
    if (value === "") {
        console.log('Current quantity value is empty')
        return;
    }
    $.ajax({
        url: $SCRIPT_ROOT + '/change_quantity_in_group',
        dataType: 'json',
        type: 'POST',
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
            $('#groups_table').replaceWith(response);
        },
        error: function(response) {
            location.reload();
        }
    })
})