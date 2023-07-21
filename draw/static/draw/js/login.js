$(document).ready( () => {
    
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

    

    // 로그인
    $('.login-btn').click( () => {
        $(".backL").css("display", "");
        memberid = document.getElementById("member_loginid").value;
        if(!emailRegEx.test(memberid)) {
            $('.email-error-box').html('이메일을 입력하세요.');
            document.getElementById("member_loginid").focus();
            return false;
        }
    
        memberpwd = document.getElementById("member_loginpwd").value;
        if(!passwordRegEx.test(memberpwd)) {
            $('.password-error-box').html('비밀번호를 입력하세요.');
            document.getElementById("member_loginpwd").focus();
            return false;
        }
        pwdencrypted = hex_sha1(memberpwd);
    
        var data = { member_loginid: memberid, member_loginpwd: pwdencrypted};
        var datastr = JSON.stringify(data);
        
        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                var data = xhr.responseText;
    
                var obj = JSON.parse(data);
                if(obj.flag == "0"){
                    $(".backL").css("display", "none");
                    location.href = "/main/";
                }
                else {
                    $('.error-box').html(obj.result_msg);
                    $('#member_loginid').focus();
                    if(obj.inactive == "1") {
                        $('.sendmail_btn').show();
                        getid(obj.member_loginid);
                    }
                }
            }
        };
        xhr.open("POST", "/member_login");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(datastr);
    
    });

    // 이메일, 비밀번호 정규식
    // 이메일 형식
    const emailRegEx = /^[A-Za-z0-9]([-_.]?[A-Za-z0-9])*@[A-Za-z0-9]([-_.]?[A-Za-z0-9])*\.[A-Za-z]{2,3}$/i;
    // 영문, 숫자 포함 6~20 자리
    // var passwordRegEx = /^[A-Za-z0-9]{6,20}$/;
    // 영문, 숫자, 특수문자 포함 8~20자리
    const passwordRegEx = /^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,20}$/;


    $("#member_loginid").keyup( () => {
        let $id = $('#member_loginid').val();
        if (!emailRegEx.test($id)) {
            $('.email-error-box').html('이메일 형식이 아닙니다.');
            $('.email-input-box').css({'border-bottom': '2px solid red'});
            $('.email-title').css({'color': 'red'});
        } else {
            $('.email-error-box').html('');
            $('.email-input-box').css({'border-bottom': '2px solid black'});
            $('.email-title').css({'color': 'black'});
        }
        if ($id.length == 0) {
            $('.email-error-box').html('');
            $('.email-input-box').css({'border-bottom': '2px solid black'});
            $('.email-title').css({'color': 'black'});
        }
    });

    $("#member_loginpwd").keyup( (event) => {
        let $pwd = $('#member_loginpwd').val();
        if (!passwordRegEx.test($pwd)) {
            $('.password-error-box').html('영문, 숫자, 특수문자를 조합해서 입력해주세요. (8-20자)');
            // $('.password-error-box').html('영문, 숫자를 조합해서 입력해주세요. (6-20자)');
            $('.password-input-box').css({'border-bottom': '2px solid red'});
            $('.password-title').css({'color': 'red'});
        } else {
            $('.password-error-box').html('');
            $('.password-input-box').css({'border-bottom': '2px solid black'});
            $('.password-title').css({'color': 'black'});
        }
        if ($pwd.length == 0) {
            $('.password-error-box').html('');
            $('.password-input-box').css({'border-bottom': '2px solid black'});
            $('.password-title').css({'color': 'black'});
        }

        if (event.code === 'Enter') {
            $('.login-btn').click();
        }
    });
    

    // 로그인 id focus
    $('#member_loginid').focus( (e) => {
        let $id = $('#member_loginid').val();
        const value = $(e.target).parent();
        if (!emailRegEx.test($id)) {
            value.css({'border-bottom': '2px solid red'});
        } else {
            value.css({'border-bottom': '2px solid black'});
        }
        if ($id.length == 0) {
            $('.email-error-box').html('');
            $('.email-input-box').css({'border-bottom': '2px solid black'});
            $('.email-title').css({'color': 'black'});
        }
    });

    $('#member_loginid').blur( (e) => {
        let $id = $('#member_loginid').val();
        const value = $(e.target).parent();
        if (!emailRegEx.test($id)) {
            value.css({'border-bottom': '1px solid red'});
        } else {
            value.css({'border-bottom': '1px solid #F5F5F5'});
        }
        if ($id.length == 0) {
            $('.email-error-box').html('');
            $('.email-input-box').css({'border-bottom': '1px solid #F5F5F5'});
            $('.email-title').css({'color': 'black'});
        }
    });

    $('#email_close_btn').click( () => {
        $('.email-error-box').html('');
        $('.email-input-box').css({'border-bottom': '1px solid #F5F5F5'});
        $('.email-title').css({'color': 'black'});
    })

    // 로그인 pwd focus
    $('#member_loginpwd').focus( (e) => {
        let $pwd = $('#member_loginpwd').val();
        const value = $(e.target).parent();
        if (!passwordRegEx.test($pwd)) {
            value.css({'border-bottom': '2px solid red'});
        } else {
            value.css({'border-bottom': '2px solid black'});
        }
        if ($pwd.length == 0) {
            $('.password-error-box').html('');
            $('.password-input-box').css({'border-bottom': '2px solid black'});
            $('.password-title').css({'color': 'black'});
        }
    });

    $('#member_loginpwd').blur( (e) => {
        let $pwd = $('#member_loginpwd').val();
        const value = $(e.target).parent();
        if (!passwordRegEx.test($pwd)) {
            value.css({'border-bottom': '1px solid red'});
        } else {
            value.css({'border-bottom': '1px solid #F5F5F5'});
        }
        if ($pwd.length == 0) {
            $('.password-error-box').html('');
            $('.password-input-box').css({'border-bottom': '1px solid #F5F5F5'});
            $('.password-title').css({'color': 'black'});
        }
    });

    $('#password_close_btn').click( () => {
        $('.password-error-box').html('');
        $('.password-input-box').css({'border-bottom': '1px solid #F5F5F5'});
        $('.password-title').css({'color': 'black'});
    })

    
    
});