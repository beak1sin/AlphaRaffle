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
  
  $('.search-link').click(function() {
    $('.search-section').show();
    $('#scroll-container').css({'overflow': 'hidden'});
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