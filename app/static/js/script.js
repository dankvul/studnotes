function exec_add_deadline() {
    document.getElementById('deadline_input_form').style.visibility = "visible";
}
function close_add_deadline() {
    document.getElementById('deadline_input_form').style.visibility = "hidden";
}

function send_queue() {
    if (!$("#queue-id-name").val()) {
        $("#queue_errors").html("Value required");
        return;
    }

    $.post('/queues/add', {
        name: $("#queue-id-name").val()
    }).done(function (response) {
        $('#all_queues').append(
            "                   <button type=\"button\" onclick=\"window.location.href = '/queues/"+response['id']+"'; \" class=\"list-group-item list-group-item-action d-flex justify-content-between align-items-center\">\n" +
            "                        "+ response['name'] +
            "                        <span class=\"badge badge-primary badge-pill\"> "+ response['size'] + "</span>\n" +
            "                   </button>");
        close_add_deadline();
    }).fail(function() {
        $('#queue_errors').html('ERROR adding queue')
    });


}

function enter_to_queue(user_id, queue_id) {
    $.post('/queues/enter',{
        user_id: user_id,
        queue_id: queue_id
    }).done(function (response) {
        alert(response['message']);
    }).fail(function () {
        alert('Error adding you to this queue')
    });
    location.reload();
}

function delete_deadline(id){
    window.location.href = '/deadlines/delete/' + id;
}

function send() {
    if (!$("#id-body").val()) {
        $("#deadline_errors").html("Value required");
        return;
    }

    $.post('/deadline_add', {
        body: $("#id-body").val(),
        date: $("#id-date").val(),
        state: $("#id-select").val()
    }).done(function (response) {
        if (response['error']) {
            $('#deadline_errors').html(response['error']);
        } else {
            $('#all_deadlines').append(
                "                        <div class=\"col-sm-3 deadline\">\n" +
                "                            <h4>" + response['body'] + "</h4>\n" +
                "                            <h5 style='color:red;'>Days to go: " + response['exp_date'] + "</h5>\n" +
                "                            <button class=\"btn btn-primary\" onclick=\'delete_deadline(" + response['id'] + ")\'>DELETE</button>\n" +
                "                        </div>");
            close_add_deadline();
        }
    }).fail(function() {
        $('#deadline_errors').html('ERROR adding deadline')
    });


}


