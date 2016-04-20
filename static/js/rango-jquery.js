
$(document).ready( function() {

    $("#about-btn").addClass('btn btn-primary').click( function(event) {
        alert("You clicked the button using JQuery!");
        addClass('btn btn-primary')
    });

    $("p").hover( function() {
            $('p').css('color', 'red');
    },
    function() {
            $('p').css('color', 'blue');
    });

    $('.rango-add').click(function(){
    var catid = $(this).attr("data-catid");
        var url = $(this).attr("data-url");
        var title = $(this).attr("data-title");
        var me = $(this);
        $.get('/rango/auto_add_page/', {category_id: catid, url: url, title: title}, function(data){
                        $('#pages').html(data);
                        me.hide();
                        });
                                });



});

