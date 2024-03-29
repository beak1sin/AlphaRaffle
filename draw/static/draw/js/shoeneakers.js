$(document).ready(function() {
    // input x버튼 기능
    $(".input-value").on("input", function() {
        if ($(this).val().length > 0) {
            // $('.input-icon-close').addClass('active');
            $(this).next().addClass('active');
            // $('.input-icon-close').click(function() {
            $(this).next().click(function() {
                // $(".input-value").val('');
                $(this).prev().val('');
                $(this).removeClass('active');
            });
        } else {
            // $('.input-icon-close').removeClass('active');
            $(this).next().removeClass('active');
        }
    });

    // 패스워드 x버튼 기능
    $(".password-value").on("input", function() {
        if ($(this).val().length > 0) {
            $(this).next().addClass('active');
            $(this).next().click(function() {
                $(this).prev().val('');
                $(this).removeClass('active');
            });
        } else {
            $(this).next().removeClass('active');
        }
    });

    // 비밀번호 숨기기 해제 기능
    $('.password-icon-hide').click(function () {
        if ($(this).hasClass('active')) {
            $(this).removeClass('active');
            $(this).next().attr('type', 'password');
        } else {
            $(this).addClass('active');
            $(this).next().attr('type', 'text');
        }
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

    // 북마크 기능
    $('.grid-wrapper').on('click', '.bookmark-icon-label', function(event) {
        event.preventDefault();
        let $serialno = $(this).parent().parent().parent().parent().parent().attr('data-value');
        
        var $this = $(this);
        var $count = $(this).parent().next().children();
  
        var data = {serialnoAJAX: $serialno};
        var datastr = JSON.stringify(data);
  
        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                var data = xhr.responseText;
  
                var obj = JSON.parse(data);
  
                if (obj.flag == '0') {
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

    // 현재 사용x
    // 북마크확인버튼 클릭 시 로그인페이지로 이동
    $(document).on("click", "#goLogin_btn", function (e){
        location.href = '/auth/login/';
    });

    // 현재 사용x
    // 신고 로그인 여부
    $('.report_btn').click(function () {
      var data = {};
      var datastr = JSON.stringify(data);
      xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
          if (xhr.readyState == 4) {
              var data = xhr.responseText;

              var obj = JSON.parse(data);

              if(obj.flag == "0"){
                  // 로그인 X
                  // alert(obj.result_msg);
                  reportLayerOn();
                  // 레이어 외부 영역, 취소 버튼 클릭 시
                  $('.u-section-1.blurOn, .u-section-2.blurOn, .u-section-3.blurOn, .u-section-4.blurOn, #cancel_btn').click(function () {
                    reportLayerOff();
                  });
              } else {
                  // 로그인 O
                  // alert(obj.result_msg);
                  reportFormLayerOn();
                  // 레이어 외부 영역, 취소 버튼 클릭 시
                  $('.u-section-1.blurOn, .u-section-2.blurOn, .u-section-3.blurOn, .u-section-4.blurOn, #cancel_btn').click(function () {
                    reportFormLayerOff();
                  });
              }
          }
      };
      xhr.open("POST", "reportLayer");
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
      xhr.send(datastr);

  });

    // 현재 사용x
    // 신고 전송하기
  $('#report_btn').click(function () {
    let reportValue = $('.content_area_value').val();
    if (reportValue == '' || reportValue.length == 0) {
      alert('내용을 입력해주세요.');
      return false;
    }
    var data = {reportValueAJAX: reportValue};
    var datastr = JSON.stringify(data);
    xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            var data = xhr.responseText;

            var obj = JSON.parse(data);

            if(obj.flag == "0"){
                // 로그인 X
                alert(obj.result_msg);
            } else {
                // 로그인 O
                alert(obj.result_msg);
                reportFormLayerOff();
            }
        }
    };
    xhr.open("POST", "report");
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.send(datastr);

  });

  function bookmarkLayerOn () {
    $('.bookmark-layer').removeClass('off');
    $('.bookmark-layer').addClass('on');
    $('.u-section-1').removeClass('blurOff');
    $('.u-section-1').addClass('blurOn');
    $('.u-section-2').removeClass('blurOff');
    $('.u-section-2').addClass('blurOn');
  }

  function bookmarkLayerOff () {
    $(".bookmark-layer").removeClass("on");
    $('.u-section-1').removeClass("blurOn");
    $('.u-section-2').removeClass("blurOn");
    $(".bookmark-layer").addClass("off");
    $('.u-section-1').addClass("blurOff");
    $('.u-section-2').addClass("blurOff");
  }

  function reportLayerOn () {
    $('.report-layer').removeClass('off');
    $('.report-layer').addClass('on');
    $('.u-section-1').removeClass('blurOff');
    $('.u-section-1').addClass('blurOn');
    $('.u-section-2').removeClass('blurOff');
    $('.u-section-2').addClass('blurOn');
    $('.u-section-3').removeClass('blurOff');
    $('.u-section-3').addClass('blurOn');
    $('.u-section-4').removeClass('blurOff');
    $('.u-section-4').addClass('blurOn');
  }

  function reportLayerOff () {
    $('.report-layer').removeClass('on');
    $('.report-layer').addClass('off');
    $('.u-section-1').removeClass('blurOn');
    $('.u-section-1').addClass('blurOff');
    $('.u-section-2').removeClass('blurOn');
    $('.u-section-2').addClass('blurOff');
    $('.u-section-3').removeClass('blurOn');
    $('.u-section-3').addClass('blurOff');
    $('.u-section-4').removeClass('blurOn');
    $('.u-section-4').addClass('blurOff');
  }

  function reportFormLayerOn () {
    $('.report-form-layer').removeClass('off');
    $('.report-form-layer').addClass('on');
    $('.u-section-1').removeClass('blurOff');
    $('.u-section-1').addClass('blurOn');
    $('.u-section-2').removeClass('blurOff');
    $('.u-section-2').addClass('blurOn');
    $('.u-section-3').removeClass('blurOff');
    $('.u-section-3').addClass('blurOn');
    $('.u-section-4').removeClass('blurOff');
    $('.u-section-4').addClass('blurOn');
  }

  function reportFormLayerOff () {
    $('.report-form-layer').removeClass('on');
    $('.report-form-layer').addClass('off');
    $('.u-section-1').removeClass('blurOn');
    $('.u-section-1').addClass('blurOff');
    $('.u-section-2').removeClass('blurOn');
    $('.u-section-2').addClass('blurOff');
    $('.u-section-3').removeClass('blurOn');
    $('.u-section-3').addClass('blurOff');
    $('.u-section-4').removeClass('blurOn');
    $('.u-section-4').addClass('blurOff');
  }

  $('.search-link, .search-icon').click(function() {
    $('.search-section').show();
    $('#scroll-container').css({'overflow': 'hidden'});
    $('.left-search-ad-box-js').html('<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-2714501163035094" data-ad-slot="9094761939" data-ad-format="vertical" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script>');
    $('.right-search-ad-box-js').html('<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-2714501163035094" data-ad-slot="1575364567" data-ad-format="vertical" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script>');
  });

  $('.cancel-icon').click(function() {
    $('.search-section').hide();
    $('#scroll-container').css({'overflow': 'scroll'});
  })

    $('.xbutton-icon-label').click(function() {
        let $recent_search = $(this).parent().parent().prev().text();
        let $recent_search_value = $(this).parent().parent().parent();

        var data = {recent_searchAJAX: $recent_search};
        var datastr = JSON.stringify(data);

        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                var data = xhr.responseText;

                var obj = JSON.parse(data);

                if (obj.flag == '1') {
                    alert(obj.result_msg);
                    $recent_search_value.remove();
                    if ($('.recent-items').length == 0) {
                        var html = '<p style="margin: 0px; font-size: 20px; font-weight: 400;">최근 검색어가 없습니다.</p>';
                        $('.recent-flex').append(html);
                    }
                }
            }
        };
        xhr.open("POST", "delete_recent_searches");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(datastr);
    });

    $('#all_recent_delete').click(function() {
        var data = {};
        var datastr = JSON.stringify(data);

        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                var data = xhr.responseText;

                var obj = JSON.parse(data);

                if (obj.flag == '1') {
                    alert(obj.result_msg);
                    if (obj.recent == '존재유') {
                        $('.recent-flex > div').remove();
                        var html = '<p style="margin: 0px; font-size: 20px; font-weight: 400;">최근 검색어가 없습니다.</p>';
                        $('.recent-flex').append(html);
                    }
                } else {
                    alert(obj.result_msg);
                }
            }
        };
        xhr.open("POST", "all_recent_delete");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(datastr);
    });
    
    // 맨위로 가는 버튼
    $('.goup-icon-label').click(function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth' // 부드러운 스크롤을 위해 'smooth' 옵션 사용
        });
    });

    $('#search_form').submit(function(event) {
        event.preventDefault();
        // const url = window.location.href;
        const url = window.location.protocol + '//' + window.location.host + '/full/';
        const paramName = $('#search_value').attr('name');
        const paramValue = $('#search_value').val().trim();
        const newURL = addParamToURL(url, paramName, paramValue);
        window.location.href = newURL;
    });

    function addParamToURL(url, paramName, paramValue) {
        const urlParams = new URLSearchParams(window.location.search);
        urlParams.delete('serialnum');
        if (paramName != "serialnum") {
            urlParams.set(paramName, paramValue);
        }
      
        // 기존 URL의 경로와 파라미터를 유지하면서 새로운 파라미터를 덧붙임
        const newURL = `${url.split('?')[0]}?${urlParams}`;
      
        return newURL;
    }

    $('.recent-searches-value').click(function() {
        const url = window.location.protocol + '//' + window.location.host + '/full/';
        const paramName = 'search_term';
        const paramValue = $(this).text();
        const newURL = addParamToURL(url, paramName, paramValue);
        window.location.href = newURL;
    });

    $(document).on('click', '.profile-img', function() {
        if ($(this).hasClass('off')) {
            $(this).removeClass('off').addClass('on');
            $('.profile-list').removeClass('off').addClass('on');
        } else if ($(this).hasClass('on')) {
            $(this).removeClass('on').addClass('off');
            $('.profile-list').removeClass('on').addClass('off');
        }
    });

    // profile-img 제외 남은 여백 클릭 시 이벤트
    $(document).on('click', function(event) {
        // 클릭된 요소가 .profile-list 또는 그 자식 요소, 또는 .profile-img가 아니면
        if (!$(event.target).closest('.profile-list').length && !$(event.target).hasClass('profile-img')) {
            // .profile-list가 on 상태인 경우에만 off로 변경
            if ($('.profile-list').hasClass('on')) {
                $('.profile-img').removeClass('on').addClass('off');
                $('.profile-list').removeClass('on').addClass('off');
            }
        }
    });
});

