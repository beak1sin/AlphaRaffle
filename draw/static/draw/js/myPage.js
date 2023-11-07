$(document).ready(function() {

    $('.comment-delete-btn').click(function () {
        $(".backL").css("display", "");
        let pk = $(this).parent().parent().attr('data-value');
        let comment = $(this).parent().parent().children(':nth-child(2)').children(':nth-child(1)').text();
        let created_date = $(this).parent().parent().children(':nth-child(2)').children(':nth-child(2)').text();
        let shoename = $(this).parent().parent().children(':nth-child(2)').children(':nth-child(3)').text();
        const data = {'pk': pk,'comment': comment, 'created_date': created_date, 'shoename': shoename};

        fetch('comment_delete_mypage', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            $(this).parent().parent().css({'text-align': 'center'});
            $(this).parent().parent().html(data.message);
            $(".backL").css("display", "none");
        })
        .catch(error => {
            console.log('Error: ' + error);
        });
    });

    // header 스크롤 구현
    var didScroll;
    var lastScrollTop = 0;
    var delta = 5; // 동작의 구현이 시작되는 위치
    var navbarHeight = $('header').outerHeight(); // 영향을 받을 요소를 선택

    // 스크롤시에 사용자가 스크롤했다는 것을 알림
    $(window).scroll(function(event){
        didScroll = true;
    });

    // hasScrolled()를 실행하고 didScroll 상태를 재설정
    setInterval(function() {
        if (didScroll) {
            hasScrolled();
            didScroll = false;
        }
    }, 250);

    // 동작을 구현
    function hasScrolled() {
        // 접근하기 쉽게 현재 스크롤의 위치를 저장한다.
        var st = $(this).scrollTop();
        
        // 설정한 delta 값보다 더 스크롤되었는지를 확인한다.
        if(Math.abs(lastScrollTop - st) <= delta){
            return;
        }
        
        // 헤더의 높이보다 더 스크롤되었는지 확인하고 스크롤의 방향이 위인지 아래인지를 확인한다.
        if (st > lastScrollTop && st > navbarHeight){
            // Scroll Down
            $('header').removeClass('nav-down').addClass('nav-up');
            $('#mypage').removeClass('nav-up').addClass('nav-down');
            $('#mypage_nav').removeClass('nav-up').addClass('nav-down');
        } else {
            // Scroll Up
            if(st + $(window).height() < $(document).height()) {
            $('header').removeClass('nav-up').addClass('nav-down');
            $('#mypage').removeClass('nav-down').addClass('nav-up');
            $('#mypage_nav').removeClass('nav-down').addClass('nav-up');
                
            }
        }
        
        // lastScrollTop 에 현재 스크롤위치를 지정한다.
        lastScrollTop = st;
    }

    $('.checkbox-circle-btn').click(function() {
        if ($(this).hasClass('checked')) {
            $(this).removeClass('checked');
        } else {   
            $(this).addClass('checked');
        }
    });
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

var xhr;
