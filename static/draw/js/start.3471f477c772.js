$(document).ready(function () {
    window.addEventListener("wheel", function(e){
        e.preventDefault();
    },{passive : false});

    var $html = $("html");
    var page = 1;
    var lastPage = $(".content").length;
    $html.animate({scrollTop:0},10);

    $(window).on("wheel", function(e){
 
        if($html.is(":animated")) return;
     
        if(e.originalEvent.deltaY > 0){
            if(page== lastPage) return;
     
            page++;
        }else if(e.originalEvent.deltaY < 0){
            if(page == 1) return;
     
            page--;
        }
        var posTop = (page-1) * $(window).height();
     
        $html.animate({scrollTop : posTop});
     
    });

    $('.first-btn, .second-btn, .third-btn').click(function () {
        var $clicked = $(event.target);
        if ($clicked.is('.first-btn')) {
            page = 1;
            var posTop = (page-1) * $(window).height();
            $html.animate({scrollTop : posTop});
        } else if($clicked.is('.second-btn')) {
            page = 2;
            var posTop = (page-1) * $(window).height();
            $html.animate({scrollTop : posTop});
        } else if($clicked.is('.third-btn')) {
            page = 3;
            var posTop = (page-1) * $(window).height();
            $html.animate({scrollTop : posTop});
        }
    });

});