$(document).ready(function() {
	// 로딩화면 출력
	$(".backL").css("display", "");
});
$(window).load(function() {
	// 로딩 완료되었을때
	$(".backL").css("display", "none");
});

// channels

/* 
const loc = window.location.href.split(window.location.host)[1];

const socket = new WebSocket(`ws://${window.location.host}/ws${loc}`);
// console.log(socket);
var dataBox = $('#notificationBox');

socket.onmessage = (e) => {
    // console.log('Server: ' + e.data);
    const {message, sender} = JSON.parse(e.data);
    console.log(message);
    console.log(sender);
    // dataBox.html(`<p>${sender}: ${message}`);
};

socket.onopen = (e) => {
    socket.send(JSON.stringify({
        'message': 'Hello from Client',
        'sender': 'test sender'
    }));
};

$('.bookmark-icon-label').click(() => {
    const message = '클릭됨';
    socket.send(JSON.stringify({
        'message': message,
        'sender': $('.user_hidden').text()
    }));
});

*/

// $('.comment-send-icon-label').click(function() {
//     alert('전송');
//     const receiver = $(this).parent().parent().parent().parent().children(':first').children(':first').text();
//     const message = '댓글 연습';
//     alert(receiver);
//     socket.send(JSON.stringify({
//         'message': message,
//         'sender': $('.user_hidden').text(),
//         'receiver': receiver
//     }));
// });



