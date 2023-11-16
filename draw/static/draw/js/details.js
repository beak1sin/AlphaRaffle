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
        $(".backL").css("display", "");
        let $comment = $(this).parent().prev();
        let $commentValue = $comment.val().trim();
        if ($commentValue.trim() == "") {
            alert('댓글을 입력해주세요.');
            $comment.val("");
            $comment.focus();
            $(".backL").css("display", "none");
            return false;
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
                    $(".backL").css("display", "none");
                } else {
                    // 현재경로 + 공백추가 필수!!
                    $('.box3').load(location.href + " .box3", function() {
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
                       $(".backL").css("display", "none");
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

    $('.comment-option-icon-label').click(function() {
        $(this).parent().next().show();
        $(this).parent().hide();
    });

    $('.comment-option-cancel').click(function() {
        $(this).parent().prev().show();
        $(this).parent().hide();
    });

    $('.comment-option-delete').click(function() {
        let $nickname = $(this).parent().parent().children('span:eq(0)').text();
        let $pk = $(this).parent().parent().parent().parent().attr('data-value');
        let self = this;

        var data = {nicknameAJAX: $nickname, pkAJAX: $pk};
        var datastr = JSON.stringify(data);

        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4) {
                var data = xhr.responseText;
                var obj = JSON.parse(data);
                if (obj.flag == "0") {
                    alert(obj.result_msg);
                } else {
                    $(self).parent().parent().parent().parent().css({'text-align': 'center'});
                    $(self).parent().parent().parent().parent().html(obj.result_msg);
                }
            }
        };
        xhr.open("POST", "comment_delete_details");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(datastr);
    }); 
});

// document.addEventListener('DOMContentLoaded', function() {
//     if (window.location.hostname != "127.0.0.1") {
//         var adContainerTop = document.querySelector('.top-ad-box-js'); // 광고를 표시할 컨테이너 선택 (상단)
//         var adContainerBottom = document.querySelector('.bottom-ad-box-js'); // 광고를 표시할 컨테이너 선택 (하단)

//         var adScriptTop = document.createElement('script'); // 새로운 <script> 태그 생성 (상단)
//         adScriptTop.setAttribute('type', 'text/javascript');
//         adScriptTop.setAttribute('src', '//t1.daumcdn.net/kas/static/ba.min.js');
//         adScriptTop.setAttribute('async', true);

//         var adElementTop = document.createElement('ins');
//         adElementTop.className = 'kakao_ad_area';
//         adElementTop.style.display = 'none';


//         var adScriptBottom = document.createElement('script'); // 새로운 <script> 태그 생성 (하단)
//         adScriptBottom.setAttribute('type', 'text/javascript');
//         adScriptBottom.setAttribute('src', '//t1.daumcdn.net/kas/static/ba.min.js');
//         adScriptBottom.setAttribute('async', true);

//         var adElementBottom = document.createElement('ins');
//         adElementBottom.className = 'kakao_ad_area';
//         adElementBottom.style.display = 'none';

//         // 화면의 너비에 따라 적절한 광고 데이터 설정
//         if (window.innerWidth < 728) {
//             adElementTop.setAttribute('data-ad-unit', 'DAN-emBQqKhNUlAEd2Cb');
//             adElementTop.setAttribute('data-ad-width', '320');
//             adElementTop.setAttribute('data-ad-height', '100');
//             adElementBottom.setAttribute('data-ad-unit', 'DAN-gotHkYVL9z9PnsAc');
//             adElementBottom.setAttribute('data-ad-width', '320');
//             adElementBottom.setAttribute('data-ad-height', '100');
//         } else {
//             adElementTop.setAttribute('data-ad-unit', 'DAN-c65JhAo32jkuvteX');
//             adElementTop.setAttribute('data-ad-width', '728');
//             adElementTop.setAttribute('data-ad-height', '90');
//             adElementBottom.setAttribute('data-ad-unit', 'DAN-VGpc879tojj1N4DK');
//             adElementBottom.setAttribute('data-ad-width', '728');
//             adElementBottom.setAttribute('data-ad-height', '90');

//             var adContainerLeft = document.querySelector('.left-ad-box-js'); // 광고를 표시할 컨테이너 선택 (상단)
//             var adContainerRight = document.querySelector('.right-ad-box-js'); // 광고를 표시할 컨테이너 선택 (하단)

//             var adScriptLeft = document.createElement('script'); // 새로운 <script> 태그 생성 (상단)
//             adScriptLeft.setAttribute('type', 'text/javascript');
//             adScriptLeft.setAttribute('src', '//t1.daumcdn.net/kas/static/ba.min.js');
//             adScriptLeft.setAttribute('async', true);

//             var adElementLeft = document.createElement('ins');
//             adElementLeft.className = 'kakao_ad_area';
//             adElementLeft.style.display = 'none';


//             var adScriptRight = document.createElement('script'); // 새로운 <script> 태그 생성 (하단)
//             adScriptRight.setAttribute('type', 'text/javascript');
//             adScriptRight.setAttribute('src', '//t1.daumcdn.net/kas/static/ba.min.js');
//             adScriptRight.setAttribute('async', true);

//             var adElementRight = document.createElement('ins');
//             adElementRight.className = 'kakao_ad_area';
//             adElementRight.style.display = 'none';

//             adElementLeft.setAttribute('data-ad-unit', 'DAN-1NwSKO1ZHXmfBv0V');
//             adElementLeft.setAttribute('data-ad-width', '160');
//             adElementLeft.setAttribute('data-ad-height', '600');
//             adElementRight.setAttribute('data-ad-unit', 'DAN-H42zUYW4NZAQhFT8');
//             adElementRight.setAttribute('data-ad-width', '160');
//             adElementRight.setAttribute('data-ad-height', '600');

//             adContainerLeft.appendChild(adElementLeft);
//             adContainerLeft.appendChild(adScriptLeft);
//             adContainerRight.appendChild(adElementRight);
//             adContainerRight.appendChild(adScriptRight);
//         }

//         // 광고 요소와 스크립트를 컨테이너에 추가
//         adContainerTop.appendChild(adElementTop);
//         adContainerTop.appendChild(adScriptTop);
//         adContainerBottom.appendChild(adElementBottom);
//         adContainerBottom.appendChild(adScriptBottom);
//     }
// });