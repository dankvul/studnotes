function exec_add_deadline() {
    document.getElementById('deadline_input_form').style.visibility = "visible";
}
function close_add_deadline() {
    document.getElementById('deadline_input_form').style.visibility = "hidden";
}


function format_date(x) {
    var date = x[8] + x[9] + '.' + x[5] + x[6] + '.' + x[0] + x[1] + x[2] + x[3];
    return date;
}

function redirect_to_queue(id){
    alert('123');
    window.location.replace("/id");
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
            "                   <li class=\"list-group-item d-flex justify-content-between align-items-center\">\n" +
            "                        "+ response['name'] +
            "                        <span class=\"badge badge-primary badge-pill\"> "+ response['size'] + "</span>\n" +
            "                   </li>");
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
        $('#all_deadlines').append(
            "                        <div class=\"col-sm-3 deadline\">\n" +
            "                            <h4>Name of deadline: " + response['body'] + "</h4>\n" +
            "                            <h5 style='color:red;'>Expire Date: " + response['exp_date'] + "</h5>\n" +
            "                        </div>");
        close_add_deadline();
    }).fail(function() {
        $('#deadline_errors').html('ERROR adding deadline')
    });


}


