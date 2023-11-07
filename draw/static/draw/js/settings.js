$(document).ready(function() {
    $('.profile-img-change-btn').click(function() {
        document.getElementById("upload").click();
    });
    document.getElementById('upload').addEventListener('change', function(){
        $(".backL").css("display", "");
        var fileInput = document.getElementById('upload');
        var file = fileInput.files[0];
        
        var formData = new FormData();
        formData.append('file', file);
        // var url = `${window.location.protocol}//${window.location.host}/auth/mypage/upload`;
        fetch('upload', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken') // getCookie는 아래에 정의됨
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.flag == '0') {
                $('.fileUpload-msg').css({'color': 'red'});
                $('.fileUpload-msg').html(data.message);
            } else {
                $('#header_profile_img').attr('src', data.image_url);
                $('#profile_img').attr('src', data.image_url);
                $('#profile_img_2').attr('src', data.image_url);
            }
            $(".backL").css("display", "none");
            // location.href = '/auth/mypage/';
        })
        .catch((error) => {
            console.error('Error:', error);
            $(".backL").css("display", "none");
        });
    });


    document.getElementById('redirectAndClick').addEventListener('click', function() {
        window.location.href = `${window.location.protocol}//${window.location.host}/auth/login/?autoClick=true`;
    });

    // header 스크롤 구현
    var didScroll;
    var lastScrollTop = 0;
    var delta = 5; // 동작의 구현이 시작되는 위치
    var navbarHeight = $('header').outerHeight(); // 영향을 받을 요소를 선택

    // 스크롤시에 사용자가 스크롤했다는 것을 알림
    $(window).scroll(function(event){
        didScroll = true;
    });

    // hasScrolled()를 실행하고 didScroll 상태를 재설정
    setInterval(function() {
        if (didScroll) {
            hasScrolled();
            didScroll = false;
        }
    }, 250);

    // 동작을 구현
    function hasScrolled() {
        // 접근하기 쉽게 현재 스크롤의 위치를 저장한다.
        var st = $(this).scrollTop();
        
        // 설정한 delta 값보다 더 스크롤되었는지를 확인한다.
        if(Math.abs(lastScrollTop - st) <= delta){
            return;
        }
        
        // 헤더의 높이보다 더 스크롤되었는지 확인하고 스크롤의 방향이 위인지 아래인지를 확인한다.
        if (st > lastScrollTop && st > navbarHeight){
            // Scroll Down
            $('header').removeClass('nav-down').addClass('nav-up');
            $('#mypage').removeClass('nav-up').addClass('nav-down');
            $('#mypage_nav').removeClass('nav-up').addClass('nav-down');
        } else {
            // Scroll Up
            if(st + $(window).height() < $(document).height()) {
            $('header').removeClass('nav-up').addClass('nav-down');
            $('#mypage').removeClass('nav-down').addClass('nav-up');
            $('#mypage_nav').removeClass('nav-down').addClass('nav-up');
                
            }
        }
        
        // lastScrollTop 에 현재 스크롤위치를 지정한다.
        lastScrollTop = st;
    }

    $('.checkbox-circle-btn').click(function() {
        if ($(this).hasClass('checked')) {
            $(this).removeClass('checked');
        } else {   
            $(this).addClass('checked');
        }
    });
    
    $('#profile_nick_btns').on('click', '.nickname-change-btn', function(){
        $(this).removeClass('nickname-change-btn').addClass('nickname-duplicate-btn').text('중복확인');
        $('.nickname-value').hide();
        $('.nickname-input').show();
        $('.nickname-error-msg').text('동일한 닉네임입니다.');
        if ($('.nickname-cancel-btn').length === 0) {
            $('#profile_nick_btns').append('<div class="nickname-cancel-btn" style="margin-left: 5px;">취소</div>');
        }
    });

    $('#profile_nick_btns').on('click', '.nickname-cancel-btn', function(){
        $('.nickname-save-btn').removeClass('nickname-save-btn').addClass('nickname-change-btn').text('닉네임 변경');
        $('.nickname-duplicate-btn').removeClass('nickname-duplicate-btn').addClass('nickname-change-btn').text('닉네임 변경');
        $('.nickname-input').hide().attr('readonly', false).val($('.nickname-value').text()).css({'border-bottom': '2px solid red'});
        $('.nickname-value').show();
        $('.nickname-error-msg').text('').css({'color': 'red'});
        $(this).remove();
    });

    $('#profile_nick_btns').on('click', '.nickname-duplicate-btn', function(){
        let $nickname = $('#member_nickname').val();
        if (!nicknameRegEx.test($nickname) || $nickname == $('.nickname-value').text()) {
            return false;
        }
        var data = {nicknameAJAX: $nickname};
        var datastr = JSON.stringify(data);
        
        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4) {
                var data = xhr.responseText;
                var obj = JSON.parse(data);
                if(obj.flag == '0') {
                    $('.nickname-error-msg').text(obj.result_msg);
                } else {
                    $('.nickname-duplicate-btn').removeClass('nickname-duplicate-btn').addClass('nickname-save-btn').text('변경');
                    $('.nickname-input').attr('readonly', true);
                    $('.nickname-error-msg').css({'color': 'black'}).text(obj.result_msg);
                }
            }
        };
        xhr.open("POST", "nickname_duplicate");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(datastr);
    });

    $('#profile_nick_btns').on('click', '.nickname-save-btn', function(){
        let $nickname = $('#member_nickname').val();
        if (!nicknameRegEx.test($nickname) || $nickname == $('.nickname-value').text()) {
            return false;
        }
        var data = {nicknameAJAX: $nickname};
        var datastr = JSON.stringify(data);
        
        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4) {
                var data = xhr.responseText;
                var obj = JSON.parse(data);
                if(obj.flag == '0') {
                    $('.nickname-error-msg').text(obj.result_msg);
                } else {
                    $('.nickname-save-btn').removeClass('nickname-save-btn').addClass('nickname-change-btn').text('닉네임 변경');
                    $('.nickname-input').hide().attr('readonly', false).val(obj.new_nickname).css({'border-bottom': '2px solid red'});
                    $('.nickname-value').show().text(obj.new_nickname);
                    $('.nickname-error-msg').css({'color': 'black'}).text(obj.result_msg);
                    $('.main-nickname').text(obj.new_nickname);
                    $('.nickname-cancel-btn').remove();
                }
            }
        };
        xhr.open("POST", "nickname_save");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(datastr);
    });

    $('#left-btns').on('click', '.profile-change-btn', function(){
        $(this).removeClass('profile-change-btn').addClass('profile-save-btn').text('저장');
        $('.info-value').hide();
        $('.info-input').show();
        if ($('.profile-cancel-btn').length === 0) {
            $('#left-btns').append('<div class="profile-cancel-btn" style="margin-left: 20px;">취소</div>');
        }
    });

    $('#left-btns').on('click', '.profile-cancel-btn', function(){
        $('.profile-save-btn').removeClass('profile-save-btn').addClass('profile-change-btn').text('변경');
        $('#member_realname').val($('.realname').text());
        $('#member_phonenumber').val($('.phonenumber').text());
        $('#member_birth').val($('.birth').text());
        $('#member_nikeid').val($('.nikeid').text());
        $('.info-subject').css({'color': 'black'});
        $('.info-input-error-msg').text('');
        $('.info-input').css({'border-bottom': '1px solid #F5F5F5'});
        $('.info-input').hide();
        $('.info-value').show();
        $(this).remove();
    });

    $('#left-btns').on('click', '.profile-save-btn', function(){
        let $realname = $('#member_realname').val();
        let $phonenumber = $('#member_phonenumber').val();
        let $birth = $('#member_birth').val(); 
        let $nikeid = $('#member_nikeid').val();
        if (!nameRegEx.test($realname) || !phonenumberRegEx.test($phonenumber) || !birthRegEx.test($birth) || !nikeidRegEx.test($nikeid)) {
            return false;
        }
        var data = {realnameAJAX: $realname, phonenumberAJAX: $phonenumber, birthAJAX: $birth, nikeidAJAX: $nikeid};
        var datastr = JSON.stringify(data);
        
        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4) {
                var data = xhr.responseText;
                var obj = JSON.parse(data);
                if(obj.flag == '0') {
                    alert(obj.result_msg);
                } else {
                    alert(obj.result_msg);
                    $('.profile-save-btn').removeClass('profile-save-btn').addClass('profile-change-btn').text('변경');
                    $('.info-input').hide();
                    $('.info-value').show();
                    $('.profile-cancel-btn').remove();
                    $('.realname').text(obj.memberrealname)
                    $('.phonenumber').text(obj.memberphonenumber);
                    $('.birth').text(obj.memberbirth);
                    $('.nikeid').text(obj.membernikeid);
                }
            }
        };
        xhr.open("POST", "member_update");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(datastr);
    });

    // 이름 정규식
    const nameRegEx = /^[가-힣]{2,10}$/;

    $("#member_realname").keyup(function() {
        let $name = $('#member_realname').val();
        if (!nameRegEx.test($name)) {
            $(this).next().text('2 ~ 10자로 입력해주세요.')
            $(this).css({'border-bottom': '2px solid red'});
            $(this).prev().prev().css({'color': 'red'});
        } else {
            $(this).next().text('')
            $(this).css({'border-bottom': '2px solid black'});
            $(this).prev().prev().css({'color': 'black'});
        }
        if ($name.length == 0) {
            $(this).next().text('')
            $(this).css({'border-bottom': '2px solid black'});
            $(this).prev().prev().css({'color': 'black'});
        }

    });

    // name focus
    $('#member_realname').focus(function() {
        let $name = $('#member_realname').val();
        if (!nameRegEx.test($name)) {
            $(this).css({'border-bottom': '2px solid red'});
        } else {
            $(this).css({'border-bottom': '2px solid black'});
        }
        if ($name.length == 0) {
            $(this).next().text('')
            $(this).css({'border-bottom': '2px solid black'});
            $(this).prev().prev().css({'color': 'black'});
        }
    });

    $('#member_realname').blur(function() {
        let $name = $('#member_realname').val();
        if (!nameRegEx.test($name)) {
            $(this).css({'border-bottom': '1px solid red'});
        } else {
            $(this).css({'border-bottom': '1px solid #F5F5F5'});
        }
        if ($name.length == 0) {
            $(this).next().text('')
            $(this).css({'border-bottom': '1px solid #F5F5F5'});
            $(this).prev().prev().css({'color': 'black'});
        }
    });

    // 전화번호 정규식
    const phonenumberRegEx = /\d{11}/;

    $("#member_phonenumber").keyup(function() {
        let $phonenumber = $('#member_phonenumber').val();
        if (!phonenumberRegEx.test($phonenumber)) {
            $(this).next().text('전화번호 11자리를 입력해주세요. ( - 하이픈 제외)')
            $(this).css({'border-bottom': '2px solid red'});
            $(this).prev().prev().css({'color': 'red'});
        } else {
            $(this).next().text('')
            $(this).css({'border-bottom': '2px solid black'});
            $(this).prev().prev().css({'color': 'black'});
        }
        if ($phonenumber.length == 0) {
            $(this).next().text('')
            $(this).css({'border-bottom': '2px solid black'});
            $(this).prev().prev().css({'color': 'black'});
        }

    });

    // phonenumber focus
    $('#member_phonenumber').focus(function() {
        let $phonenumber = $('#member_phonenumber').val();
        if (!phonenumberRegEx.test($phonenumber)) {
            $(this).css({'border-bottom': '2px solid red'});
        } else {
            $(this).css({'border-bottom': '2px solid black'});
        }
        if ($phonenumber.length == 0) {
            $(this).next().text('')
            $(this).css({'border-bottom': '2px solid black'});
            $(this).prev().prev().css({'color': 'black'});
        }
    });

    $('#member_phonenumber').blur(function() {
        let $phonenumber = $('#member_phonenumber').val();
        if (!phonenumberRegEx.test($phonenumber)) {
            $(this).css({'border-bottom': '1px solid red'});
        } else {
            $(this).css({'border-bottom': '1px solid #F5F5F5'});
        }
        if ($phonenumber.length == 0) {
            $(this).next().text('')
            $(this).css({'border-bottom': '1px solid #F5F5F5'});
            $(this).prev().prev().css({'color': 'black'});
        }
    });

    // 생일 정규식
    const birthRegEx = /([0-9]{2}(0[1-9]|1[0-2])(0[1-9]|[1,2][0-9]|3[0,1]))/;

    $("#member_birth").keyup(function() {
        let $birth = $('#member_birth').val();
        if (!birthRegEx.test($birth)) {
            $(this).next().text('생년월일 6자리를 입력해주세요.')
            $(this).css({'border-bottom': '2px solid red'});
            $(this).prev().prev().css({'color': 'red'});
        } else {
            $(this).next().text('')
            $(this).css({'border-bottom': '2px solid black'});
            $(this).prev().prev().css({'color': 'black'});
        }
        if ($birth.length == 0) {
            $(this).next().text('')
            $(this).css({'border-bottom': '2px solid black'});
            $(this).prev().prev().css({'color': 'black'});
        }

    });

    // birth focus
    $('#member_birth').focus(function() {
        let $birth = $('#member_birth').val();
        if (!birthRegEx.test($birth)) {
            $(this).css({'border-bottom': '2px solid red'});
        } else {
            $(this).css({'border-bottom': '2px solid black'});
        }
        if ($birth.length == 0) {
            $(this).next().text('')
            $(this).css({'border-bottom': '2px solid black'});
            $(this).prev().prev().css({'color': 'black'});
        }
    });

    $('#member_birth').blur(function() {
        let $birth = $('#member_birth').val();
        if (!birthRegEx.test($birth)) {
            $(this).css({'border-bottom': '1px solid red'});
        } else {
            $(this).css({'border-bottom': '1px solid #F5F5F5'});
        }
        if ($birth.length == 0) {
            $(this).next().text('')
            $(this).css({'border-bottom': '1px solid #F5F5F5'});
            $(this).prev().prev().css({'color': 'black'});
        }
    });

    // 나이키id 정규식
    const nikeidRegEx = /^[A-Za-z0-9]([-_.]?[A-Za-z0-9])*@[A-Za-z0-9]([-_.]?[A-Za-z0-9])*\.[A-Za-z]{2,3}$/i;

    $("#member_nikeid").keyup(function() {
        let $nikeid = $('#member_nikeid').val();
        if (!nikeidRegEx.test($nikeid)) {
            $(this).next().text('이메일 형식이 아닙니다.')
            $(this).css({'border-bottom': '2px solid red'});
            $(this).prev().prev().css({'color': 'red'});
        } else {
            $(this).next().text('')
            $(this).css({'border-bottom': '2px solid black'});
            $(this).prev().prev().css({'color': 'black'});
        }
        if ($nikeid.length == 0) {
            $(this).next().text('')
            $(this).css({'border-bottom': '2px solid black'});
            $(this).prev().prev().css({'color': 'black'});
        }

    });

    // nikeid focus
    $('#member_nikeid').focus(function() {
        let $nikeid = $('#member_nikeid').val();
        if (!nikeidRegEx.test($nikeid)) {
            $(this).css({'border-bottom': '2px solid red'});
        } else {
            $(this).css({'border-bottom': '2px solid black'});
        }
        if ($nikeid.length == 0) {
            $(this).next().text('')
            $(this).css({'border-bottom': '2px solid black'});
            $(this).prev().prev().css({'color': 'black'});
        }
    });

    $('#member_nikeid').blur(function() {
        let $nikeid = $('#member_nikeid').val();
        if (!nikeidRegEx.test($nikeid)) {
            $(this).css({'border-bottom': '1px solid red'});
        } else {
            $(this).css({'border-bottom': '1px solid #F5F5F5'});
        }
        if ($nikeid.length == 0) {
            $(this).next().text('')
            $(this).css({'border-bottom': '1px solid #F5F5F5'});
            $(this).prev().prev().css({'color': 'black'});
        }
    });

    // 닉네임 정규식
    const nicknameRegEx = /^([a-zA-Z0-9ㄱ-ㅎ|ㅏ-ㅣ|가-힣]).{1,20}$/;

    $("#member_nickname").keyup(function() {
        let $nickname = $('#member_nickname').val();
        if (!nicknameRegEx.test($nickname)) {
            $(this).next().text('한글, 영문, 숫자를 조합해서 입력해주세요. (2-20자)')
            $(this).css({'border-bottom': '2px solid red'});
            // $(this).prev().prev().css({'color': 'red'});
        } else {
            $(this).next().text('')
            $(this).css({'border-bottom': '2px solid black'});
            // $(this).prev().prev().css({'color': 'black'});
        }
        if ($nickname.length == 0) {
            $(this).next().text('')
            $(this).css({'border-bottom': '2px solid black'});
            // $(this).prev().prev().css({'color': 'black'});
        }

        if ($nickname == $('.nickname-value').text()) {
            $(this).next().text('동일한 닉네임입니다.');
            $(this).css({'border-bottom': '2px solid red'});
        }

    });

    // nickname focus
    $('#member_nickname').focus(function() {
        let $nickname = $('#member_nickname').val();
        if (!nicknameRegEx.test($nickname)) {
            $(this).css({'border-bottom': '2px solid red'});
        } else {
            $(this).css({'border-bottom': '2px solid black'});
        }
        if ($nickname.length == 0) {
            $(this).next().text('')
            $(this).css({'border-bottom': '2px solid black'});
            // $(this).prev().prev().css({'color': 'black'});
        }
        if ($nickname == $('.nickname-value').text()) {
            $(this).css({'border-bottom': '2px solid red'});
        }
    });

    $('#member_nickname').blur(function() {
        let $nickname = $('#member_nickname').val();
        if (!nicknameRegEx.test($nickname)) {
            $(this).css({'border-bottom': '1px solid red'});
        } else {
            $(this).css({'border-bottom': '1px solid #F5F5F5'});
        }
        if ($nickname.length == 0) {
            $(this).next().text('')
            $(this).css({'border-bottom': '1px solid #F5F5F5'});
            // $(this).prev().prev().css({'color': 'black'});
        }
        if ($nickname == $('.nickname-value').text()) {
            $(this).css({'border-bottom': '1px solid red'});
        }
    });

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

