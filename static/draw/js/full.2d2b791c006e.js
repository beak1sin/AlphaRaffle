$(document).ready(function() {
    $(window).scroll(function(){
			
        $('.product-item').each( function(i){
            
            var bottom_of_element = $(this).offset().top + $(this).outerHeight() / 10;
            var bottom_of_window = $(window).scrollTop() + $(window).height();
            
            if( bottom_of_window > bottom_of_element ){
                // $(this).animate({'opacity':'1'},1000);
                // $(this).fadeTo(1000, 1);
                $(this).css({
                    'animation': 'fadeInUp 2s',
                    'opacity': 1
                });
            }
            
        }); 
    });
});



function sidebar() {
    if ($('.filter-layer').hasClass("off")) {
        $('.filter-layer').removeClass("off");
        $('.u-section-1').removeClass("blurOff");
        $('.filter-layer').addClass("on");
        $('.u-section-1').addClass("blurOn");
        $('.u-section-1').attr("onclick", "filterClose();");
        // alert('??');
    } else {
        $('.filter-layer').removeClass("on");
        $('.u-section-1').removeClass("blurOn");
        $('.filter-layer').addClass("off");
        $('.u-section-1').addClass("blurOff");
        $('.u-section-1').removeAttr("onclick");
    }
}

function filterClose() {
  $('.u-section-1').addClass('functionOn');
  if ($('.u-section-1').hasClass("functionOn")) {
    // $('.filter-layer').removeClass("on");
  //   $('.u-section-1').removeClass("blurOn");
  //   $('.u-section-1').removeClass("functionOn");
  //   $('.filter-layer').addClass("off");
  //   $('.u-section-1').addClass("blurOff");
  }
} 
