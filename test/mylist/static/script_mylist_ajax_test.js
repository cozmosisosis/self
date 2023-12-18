console.log("ajax testing js file jjjj")


$(document).ready(function () {
    $.ajax({
        url: $SCRIPT_ROOT + '/my_items_new_ajax',
        dataType: 'json',
        type: 'GET',
        success: function (response) {
            $('#my_items_table').replaceWith(response);
            form_submit();

        },
        error: function (response) {
            alert('Server side error with input');
            location.reload();
        }
    })
})




function form_submit() {

    $("form").each(function () {
        $(this).bind("submit", function (event) {
            event.preventDefault();
            console.log(event.target); // object formHTML
            console.log("form id: " + event.target.id);
            console.log("form action: " + $(this).attr("action"));
            console.log("form method: " + event.target.method);
            const data = new FormData(event.target);
            console.log([...data.entries()]);


            
            if ((!($(this).attr("action") === '/my_items_new_ajax')) || (!(['new_item', 'change_item_name', 'remove_item'].includes(data.get('action'))))) {
                console.log('invalid action type');
                return;
            }


            if (data.get('action') === 'new_item') {
                if(data.get('item_name') === '') {
                    console.log('ajax message')
                    $('#ajax_message_add_item').replaceWith('<div id="ajax_message_add_item"> Must fill out Name</div>');
                }
            }
            if (data.get('action') === 'change_item_name') {
                console.log('found match change_item_name')
                
            }
            if (data.get('action') === 'remove_item') {
                console.log('found match remove_item')
            }


            
        })
    })
}


// $.ajax({
//     url: $SCRIPT_ROOT + '/my_items_new_ajax',
//     dataType: 'json',
//     type: 'POST',
//     data: {
//         id: id,
//         value: value
//     },
//     success: function (response) {
//         $('#my_items_table').replaceWith(response)
//         console.log('success')
//     },
//     error: function () {
//         console.log('error')
//     }
// })
