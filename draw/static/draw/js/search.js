$(document).ready(function () {

    $("#search_value").keyup( (e) => {
        let $search = $('#search_value');
        if ($search.val().length == 0) {
            $search.css({'border-bottom': '2px solid rgb(245, 245, 245)'});
        } else {
            $search.css({'border-bottom': '2px solid black'});
        }
    });

    $('#search_close_btn').click( () => {
        $('#search_value').html('');
        $('#search_value').css({'border-bottom': '2px solid rgb(245, 245, 245)'});
    });
    
});