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

    // 발매정보 없으면 section 사이즈 줄이기
    if ($('#noDropped').length > 0) {
      $('.u-section-2 .u-sheet-1').css('min-height', '300px');
    }
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

const $text = document.querySelector(".text");

// 글자 입력 속도
const speed = 100;

const changeLineBreak = (letter) => {
  return letter.map(text => text === "\n" ? "<br>" : text);
}
const letters = "클릭 한 번으로 응모해보세요"

// 타이핑 효과
const typing = async () => {  
  const letter = changeLineBreak(letters.split(""));
  
  while (letter.length) {
    await wait(speed);
    $text.innerHTML += letter.shift(); 
  }
  
  // 잠시 대기
  await wait(1500)
  
  // 지우는 효과
  remove();
}

// 글자 지우는 효과
const remove = async () => {
  const letter = changeLineBreak(letters.split(""));
  
  while (letter.length) {
    await wait(speed);
    
    letter.pop();
    $text.innerHTML = letter.join(""); 
  }
  
  await wait(1000)
  // 다음 순서의 글자로 지정, 타이핑 함수 다시 실행
  typing();
}

// 딜레이 기능 ( 마이크로초 )
function wait(ms) {
  return new Promise(res => setTimeout(res, ms))
}

// 초기 실행
setTimeout(typing, 1500);