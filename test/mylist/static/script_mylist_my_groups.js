console.log('My groups ajax')


$(document).ready(function() {
    $.ajax({
        url: $SCRIPT_ROOT + '/my_groups_data',
        dataType: 'json',
        type: 'GET',
        success: function(response) {
            $('#my_groups_data').replaceWith(response);
        },
        error: function(response) {
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
            $('#my_groups_data').replaceWith(response);
        },
        error: function(response) {
            location.reload();
        }
    })
})
