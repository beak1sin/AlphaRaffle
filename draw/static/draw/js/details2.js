$(document).ready(function() {
    $('.reply-btn').on('click', function() {
        // if ($('.reply-btn').hasClass('disabled')) {
        //     $(this).addClass('active');
        //     $(this).removeClass('disabled');
        // } else {
        //     $(this).addClass('disabled');
        //     $(this).removeClass('active');
        // }
        // $(".reply").toggle();
        $(this).parent().parent().next().toggle();
        if ($(this).parent().hasClass('borderBottomNone')) {
            $(this).parent().removeClass('borderBottomNone');
        } else {
            $(this).parent().addClass('borderBottomNone');
        }
        // $(this).parent().parent().prev().children().next().next().style.borderBottom="15px dotted red";
    });

    // 태그 여러개 있을 경우 margin-left 추가
    var length = $('.product-info-name-tag-tagname').length;
    var marginWidth = 0;
    for (var i = 1; i <= length; i++) {
        var width = $('.product-info-name-tag-tagname.tagname'+i).width() + 10;
        marginWidth += width;
        var tagplus = i+1;
        $('.product-info-name-tag-tagname.tagname'+tagplus).css("margin-left", marginWidth + "px");
        if(i+1==length) {break;}
    }

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

    // 댓글 기능
    $(document).on("click", "#comment_btn", function() {
        var commentValue = document.getElementById("commentArea").value;
        if (commentValue == "") {
            $('#comment_error_msg').show();
            return false;
        }
        var serialno = $('#serialno').text();
        var data = {commentValueAJAX: commentValue, serialnoAJAX: serialno};
        var datastr = JSON.stringify(data);
        
        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4) {
                var data = xhr.responseText;
                var obj = JSON.parse(data);
                if (obj.flag == "0") {
                    alert(obj.result_msg);
                } else {
                    // 현재경로 + 공백추가 필수!!
                    $('.u-section-3').load(location.href + " .u-section-3", function() {
                        commentLength = $('.comment_div').length;
                        $('#commentLength').text(`COMMENT: ${commentLength}개`);
                    });
                }
            }
        };
        xhr.open("POST", "comment");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(datastr);
    });

    // 댓글 개수
    let commentLength = $('.comment_div').length;
    $('#commentLength').text(`COMMENT: ${commentLength}개`);

    // 댓글 제한 수 타이핑
    $('#commentArea').keyup(function (e) {
        let content = $(this).val();
        let count = content.length;
        if (count == 0 || content == '') {
            $('.maxLength-box-font').text('0 / 200');
        } else {
            $('.maxLength-box-font').text(`${count} / 200`);
        }
    });

    // 응모하기 버튼 누를 시 스크롤 이동
    function dropped() {
        document.getElementById('section2').scrollIntoView({behavior: 'smooth'});
    }

    var timer = setTimeout(updateViews, 10000); // 10초 타이머 (10000ms)

    function updateViews() {
        var serialno = $('#serialno').text();
        var data = {serialnoAJAX: serialno};
        var datastr = JSON.stringify(data);
        
        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4) {
                var data = xhr.responseText;
                var obj = JSON.parse(data);
            }
        };
        xhr.open("POST", "update_views");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(datastr);
    }
}); 
