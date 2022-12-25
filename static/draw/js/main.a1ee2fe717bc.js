function dropped() {
    document.getElementById('section2').scrollIntoView({behavior: 'smooth'});
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

function detail() {

    serial = document.getElementById("serial").getAttribute('data-value');
    
    
    var data = { serialnum: serial};
    var datastr = JSON.stringify(data);


    xhr = new XMLHttpRequest();
    xhr.open("POST", "/auth/login/");
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.send(datastr);
}

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

$(window).load( function(){
    $('.product-item').each(function(i){
        
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

// 마우스커서
var polyline = document.querySelector('.drawing_line_polyline');
var polyPoints = polyline.getAttribute('points');
var circle = document.querySelector('.drawing_line_circle');
var circleX = circle.getAttribute('cx');
var circleY = circle.getAttribute('cy');
var circleR = circle.getAttribute('r');

var total = 12;
var gap = 30;
var ease = 0.5;
var debounce_removeLine;
var debounce_counter = 0;

var pointer = {
  x: window.innerWidth / 2,
  y: window.innerHeight / 2,
  tx: 0,
  ty: 0,
  dist: 0,
  scale: 1,
  speed: 2,
  circRadius: 8,
  updateCrds: function () {
    if (this.x != 0) {
      this.dist = Math.abs((this.x - this.tx) + (this.y - this.ty));
      this.scale = Math.max(this.scale + ((100 - this.dist * 8) * 0.01 - this.scale) * 0.1, 0.25); // gt 0.25 = 4px
      this.tx += (this.x - this.tx) / this.speed;
      this.ty += (this.y - this.ty) / this.speed;
    }
  }
};

var points = [];

$(window).on('mousemove', function (e) {
  pointer.x = e.clientX;
  pointer.y = e.clientY;
  debounce_counter = 0;
  drawLine();

  // debounce
  clearTimeout(debounce_removeLine);
  debounce_removeLine = setTimeout(() => {
    //console.log('debounce_removeLine', new Date().getTime());
    debounce_counter = 12;
    drawLine();
  }, 80);
})

$(window).on('mousedown', function (e) {
  pointer.circRadius = 6;
  drawLine();
});

$(window).on('mouseup', function (e) {
  pointer.circRadius = 8;
  drawLine();
});

function drawLine() {
  pointer.updateCrds();

  points.push({
    x: pointer.tx,
    y: pointer.ty
  });
  while (points.length > total) {
    points.shift();
    if (points.length > gap) {
      for (var i = 0; i < 5; i++) {
        points.shift();
      }
    }
  }
  var pointsArr = points.map(point => `${point.x},${point.y}`);
  polyPoints = pointsArr.join(' ');
  polyline.setAttribute('points', polyPoints);

  // circle
  circleX = pointer.x;
  circleY = pointer.y;
  circleR = pointer.scale * pointer.circRadius;

  circle.setAttribute('cx', circleX);
  circle.setAttribute('cy', circleY);
  circle.setAttribute('r', circleR);

  if (debounce_counter > 0) {
    debounce_counter--;
    requestAnimationFrame(drawLine);
  }
}
// ----------마우스커서