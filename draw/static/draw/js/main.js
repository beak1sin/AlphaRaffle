//current position
var pos = 0;
//number of slides
var totalSlides = $('#slider-wrap ul #slider_list').length;
// var totalSlides = $('#slider_list').length;
//get the slide width
var sliderWidth = $('#slider-wrap').width();
var totalWidth = 0;


$(window).resize(function() {
    totalSlides = $('#slider-wrap ul #slider_list').length;
    // totalSlides = $('#slider_list').length;
    sliderWidth = $('#slider-wrap').width();
    totalWidth = $('#slider').width();
    $('#slider-wrap ul#slider').width(sliderWidth*totalSlides + 2);
    // console.log(totalSlides + ', ' + sliderWidth + ', ' + totalWidth);
    // console.log($('.lazyload').width());
});


$(document).ready(function(){
  // alert($('.lazyload').width());
  /*****************
   BUILD THE SLIDER
  *****************/
  //set width to be 'x' times the number of slides
  $('#slider-wrap ul#slider').width(sliderWidth*totalSlides+2);
  
    //next slide  
  $('#next').click(function(){
    slideRight();
  });
  
  //previous slide
  $('#previous').click(function(){
    slideLeft();
  });
  
  
  
  /*************************
   //*> OPTIONAL SETTINGS
  ************************/
  //automatic slider
  var autoSlider = setInterval(slideRight, 15000);
  
  //for each slide 
  $.each($('#slider-wrap ul li'), function() { 

     //create a pagination
     var li = document.createElement('li');
     $('#pagination-wrap ul').append(li);    
  });
  
  //counter
  countSlides();
  
  //pagination
  pagination();
  
  //hide/show controls/btns when hover
  //pause automatic slide when hover
  $('#slider-wrap').hover(
    function(){ $(this).addClass('active'); clearInterval(autoSlider); }, 
    function(){ $(this).removeClass('active'); autoSlider = setInterval(slideRight, 3000); }
  );

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

  $('.full-tab, .dropped-tab, .end-tab').click(function() {
    var $name = $(this).attr('class');
    switch($name) {
        case 'dropped-tab':
            $('.full-section').hide();
            $('.droppedShoe-section').show();
            $('.endShoe-section').hide();
            $('.droppedShoeLength').show();
            $('.upcomingShoeLength').hide();
            $('.endShoeLength').hide();
            $(this).css({'color': '#FFFFFF', 'font-weight': '500'});
            $('.full-tab').css({'color': 'rgba(255, 255, 255, 0.7)', 'font-weight': '300'});
            $('.end-tab').css({'color': 'rgba(255, 255, 255, 0.7)', 'font-weight': '300'});
            break;
        case 'full-tab':
            $('.full-section').show();
            $('.droppedShoe-section').hide();
            $('.endShoe-section').hide();
            $('.droppedShoeLength').hide();
            $('.upcomingShoeLength').show();
            $('.endShoeLength').hide();
            $(this).css({'color': '#FFFFFF', 'font-weight': '500'});
            $('.dropped-tab').css({'color': 'rgba(255, 255, 255, 0.7)', 'font-weight': '300'});
            $('.end-tab').css({'color': 'rgba(255, 255, 255, 0.7)', 'font-weight': '300'});
            break;
        case 'end-tab':
            $('.full-section').hide();
            $('.droppedShoe-section').hide();
            $('.endShoe-section').show();
            $('.droppedShoeLength').hide();
            $('.upcomingShoeLength').hide();
            $('.endShoeLength').show();
            $(this).css({'color': '#FFFFFF', 'font-weight': '500'});
            $('.dropped-tab').css({'color': 'rgba(255, 255, 255, 0.7)', 'font-weight': '300'});
            $('.full-tab').css({'color': 'rgba(255, 255, 255, 0.7)', 'font-weight': '300'});
            break;
    }
  });

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
                  html += '<div class="img-box" onclick="window.open(\'' + STATIC_FULL_URL + shoe1.serialno + '\', \'_blank\')">'; 
                  html += '<img class="lazyload shoeimg" data-src="' + STATIC_IMAGES_URL + shoe1.shoename + shoe1.serialno + '0.avif"></div>';
                  html += '<div class="bookmark-icon">';
                  html += '<label class="bookmark-icon-label' + (liked ? ' on' : '') + '">';
                  html += '<span class="icon"></span></label></div>';
                  html += '<div class="shoelikecount-box"><p class="shoelikecount">' + shoe1.shoelikecount + '</p></div></div>';
                  html += '<div class="grid-shoename-box"><p class="shoename">' + shoe1.shoename + '</p></div>';
                  html += '<div class="grid-pubdate-box"><p class="pubdate">' + shoe1.pubdate + '</p></div>';
                  html += '<div class="grid-goBtn-box"><button class="goBtn" onclick="window.open(\'' + STATIC_FULL_URL + shoe1.serialno + '\', \'_blank\')">바로가기</button></div>';
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
                            //   $('.bookmark-layer').removeClass('off');
                            //   $('.bookmark-layer').addClass('on');
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

  var bannerBoxBottom = $('.banner-box').offset().top + $('.banner-box').height() - 42;
  var adBox = $('.ad-box');
  var adBoxPos = $('.ad-box-pos');

  if ($(window).scrollTop() > bannerBoxBottom) {
      adBox.addClass('fixed');
  } else {
      adBox.removeClass('fixed');
  }
  
  $(window).scroll(function() {
      var scrollPos = $(window).scrollTop();
      if (scrollPos > bannerBoxBottom) {
          adBox.addClass('fixed');
          adBoxPos.addClass('fixed');
      } else {
          adBox.removeClass('fixed');
          adBoxPos.removeClass('fixed');
      }
  });

});//DOCUMENT READY


/***********
 SLIDE LEFT
************/
function slideLeft(){
  pos--;
  if(pos==-1){ pos = totalSlides-1; }
  $('#slider-wrap ul#slider').css('left', -(sliderWidth*pos));  
  
  //*> optional
  countSlides();
  pagination();
}


/************
 SLIDE RIGHT
*************/
function slideRight(){
  pos++;
  if(pos==totalSlides){ pos = 0; }
  $('#slider-wrap ul#slider').css('left', -(sliderWidth*pos)); 
  
  //*> optional 
  countSlides();
  pagination();
}



  
/************************
 //*> OPTIONAL SETTINGS
************************/
function countSlides(){
  $('#counter').html(pos+1 + ' / ' + totalSlides);
}

function pagination(){
  $('#pagination-wrap ul li').removeClass('active');
  $('#pagination-wrap ul li:eq('+pos+')').addClass('active');
}

// const infinite = new Waypoint.Infinite({
//   element: $('.infinite-container')[0],
//   offset: 'bottom-in-view',
//   onBeforePageLoad : function() {

//   },
//   onAfterPageLoad : function() {

//   }
// })