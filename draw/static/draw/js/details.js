$(document).ready(function() {
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

    $('.details-bookmark-icon-label').click(function() {
        var $this = $(this);
        
        var $serialno =  $('.serialno').text();
        const $serialnoSlash = $('.serialnoSlash').text();
        if ($serialnoSlash.trim() !== ""){
            $serialno = $serialnoSlash.replace('/', '_');
        }
        var $count = $('#shoelikecount');

        var data = {serialnoAJAX: $serialno};
        var datastr = JSON.stringify(data);

        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                var data = xhr.responseText;

                var obj = JSON.parse(data);

                if (obj.flag == '0') {
                    alert(obj.result_msg);
                    location.href = '/auth/login/';
                } else {
                    if(obj.liked) {
                        $this.addClass('on');
                    } else {
                        $this.removeClass('on');
                    }
                    $count.text(obj.count);
                }
            }
        };
        xhr.open("POST", "likeShoe");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(datastr);
    });

    var timer = setTimeout(updateViews, 10000); // 10초 타이머 (10000ms)

    function updateViews() {
        var serialno = $('.serialno').text();
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

    $('.commentArea').keyup(function (e) {
        let content = $(this).val();
        let count = content.length;
        let $commetLength = $(this).parent().next().next();
        if (count == 0 || content == '') {
            $commetLength.text('0 / 200');
        } else {
            $commetLength.text(`${count} / 200`);
        }
    });

    $('.comment-reply').click(function() {
         if ($(this).hasClass('off')) {
            const member_nickname = $('.nickname_hidden').text();
            var html = '<div data-id="reply-area" style="width: 100%; padding: 20px 50px; background: #EEEEEE; border-radius: 10px; margin-top: 20px;">';
            html += '<div style="height: 36px; width: 36px; float: left;">';
            html += '<img class="lazyload" style="width: 36px; height: 36px; border-radius: 50px;" data-src="' + STATIC_IMAGES_URL + 'jordan1OFF.jpeg' + '"></div>';
            html += '<span style="font-size: 20px; font-weight: 500; line-height: 36px; margin-left: 10px;">' + member_nickname +  '</span>';
            html += '<div style="width: 100%; position: relative; margin-top: 10px;">';
            html += '<input class="commentArea" style="width: 97%; height: 38px; border: none; border-bottom: 1px solid black;  background: #EEEEEE;" placeholder="댓글을 입력해주세요." maxlength="200">';
            html += '<div class="comment-reply-send-icon"><label class="comment-reply-send-icon-label"><span class="icon"></span></label></div></div>';
            html += '<span style="font-size: 12px; font-weight: 200; color: #E13030;">악성 댓글과 도배 및 스팸 댓글은 처벌 및 사용 제한 조치를 받을 수 있습니다.</span><span class="commentLength"></span></div>';
            $(this).parent().parent().append(html);
            $(this).removeClass('off');
        } else {
            $(this).parent().parent().find('div[data-id="reply-area"]').remove();
            $(this).addClass('off');
        }

        $('.comment-reply-send-icon-label').click(function() {
            alert('전송');
            const receiver = $(this).parent().parent().parent().parent().children(':first').children(':first').text();
            const message = '댓글 연습';
            alert(receiver);
            socket.send(JSON.stringify({
                'message': message,
                'sender': $('.user_hidden').text(),
                'receiver': receiver
            }));
        });

        $('.commentArea').keyup(function (e) {
            let content = $(this).val();
            let count = content.length;
            let $commetLength = $(this).parent().next().next();
            if (count == 0 || content == '') {
                $commetLength.text('0 / 200');
            } else {
                $commetLength.text(`${count} / 200`);
            }
        });
    });

    $('.comment-send-icon-label').click(function() {
        let $comment = $(this).parent().prev();
        let $commentValue = $comment.val().trim();
        if ($commentValue.trim() == "") {
            alert('댓글을 입력해주세요.');
            $comment.val("");
            $comment.focus();
            return
        }
        
        var $serialno =  $('.serialno').text();

        var data = {commentValueAJAX: $commentValue, serialnoAJAX: $serialno};
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
                        $('.commentArea').keyup(function (e) {
                            let content = $(this).val();
                            let count = content.length;
                            let $commetLength = $(this).parent().next().next();
                            if (count == 0 || content == '') {
                                $commetLength.text('0 / 200');
                            } else {
                                $commetLength.text(`${count} / 200`);
                            }
                        });

                        $('.commentArea').keypress(function(e) {
                            if (e.which == 13) {  // 13 is the ASCII code for the Enter key
                                $('.comment-send-icon-label').trigger('click');
                            }
                        });

                        $('.comment-reply').click(function() {
                            if ($(this).hasClass('off')) {
                               const member_nickname = $('.nickname_hidden').text();
                               var html = '<div data-id="reply-area" style="width: 100%; padding: 20px 50px; background: #EEEEEE; border-radius: 10px; margin-top: 20px;">';
                               html += '<div style="height: 36px; width: 36px; float: left;">';
                               html += '<img class="lazyload" style="width: 36px; height: 36px; border-radius: 50px;" data-src="' + STATIC_IMAGES_URL + 'jordan1OFF.jpeg' + '"></div>';
                               html += '<span style="font-size: 20px; font-weight: 500; line-height: 36px; margin-left: 10px;">' + member_nickname +  '</span>';
                               html += '<div style="width: 100%; position: relative; margin-top: 10px;">';
                               html += '<input class="commentArea" style="width: 97%; height: 38px; border: none; border-bottom: 1px solid black;  background: #EEEEEE;" placeholder="댓글을 입력해주세요." maxlength="200">';
                               html += '<div class="comment-reply-send-icon"><label class="comment-reply-send-icon-label"><span class="icon"></span></label></div></div>';
                               html += '<span style="font-size: 12px; font-weight: 200; color: #E13030;">악성 댓글과 도배 및 스팸 댓글은 처벌 및 사용 제한 조치를 받을 수 있습니다.</span><span class="commentLength"></span></div>';
                               $(this).parent().parent().append(html);
                               $(this).removeClass('off');
                           } else {
                               $(this).parent().parent().find('div[data-id="reply-area"]').remove();
                               $(this).addClass('off');
                           }
                   
                           $('.comment-reply-send-icon-label').click(function() {
                               alert('전송');
                               const receiver = $(this).parent().parent().parent().parent().children(':first').children(':first').text();
                               const message = '댓글 연습';
                               alert(receiver);
                               socket.send(JSON.stringify({
                                   'message': message,
                                   'sender': $('.user_hidden').text(),
                                   'receiver': receiver
                               }));
                           });
                   
                           $('.commentArea').keyup(function (e) {
                               let content = $(this).val();
                               let count = content.length;
                               let $commetLength = $(this).parent().next().next();
                               if (count == 0 || content == '') {
                                   $commetLength.text('0 / 200');
                               } else {
                                   $commetLength.text(`${count} / 200`);
                               }
                           });
                       });

                    });
                }
            }
        };
        xhr.open("POST", "comment");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(datastr);
    });

    $('.commentArea').keypress(function(e) {
        if (e.which == 13) {  // 13 is the ASCII code for the Enter key
            $('.comment-send-icon-label').trigger('click');
        }
    });

    $('.comment-reply-logout').click( () => {
        alert('로그인 후에 이용이 가능합니다.');
    });

    // $('.comment-send-icon-label').click(function() {
    //     var receiver = $(this).parent().parent().parent().parent().children(':first').children(':first').text();
    //     alert(receiver);
    // });
});