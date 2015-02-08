//The id of the workout
var workout_id = "-1";
var eind = 1;
var exind = 0;
var cur_table = 0;

/*Javascript sucks. heres a lift entry object*/
function LiftEntry (eid, wid, rid, sid)
{
    this.eid = '#' + eid;
    this.wid = '#' + wid;
    this.rid = '#' + rid;
    this.sid = '#' + sid;
    this.complete = false;
}

LiftEntry.prototype.check_complete = function () {
    empty = '';
    console.log("things " + $(this.eid).val() + " " + $(this.wid).val() + " " + $(this.rid).val()+ " " + $(this.sid).val());
    if ($(this.eid).val() != empty &&
        $(this.wid).val() != empty &&
        $(this.rid).val() != empty &&
        $(this.sid).val() != empty) {
            this.complete = true;
            return true;
    } else {
        this.complete = false;
        return false;
    }
    console.log("complete? " + this.complete);
};

var liftEntries = [];

/* Here is the end of the lift entry object */

/*function fancy_text()
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

}*/

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
    console.log("the data " + data + " |");
    le = JSON.parse(data).id;
}

function add_lift_error(jqXHR, textStatus, errorThrown) {
}

/* Takes a LiftEntry object */
function add_lift_entry(entry) {
    console.log(entry.complete);
    console.log($(entry.wid).val());
    console.log($(entry.rid).val());
    console.log($(entry.sid).val());
    console.log($(entry.eid).val());

    var e_url = 'http://127.0.0.1:8000/api/v1/excercise/';
    var w_url = 'http://127.0.0.1:8000/api/v1/workout/';
    
    console.log('ale workout_id: ' + workout_id);

    var data = JSON.stringify(
            {
                "weight": $(entry.wid).val(),
        /*TODO add a units thing */
                "units": $('lbs').val(),
                "sets": $(entry.sid).val(),
                "reps": $(entry.rid).val(),
                "workout": w_url + workout_id + '/',
                "excercise": e_url + $(entry.eid).val() + '/',
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

    for (var i = 0; i < liftEntries.length; i++) {
        for (var j = 0; j < liftEntries[i].length; j++) {
            if (liftEntries[i][j].check_complete()) {
                add_lift_entry(liftEntries[i][j]);
            }
        }
    }
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

}

function append_excercise() {
    exind = liftEntries.length;

    var etable = "<table id='exc" + exind + "'>" +
  "<thead><tr><th></th><th>Weight</th><th>Reps</th><th>Sets</th></tr></thead>" +
  "<tbody id='e0'>" +
    "<tr id='e" + exind + "ent0'>" +
      "<td><input type='text' name='excer' placeholder='Excercise' id='excer" + exind + "' class='excer ui-autocomplete-input' autocomplete='off' onfocus='set_table_loc(" + exind + ",0)'" + 
        "<input type='hidden' id='e" + exind + "'></td>" + 
      "<td><input type='number' id='e" + exind + "w0' onfocus='set_table_loc(" + exind + ")'></td>" +
      "<td><input type='number' id='e" + exind + "r0' onfocus='set_table_loc(" + exind + ")'></td>" +
      "<td><input type='number' id='e" + exind + "s0' onfocus='set_table_loc(" + exind + ")'></td>" +
    "</tr>" + 
    "<tr id='e" + exind + "ent1'>" +
      "<td></td>" +
      "<td><input type='number' id='e" + exind + "w1' onfocus='set_table_loc(" + exind + ")'></td>" +
      "<td><input type='number' id='e" + exind + "r1' onfocus='set_table_loc(" + exind + ")'></td>" +
      "<td><input type='number' id='e" + exind + "s1' onfocus='set_table_loc(" + exind + ")'></td>" +
    "</tr>" +
  "</tbody>" +
"</table> ";
    console.log(etable);
    $("#lifts").append(etable);
}

//function append_lift_entry(table_id) {
function append_lift_entry() {
    exind = liftEntries[cur_table].length;

    var erow = "<tr id='e" + cur_table + "ent" + exind + "'>" +
      "<td></td>" +
      "<td><input type='number' id='e" + cur_table + "w" + exind + "' onfocus='set_table_loc(" + exind + ")'></td>" +
      "<td><input type='number' id='e" + cur_table + "r" + exind + "' onfocus='set_table_loc(" + exind + ")'></td>" +
      "<td><input type='number' id='e" + cur_table + "s" + exind + "' onfocus='set_table_loc(" + exind + ")'></td>" +
    "</tr>";
    console.log(erow);
    $("#e" + cur_table).append(erow);
}

function set_table_loc(table_id) {
    cur_table = table_id;
    //liftEntries[table_id][row_id].check_complete();
    console.log("current table: " + cur_table);
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

function set_arrow_keys() {
    $('input').keyup(function(e){
        console.log(e.keyCode);
    });
}

function init_workouts() {
    liftEntries[0] = []
    liftEntries[0].push(new LiftEntry('e0', 'e0w0', 'e0r0', 'e0s0'));
    liftEntries[0].push(new LiftEntry('e0', 'e0w1', 'e0r1', 'e0s1'));
    console.log('hola folks: %d', liftEntries.length);
    console.log('and: %d', liftEntries[0].length);
}

