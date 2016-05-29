//The id of the workout
var workout_id = "-1";
var eind = 1;
var exind = 0;
var pre_entry = null;
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


function set_date() {
    var date = new Date().toISOString().substring(0,10);
    $('#wo_date').val(date);
}

function add_workout_success(data, textStatus, jqXHR) {
    workout_id = JSON.parse(data).id;
    add_lift_entries();
}

function add_workout_error(jqXHR, textStatus, errorThrown) {
    alert("failed " + textStatus + " " + errorThrown);
}

function add_lift_success(data, textStatus, jqXHR) {
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

    $.ajax({type: 'POST',
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
    var ac_source = "http://127.0.0.1:8000/api/v1/excercisesearch/"

    var id_num = id.substring(id.length-1, id.length);
    var cur_data;

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
              cur_data = $.map(d, function(obj) {
                  return {
                      label: obj.name,
                      value: obj.name,
                      id: obj.id
                  };
              });
              response(cur_data);
          },
            error: function(jqXHR, textStatus, errorThrown){
                alert(jqXHR);                        
            },
        });
      },
        minLength: 2,
        select: function(event, ui) {
            $('#e'+ id_num).val(ui.item.id);
        },
        change: function(event, ui) {
            if (ui.item) {
                return;
            }
            var value = this.value;
            console.log(value);
            console.log(cur_data.length);
            for (var i=0; i<cur_data.length; i++) {
                if (value === cur_data[i].value) {
                    $('#e'+ id_num).val(cur_data[i].id);
                }
            }
        },
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
    table.focusin(function() {
        update_tables(this);
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
    if (pre_entry == null) {
        pre_entry = new_entry;
        return;
    }
    if (new_entry == pre_entry) {
        return;
    }

    var entry = pre_entry;
    pre_entry = new_entry;
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

function hide_extra_entries(table) {
    var entries = jQuery.data(table, "entries");
    var len = entries.length;
    if (!entries[len-1].complete && !entries[len-2].complete) {
        var rows = $(table).find('> tbody > tr');
        $(rows[len-1]).fadeTo(100,0);
    }
}

function show_extra_entries(table) {
        var row = $(table).find('> tbody > tr').last();
        row.fadeTo(100,1);
}

function update_tables(new_table) {
    if (pre_table == null) {
        pre_table = new_table;
        return;
    }

    if (new_table == pre_table) {
        return;
    }
    hide_extra_entries(pre_table);
    show_extra_entries(new_table);
    pre_table = new_table;
}