// 마우스커서

// var polyline = document.querySelector('.drawing_line_polyline');
// var polyPoints = polyline.getAttribute('points');
// var circle = document.querySelector('.drawing_line_circle');
// var circleX = circle.getAttribute('cx');
// var circleY = circle.getAttribute('cy');
// var circleR = circle.getAttribute('r');

// var total = 12;
// var gap = 30;
// var ease = 0.5;
// var debounce_removeLine;
// var debounce_counter = 0;

// var pointer = {
//   x: window.innerWidth / 2,
//   y: window.innerHeight / 2,
//   tx: 0,
//   ty: 0,
//   dist: 0,
//   scale: 1,
//   speed: 2,
//   circRadius: 8,
//   updateCrds: function () {
//     if (this.x != 0) {
//       this.dist = Math.abs((this.x - this.tx) + (this.y - this.ty));
//       this.scale = Math.max(this.scale + ((100 - this.dist * 8) * 0.01 - this.scale) * 0.1, 0.25); // gt 0.25 = 4px
//       this.tx += (this.x - this.tx) / this.speed;
//       this.ty += (this.y - this.ty) / this.speed;
//     }
//   }
// };

// var points = [];

// $(window).on('mousemove', function (e) {
//   pointer.x = e.clientX;
//   pointer.y = e.clientY;
//   debounce_counter = 0;
//   drawLine();

//   // debounce
//   clearTimeout(debounce_removeLine);
//   debounce_removeLine = setTimeout(() => {
//     //console.log('debounce_removeLine', new Date().getTime());
//     debounce_counter = 12;
//     drawLine();
//   }, 80);
// })

// $(window).on('mousedown', function (e) {
//   pointer.circRadius = 6;
//   drawLine();
// });

// $(window).on('mouseup', function (e) {
//   pointer.circRadius = 8;
//   drawLine();
// });

// function drawLine() {
//   pointer.updateCrds();

//   points.push({
//     x: pointer.tx,
//     y: pointer.ty
//   });
//   while (points.length > total) {
//     points.shift();
//     if (points.length > gap) {
//       for (var i = 0; i < 5; i++) {
//         points.shift();
//       }
//     }
//   }
//   var pointsArr = points.map(point => `${point.x},${point.y}`);
//   polyPoints = pointsArr.join(' ');
//   polyline.setAttribute('points', polyPoints);

//   // circle
//   circleX = pointer.x;
//   circleY = pointer.y;
//   circleR = pointer.scale * pointer.circRadius;

//   circle.setAttribute('cx', circleX);
//   circle.setAttribute('cy', circleY);
//   circle.setAttribute('r', circleR);

//   if (debounce_counter > 0) {
//     debounce_counter--;
//     requestAnimationFrame(drawLine);
//   }
// }
// ----------마우스커서