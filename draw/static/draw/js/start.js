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

    const shoe0 = STATIC_NECESSARY + "scott.png";
    const shoe1 = STATIC_NECESSARY + "chicago.png";
    const shoe2 = STATIC_NECESSARY + "scott2.png";
    const shoe3 = STATIC_NECESSARY + "dunkpanda.png";
    const shoe4 = STATIC_NECESSARY + "nb.png";
    const shoe5 = STATIC_NECESSARY + "superstar.png";


    // 신발 비
    function createSnow () {
        const el = document.createElement('div');
        el.classList.add('snow');
        el.style.position = 'absolute';
        el.style.marginLeft = Math.floor(Math.random() * window.innerWidth - 300) + 'px';
        el.style.marginTop = Math.floor(Math.random() * window.innerHeight - 300) + 'px';
        const elImg = document.createElement('img');
        elImg.src = eval('shoe' + Math.floor(Math.random() * 6));
        el.appendChild(elImg);
        $('.content.snowSection').prepend(el);
    }
    function createShoe () {
        const el = document.createElement('div');
        el.classList.add('shoe');
        el.style.position = 'absolute';
        el.style.marginLeft = Math.floor(Math.random() * window.innerWidth - 300) + 'px';
        el.style.marginTop = Math.floor(Math.random() * window.innerHeight - 300) + 'px';
        const elImg = document.createElement('img');
        elImg.src = eval('shoe' + Math.floor(Math.random() * 6));
        el.appendChild(elImg);
        $('.content.snowSection').prepend(el);
    }
    for (let i = 0; i < 20; i++) {
        if (i % 2 == 0) {
            createSnow();
        } else {
            createShoe();
        }
        
    }
});