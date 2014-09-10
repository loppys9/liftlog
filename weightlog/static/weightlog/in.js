function fancy_text()
{
    //set the focus
    var intext = $('input[type=text]');
    intext.each( function(item, elem ) {
        $(elem).before( '<span class="ll textcolor" id=l' + $(elem).attr('name') + '></span>' );
        $(elem).after( '<span class="ll textcolor" id=r' + $(elem).attr('name') + '></span>' );
    });

    intext.focus( function() {
        var n = $(this).attr('name');
        $( '#l' + n).removeClass('textcolor');
        $( '#r' + n).removeClass('textcolor');
        $( '#l' + n).addClass('textfocuscolor');
        $( '#r' + n).addClass('textfocuscolor');
    });

    intext.focusout( function() {
        var n = $(this).attr('name');
        $( '#l' + n).removeClass('textfocuscolor');
        $( '#r' + n).removeClass('textfocuscolor');
        $( '#l' + n).addClass('textcolor');
        $( '#r' + n).addClass('textcolor');
    });

}

function set_date() {
    var date = new Date().toISOString().substring(0,10);
    $('#wo_date').val(date);
}

function add_workout_success(data, textStatus, jqXHR) {
    alert("worked");
}

function add_workout_error(jqXHR, textStatus, errorThrown) {
    alert("failed " + textStatus + " " + errorThrown);
}

function add_workout() {
    var data = JSON.stringify(
            {"name": $('#wo_name').val(),
            "date": $('#wo_date').val(),
            "descr": $('#wo_descr').val()});

    $.ajax({type: 'POST',
    url: 'http://127.0.0.1:8000/api/v1/workout/',
    data: data,
    success: add_workout_success,
    error: add_workout_error,
    processData: false,
    dataType: 'text',
    contentType: 'application/json'
    });
}