// 새로운 회원정보수정 방식
function updateMember() {
    membernickname = document.getElementById("member_nickname").value;
    if(membernickname == "") {
        document.getElementById("member_nickname").focus();
        return false;
    }

    memberphonenumber = document.getElementById("member_phonenumber").value;
    if(memberphonenumber == "") {
        document.getElementById("member_phonenumber").focus();
        return false;
    }

    membernikeid = document.getElementById("member_nikeid").value;
    if(membernikeid == "") {
        document.getElementById("member_nikeid").focus();
        return false;
    }

    memberbirth = document.getElementById("member_birth").value;
    if(memberbirth == "") {
        document.getElementById("member_birth").focus();
        return false;
    }


    var strurl = "member_update?member_nickname=" + membernickname + "&member_phonenumber=" + memberphonenumber + "&member_nikeid=" + membernikeid + "&member_birth=" + memberbirth;

    var data = { member_nickname: membernickname, member_phonenumber: memberphonenumber, member_nikeid: membernikeid, member_birth: memberbirth};
    var datastr = JSON.stringify(data);

    xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            var data = xhr.responseText;

            var obj = JSON.parse(data);
            alert(obj.result_msg);
            if(obj.flag == "0"){
                location.href = "/";
            }
        }
    };
    xhr.open("POST", "/auth/mypage/member_update");
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.send(datastr);
}
