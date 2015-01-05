//The id of the workout
var workout_id = "-1";
var eind = 0;

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
    //var w_id = JSON.parse(data).id;
    workout_id = JSON.parse(data).id;
    console.log('workout_id: ' + workout_id);
}

function add_workout_error(jqXHR, textStatus, errorThrown) {
    alert("failed " + textStatus + " " + errorThrown);
}

function add_lift_success(data, textStatus, jqXHR) {
    //var w_id = JSON.parse(data).id;
    le = JSON.parse(data).id;
    alert("ls worked\n" + data + "\n" + le_id );
}

function add_lift_error(jqXHR, textStatus, errorThrown) {
    alert("failed " + textStatus + " " + errorThrown);
}

function add_lift_entry() {
    var e_url = 'http://127.0.0.1:8000/api/v1/excercise/';
    var w_url = 'http://127.0.0.1:8000/api/v1/workout/';
    
    console.log('ale workout_id: ' + workout_id);

    var data = JSON.stringify(
            {
                "weight": $('#w0').val(),
                "units": $('#u0').val(),
                "sets": $('#s0').val(),
                "reps": $('#r0').val(),
                "workout": w_url + workout_id + '/',
                "excercise": e_url + $('#e0').val() + '/',
            });

    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:8000/api/v1/liftentry/',
        data: data,
        success: add_lift_success,
        error: add_lift_error,
        processData: false,
        dataType: 'text',
        contentType: 'application/json'
    });
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
        contentType: 'application/json',
        async: false
    });
}

function add_autocomplete(id) {
    ac_source = "http://127.0.0.1:8000/api/v1/excercisesearch/"

    id_num = id.substring(id.length-1, id.length);
    $("#" + id).autocomplete({
        source: function( request, response ) { 
            var d = JSON.stringify({"term": request.term});
        $.ajax({
          url: ac_source,
          dataType: "json",
          data: {
              term: request.term
          },
          success: function( data ) {
              var d = JSON.parse(data);
              response($.map(d, function(obj) {
                  console.log(obj);
                  console.log(obj.name);
                  console.log(obj.id);
                  return {
                      label: obj.name,
                      value: obj.name,
                      id: obj.id
                  };
              }));
          },
            error: function(jqXHR, textStatus, errorThrown){
                alert(jqXHR);                        
            },
        });
      },
        minLength: 2,
        select: function(event, ui) {
            console.log("#e" + id_num);
            $('#e'+ id_num).val(ui.item.id);
        }
    });

    /*$(".excer").autocomplete({
        source: function( request, response ) { 
            var d = JSON.stringify({"term": request.term});
        $.ajax({
          url: ac_source,
          dataType: "json",
          data: {
              term: request.term
          },
          success: function( data ) {
              var d = JSON.parse(data);
              response($.map(d, function(obj) {
                  console.log(obj);
                  console.log(obj.name);
                  console.log(obj.id);
                  return {
                      label: obj.name,
                      value: obj.name,
                      id: obj.id
                  };
              }));
          },
            error: function(jqXHR, textStatus, errorThrown){
                alert(jqXHR);                        
            },
        });
      },
        minLength: 2,
        select: function(event, ui) {
            console.log(ui);
            console.log(event);
            $('#e0').val(ui.item.id);
        }
    });*/
}

function new_lift() {
    var entry = "#entry" + eind;
    var clone = $(entry).clone();

    eind++;
    clone.attr("id", "entry" + eind);
    clone.find("*").each(function() { // For each new item with an ID
        if (this.id) {
            this.id = this.id.substring(0, this.id.length - 1) + eind;
        }
    });
    clone.find("input").val("");
    clone.find("textarea").val("");
    clone.insertAfter(entry);
    add_autocomplete("excer" + eind);
}

