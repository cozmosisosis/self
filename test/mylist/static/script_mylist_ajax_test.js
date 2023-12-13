console.log("ajax testing js file")

function testing(id) {
    value = $("#" + id).val()
    if (value === "") {
        console.log("nothing there")
        return;
    }
    console.log(id)
    console.log(value)
    console.log("key up")



    $.getJSON($SCRIPT_ROOT + '/ajax_test_submit', {
        id: id,
        value: value
    },
        function (data) {
            // parsed_data = JSON.parse(data)
            if ("error" in data){
                console.log(data)
                location.reload(true);
            }
            console.log(data)
        });
    return false;
}
