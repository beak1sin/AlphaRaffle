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

    $('.bookmark-icon-label').click(function() {
        let $serialno = $(this).parent().parent().parent().parent().attr('data-value');
  
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

    // 북마크 로그인 여부
    // $('input[type=checkbox][name=bookmark]').change(function ()  {
    //     // let $serialno = $(this).parent().parent().parent().parent().next().next().attr('data-value');
    //     let $serialno = $(this).parent().parent().parent().parent().parent().attr('data-value');

    //     var data = {serialnoAJAX: $serialno};
    //     var datastr = JSON.stringify(data);
    //     if ($('.bookmark-icon-label').hasClass('on')) {
    //         xhr = new XMLHttpRequest();
    //         xhr.onreadystatechange = function() {
    //             if (xhr.readyState == 4) {
    //                 var data = xhr.responseText;
        
    //                 var obj = JSON.parse(data);
    
    //                 if(obj.flag == "0"){
    //                     // 로그인 X
    //                     bookmarkLayerOn();
    //                     // 레이어 외부 영역, 취소 버튼 클릭 시
    //                     $('.u-section-1.blurOn, .u-section-2.blurOn, #cancel_btn').click(function () {
    //                       bookmarkLayerOff();
    //                     });
    //                 } else {
    //                     // 로그인 O
    //                     alert(obj.result_msg);
    //                     $('.bookmark-icon-label').removeClass('on');
    //                 }
    //             }
    //         };
    //         xhr.open("POST", "likeCancel");
    //         xhr.setRequestHeader("X-CSRFToken", csrftoken);
    //         xhr.send(datastr);
    //     } else {
    //         xhr = new XMLHttpRequest();
    //         xhr.onreadystatechange = function() {
    //             if (xhr.readyState == 4) {
    //                 var data = xhr.responseText;
        
    //                 var obj = JSON.parse(data);

    //                 if(obj.flag == "0"){
    //                     // 로그인 X
    //                     bookmarkLayerOn();
    //                     // 레이어 외부 영역, 취소 버튼 클릭 시
    //                     $('.u-section-1.blurOn, .u-section-2.blurOn, #cancel_btn').click(function () {
    //                     bookmarkLayerOff();
    //                     });
    //                 } else {
    //                     // 로그인 O
    //                     alert(obj.result_msg);
    //                     $('.bookmark-icon-label').addClass('on');
    //                 }
    //             }
    //         };
    //         xhr.open("POST", "like");
    //         xhr.setRequestHeader("X-CSRFToken", csrftoken);
    //         xhr.send(datastr);
    //     }
    // });
    

    // 북마크확인버튼 클릭 시 로그인페이지로 이동
    $(document).on("click", "#goLogin_btn", function (e){
        location.href = '/auth/login/';
    });

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

  var isLoading = false;

  window.addEventListener('scroll', function() {
      var scrollContainer = document.getElementById('scroll-container');
      var scrollHeight = scrollContainer.scrollHeight;
      var scrollTop = Math.ceil(window.pageYOffset || document.documentElement.scrollTop);
      var windowHeight = window.innerHeight;

    //   console.log('scrollContainer의 scrollHeight: ' + scrollHeight, 'scrollTop: ' + scrollTop, 'windowHeight: ' + windowHeight);
      
      if (!isLoading && scrollTop + windowHeight >= scrollHeight) {
          // 추가 데이터를 불러오는 작업 수행
          isLoading = true;
          loadData(function() {
              isLoading = false;
          });
      }
  });

  var nextPage = 2;  // 초기 페이지 번호

  function loadData(callback) {
      // AJAX 요청을 통해 추가 데이터를 백엔드에 요청합니다.
      // 백엔드에서는 페이지 번호 등을 기반으로 필요한 데이터를 반환해야 합니다.

      // AJAX 요청 예시 (jQuery 사용):
      var data = {page: nextPage};
      var datastr = JSON.stringify(data);
      
      xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
          if (xhr.readyState == 4) {
              var data = xhr.responseText;
  
              var obj = JSON.parse(data);
              var shoe = JSON.parse(obj.shoes);
              var likes = obj.likes;  // 멤버별 신발 좋아요 여부
              nextPage += 1;
              // alert();
              var html = '';
              for (var i = 0; i < shoe.length; i++) {
                  var shoe1 = shoe[i].fields;
                  var liked = likes[i];
                  html += '<div class="grid-box" data-value="' + shoe1.serialno + '">';
                  html += '<div class="grid-container"><div class="grid-img-box">';
                  html += '<div class="comment-icon"><label class="comment-icon-label"><span class="icon"></span></label></div>';
                  html += '<div class="commentCount-box"><p class="commentCount">0</p></div>';
                  html += '<div class="img-box" onclick="location.href = \'' + STATIC_FULL_URL + shoe1.serialno + '\'">';
                  html += '<img class="lazyload shoeimg" data-src="' + STATIC_IMAGES_URL + shoe1.shoename + shoe1.serialno + '0.jpeg"></div>';
                  html += '<div class="bookmark-icon">';
                  html += '<label class="bookmark-icon-label' + (liked ? ' on' : '') + '">';
                  html += '<span class="icon"></span></label></div>';
                  html += '<div class="shoelikecount-box"><p class="shoelikecount">' + shoe1.shoelikecount + '</p></div></div>';
                  html += '<div class="grid-shoename-box"><p class="shoename">' + shoe1.shoename + '</p></div>';
                  html += '<div class="grid-pubdate-box"><p class="pubdate">' + shoe1.pubdate + '</p></div>';
                  html += '<div class="grid-goBtn-box"><button class="goBtn" onclick="location.href = \'' + STATIC_FULL_URL + shoe1.serialno + '\'">바로가기</button></div>';
                  html += '</div></div>';
              }
              $('.infinite-container').append(html);

              $('.bookmark-icon-label').click(function() {
                  let $serialno = $(this).parent().parent().parent().parent().attr('data-value');
            
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

              if (typeof callback === 'function') {
                  callback();
              }
          }
      };
      xhr.open("POST", "");
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
      xhr.send(datastr);
  }

  $('.search-link').click(function() {
    $('.search-section').show();
    $('#scroll-container').css({'overflow': 'hidden'});
  });

  $('.search-close-btn').click(function() {
    $('.search-section').hide();
    $('#scroll-container').css({'overflow': 'scroll'});
  })

});



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