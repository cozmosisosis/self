console.log("ajax testing js file")


$(document).ready(function () {
    $.ajax({
        url: $SCRIPT_ROOT + '/my_items_data',
        dataType: 'json',
        type: 'GET',
        success: function (response) {
            $('#my_items_table').replaceWith(response);

        },
        error: function (response) {
            alert('Server side error with input');
            location.reload();
        }
    })
})

$(document).on("submit", "form", function(e) {
    
    var form = $(this);
    var formId = form.attr("id");
    e.preventDefault();

    $.ajax({
        url: $SCRIPT_ROOT + '/' + formId,
        dataType: 'json',
        type: 'POST',
        data: form.serialize(),
        success: function(response) {
            $('#my_items_table').replaceWith(response);
        },
        error: function(response) {
            location.reload();
        }
    })
})
