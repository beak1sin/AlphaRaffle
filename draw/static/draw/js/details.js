function comment() {
    commentValue = document.getElementById("commentArea").value;
    if (commentValue == "") {
        $('#comment_error_msg').show();
        return false;
    }
}

function dropped() {
    document.getElementById('section2').scrollIntoView({behavior: 'smooth'});
}

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
}); 

//heart 좋아요 클릭시! 하트 뿅
$(function(){
    var $likeBtn =$('.icon.heart');

        $likeBtn.click(function(){
            $likeBtn.toggleClass('active');

            if($likeBtn.hasClass('active')){          
               $(this).find('img').attr({
                  'src': 'https://cdn-icons-png.flaticon.com/512/803/803087.png',
                   alt:'좋아요 완료'
                    });
              
              
             }else{
                $(this).find('i').removeClass('fas').addClass('far')
               $(this).find('img').attr({
                  'src': 'https://cdn-icons-png.flaticon.com/512/812/812327.png',
                  alt:"좋아요"
               })
         }
     })
})