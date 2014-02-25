var GLOBAL_LOCK = false;

function gc(){
    var s = $('#subject').val();

    $.ajax({
        type: 'POST',
        url: 'tools/gc',
        data: {'s': s},
        success: function(data){
            $('#categories').html(data);
        }
    });
}

function get_order_details(order_id){
    if (GLOBAL_LOCK)
        return;

    var tr = $('#o' + order_id);
    var h = tr.html();

    var div = $('#ho' + order_id);

    if (div.length > 0)
        div.html(h);
    else{
        div = document.createElement('div');
        $(div).addClass('hide').attr('id', 'ho' + order_id).html(h).appendTo($('body'));
    }

    tr.html('<td colspan="6"><img src="/static/ajax-loader.gif"  alt="loading..." /></td>');
    GLOBAL_LOCK = true;

    $.ajax({
        type: 'POST',
        url: 'tools/god',
        data: {'id': order_id},
        success: function(data){
            $('#o' + order_id).html('<td colspan="6">' + data + '</td>');
            GLOBAL_LOCK = false;
        }
    });
}

function hide_order_details(order_id){
    $('#o' + order_id).html($('#ho' + order_id).html());
}

function delete_order(order_id){
    if (!confirm('Are you sure?'))
        return;

    $.ajax({
        type: 'POST',
        url: 'tools/do',
        data: {'id': order_id},
        success: function(data){
            $('#o' + order_id).remove();
        }
    });
}


function set_handlers(){
    $('.rating-w-fonts li').click(function(){
        var star_n = parseInt(this.id[2]);
        var parentId = this.parentNode.id;

        $('#m_' + parentId).val(star_n);


        var i = 0;
        for(; i<=star_n; ++i){
            $('#' + parentId[0] + 'r' + i).attr('class','rated');
        }

        for(;i<=5;++i){
            $('#' + parentId[0] + 'r' + i).attr('class','');
        }
    });
}

function show_feedback_form(order_id){
    order_id = parseInt(order_id);

    $.ajax({
        type: 'POST',
        url: 'tools/lff',
        data: {'order_id': order_id},
        success: function(data){
            $('#ff').css('display', 'none');
            $('#ff').html(data).slideDown('slow');
            set_handlers();
        }
    });
}