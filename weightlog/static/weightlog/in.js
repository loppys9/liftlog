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
    var date = new Date()
    var y = date.getFullYear();
    var m = date.getMonth();
    var d = date.getDay();
    if( d<10) {
        d = '0' + d;
    }
    if( m<10 ) {
        m = '0' + m;
    }
    date = y+'-'+m+'-'+d;
    $('#date').val(date);
}

