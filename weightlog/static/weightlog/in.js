//The id of the workout
var workout_id = "-1";
var eind = 1;
var exind = 0;
var pre_table = null;
var num_excs = 1;

/*Javascript sucks. heres a lift entry object*/
function LiftEntry (eid, wid, rid, sid, nid)
{
    this.eid = '#' + eid;
    this.wid = '#' + wid;
    this.rid = '#' + rid;
    this.sid = '#' + sid;
    this.nid = '#' + nid;
    this.complete = false;
}

LiftEntry.prototype.check_complete = function () {
    empty = '';
    //console.log("things " + $(this.eid).val() + " " + $(this.wid).val() + " " + $(this.rid).val()+ " " + $(this.sid).val());
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

/* Here is the end of the lift entry object */

//var liftEntries = [];

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
    add_lift_entries();
    //console.log('workout_id: ' + workout_id);
}

function add_workout_error(jqXHR, textStatus, errorThrown) {
    alert("failed " + textStatus + " " + errorThrown);
}

function add_lift_success(data, textStatus, jqXHR) {
    //var w_id = JSON.parse(data).id;
    //console.log("the data " + data + " |");
    le = JSON.parse(data).id;
}

function add_lift_error(jqXHR, textStatus, errorThrown) {
}

/* Takes a LiftEntry object */
function add_lift_entry(entry) {
    /*console.log(entry.complete);
    console.log($(entry.wid).val());
    console.log($(entry.rid).val());
    console.log($(entry.sid).val());
    console.log($(entry.eid).val());*/

    var e_url = 'http://127.0.0.1:8000/api/v1/excercise/';
    var w_url = 'http://127.0.0.1:8000/api/v1/workout/';
    
    //console.log('ale workout_id: ' + workout_id);

    var data = JSON.stringify(
            {
                "weight": $(entry.wid).val(),
        /*TODO add a units thing */
                "units": $('lbs').val(),
                "sets": $(entry.sid).val(),
                "reps": $(entry.rid).val(),
                "workout": w_url + workout_id + '/',
                "excercise": e_url + $(entry.eid).val() + '/',
                "note": $(entry.nid).val(),
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

function add_lift_entries() {
    $('table').each( function() {
        entries = jQuery.data(this, "entries");
        for (var i = 0; i < entries.length; i++) {
            if (entries[i].check_complete()) {
                add_lift_entry(entries[i]);
            }
        }
    });
}

function add_workout() {
    if ($('#wo_name').val() == '') {
        return;
    }

    var data = JSON.stringify(
            {"name": $('#wo_name').val(),
            "date": $('#wo_date').val(),
            "descr": $('#wo_descr').val()});

    return $.ajax({type: 'POST',
        url: 'http://127.0.0.1:8000/api/v1/workout/',
        data: data,
        success: add_workout_success,
        error: add_workout_error,
        processData: false,
        dataType: 'text',
        contentType: 'application/json',
        //async: false
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
                  /*console.log(obj);
                  console.log(obj.name);
                  console.log(obj.id);*/
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
            //console.log("#e" + id_num + ' ' + ui.item.id);
            $('#e'+ id_num).val(ui.item.id);
        }
    });

}

function append_excercise() {
    var exind = num_excs;
    var etable = "<table id='exc" + exind + "'>" +
  "<thead><tr><th></th><th>Weight</th><th>Reps</th><th>Sets</th></tr></thead>" +
  "<tbody id='e0'>" +
  "</tbody>" +
"</table> ";

    //console.log(etable);
    $("#lifts").append(etable);
    num_excs++;
    var table = $('#exc' + exind);
    table.data("id", exind);
    table.data("entries", []);
    append_lift_entry(table);
    append_lift_entry(table);
    $("#excer" + exind).each( function() {
        add_autocomplete(this.id);
    });
}

function le_id(table_id, w_s_r, exind) {
    return 'e' + table_id + w_s_r + exind;
}

function append_lift_entry(table) {
    var data = table.data("entries");
    var exind = data.length;
    var cur_table = table.data("id");
    var efield = '';

    if (exind == 0) {
        efield =  "<input type='text' name='excer' placeholder='Excercise' id='excer" + cur_table + "' class='excer ui-autocomplete-input' autocomplete='off'>" + 
        "<input type='hidden' id='e" + cur_table + "'>";
    }

    var erow = "<tr id='e" + cur_table + "ent" + exind + "'>" +
      "<td>" + efield + "</td>" +
      "<td><input type='number' id='e" + cur_table + "w" + exind + "' ></td>" +
      "<td><input type='number' id='e" + cur_table + "r" + exind + "' ></td>" +
      "<td><input type='number' id='e" + cur_table + "s" + exind + "' ></td>" +
      "<td> <input type='textarea' id='e" + cur_table + "n" + exind + "' placeholder='Notes'> </td>" +
    "</tr>";
    //console.log(erow);
    var e = 'e0';
    table.append(erow);
    le = new LiftEntry('e' + cur_table, le_id(cur_table,'w',exind), le_id(cur_table,'r',exind),
            le_id(cur_table, 's', exind), le_id(cur_table, 'n', exind));
    data.push(le);
    var row_id = '#e' + cur_table + 'ent' + exind;
    $(row_id).data("entry", le);
    $(row_id).focusin(function() {
        update_entries(this);
    });
}

function add_new_excercise() {
    var add_new = true;
    $('table').each( function() {
        //console.log(this);
        //console.log(jQuery.data(this,"entries")[0]);
        if (!jQuery.data(this,"entries")[0].complete){
            add_new = false;
        }
    });
    if (add_new) {
        append_excercise();
    }
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
    var i = 0;
    le = [];
    le.push(new LiftEntry('e0', 'e0w0', 'e0r0', 'e0s0', 'e0n0'));
    le.push(new LiftEntry('e0', 'e0w1', 'e0r1', 'e0s1', 'e0n1'));
    $('#e0 tr').each( function() {
        jQuery.data(this, "entry", le[i]);
        i++;
    });
    table = $('#exc0');
    table.data("entries", le);
    table.data("id", 0);
}

function update_excs() {
    $('table').each( function() {
    });
}

function update_entries(new_entry) {
    //console.log(new_entry.id);
    if (pre_table == null) {
        pre_table = new_entry;
        return;
    }
    if (new_entry == pre_table) {
        return;
    }

    var entry = pre_table;
    pre_table = new_entry;
    var entry_obj = jQuery.data(entry,"entry");

    if (!entry_obj.complete && entry_obj.check_complete()) {
        //console.log("and we're here!\n");
        var table = $(entry).closest('table');
        var entries = table.data("entries");
        for (var i = 0; i < entries.length-1; i++) {
            if (!entries[i].complete) {
                return;
            }
        }
        append_lift_entry(table);
        add_new_excercise();
    }
}

