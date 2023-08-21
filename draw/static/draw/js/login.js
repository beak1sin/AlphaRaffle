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

    $('#password_forgot_btn').click(function() {
        $('.login-box').hide()
        $('.password-forgot-box').show();
    });

    // member_loginid_forgot focus
    $("#member_loginid_forgot").keyup( () => {
        let $id = $('#member_loginid_forgot').val();
        if (!emailRegEx.test($id)) {
            $('.email-forgot-error-box').html('이메일 형식이 아닙니다.');
            $('.email-forgot-input-box').css({'border-bottom': '2px solid red'});
            $('.email-forgot-title').css({'color': 'red'});
            $('.auth-send-btn').removeClass('abled');
            $('.auth-send-btn').addClass('disabled');
            $('.auth-send-btn').attr('disabled', true);
        } else {
            $('.email-forgot-error-box').html('');
            $('.email-forgot-input-box').css({'border-bottom': '2px solid black'});
            $('.email-forgot-title').css({'color': 'black'});
            $('.auth-send-btn').removeClass('disabled');
            $('.auth-send-btn').addClass('abled');
            $('.auth-send-btn').attr('disabled', false);
        }
        if ($id.length == 0) {
            $('.email-forgot-error-box').html('');
            $('.email-forgot-input-box').css({'border-bottom': '2px solid black'});
            $('.email-forgot-title').css({'color': 'black'});
        }
    });

    $('#member_loginid_forgot').focus( (e) => {
        let $id = $('#member_loginid_forgot').val();
        const value = $(e.target).parent();
        if (!emailRegEx.test($id)) {
            value.css({'border-bottom': '2px solid red'});
            $('.auth-send-btn').removeClass('abled');
            $('.auth-send-btn').addClass('disabled');
            $('.auth-send-btn').attr('disabled', true);
        } else {
            if (!$(e.target).hasClass('complete')) {
                value.css({'border-bottom': '2px solid black'});
                $('.auth-send-btn').removeClass('disabled');
                $('.auth-send-btn').addClass('abled');
                $('.auth-send-btn').attr('disabled', false);
            }
            
        }
        if ($id.length == 0) {
            $('.email-forgot-error-box').html('');
            $('.email-forgot-input-box').css({'border-bottom': '2px solid black'});
            $('.email-forgot-title').css({'color': 'black'});
        }

        
    });

    $('#member_loginid_forgot').blur( (e) => {
        let $id = $('#member_loginid_forgot').val();
        const value = $(e.target).parent();
        if (!emailRegEx.test($id)) {
            value.css({'border-bottom': '1px solid red'});
            $('.auth-send-btn').removeClass('abled');
            $('.auth-send-btn').addClass('disabled');
            $('.auth-send-btn').attr('disabled', true);
        } else {
            if (!$(e.target).hasClass('complete')) {
                value.css({'border-bottom': '1px solid #F5F5F5'});
                $('.auth-send-btn').removeClass('disabled');
                $('.auth-send-btn').addClass('abled');
                $('.auth-send-btn').attr('disabled', false);
            }
        }
        if ($id.length == 0) {
            $('.email-forgot-error-box').html('');
            $('.email-forgot-input-box').css({'border-bottom': '1px solid #F5F5F5'});
            $('.email-forgot-title').css({'color': 'black'});
        }
    });

    $('#email_forgot_close_btn').click( () => {
        $('.email-forgot-error-box').html('');
        $('.email-forgot-input-box').css({'border-bottom': '1px solid #F5F5F5'});
        $('.email-forgot-title').css({'color': 'black'});
        $('.auth-send-btn').removeClass('abled');
        $('.auth-send-btn').addClass('disabled');
        $('.auth-send-btn').attr('disabled', true);
    });

    // auth focus
    $("#auth").keyup( () => {
        let $id = $('#auth').val();
        if ($id.length != 6) {
            $('.auth-error-box').html('인증번호 6자리를 입력해주세요.');
            $('.auth-input-box').css({'border-bottom': '2px solid red'});
            $('.auth-title').css({'color': 'red'});
            $('.auth-btn').removeClass('abled');
            $('.auth-btn').addClass('disabled');
            $('.auth-btn').attr('disabled', true);
        } else {
            $('.auth-error-box').html('');
            $('.auth-input-box').css({'border-bottom': '2px solid black'});
            $('.auth-title').css({'color': 'black'});
            $('.auth-btn').removeClass('disabled');
            $('.auth-btn').addClass('abled');
            $('.auth-btn').attr('disabled', false);
        }
        if ($id.length == 0) {
            $('.auth-error-box').html('');
            $('.auth-input-box').css({'border-bottom': '2px solid black'});
            $('.auth-title').css({'color': 'black'});
        }
    });

    $('#auth').focus( (e) => {
        let $id = $('#auth').val();
        const value = $(e.target).parent();
        if ($id.length != 6) {
            value.css({'border-bottom': '2px solid red'});
            $('.auth-btn').removeClass('abled');
            $('.auth-btn').addClass('disabled');
            $('.auth-btn').attr('disabled', true);
        } else {
            if (!$(e.target).hasClass('complete')) {
                value.css({'border-bottom': '2px solid black'});
                $('.auth-btn').removeClass('disabled');
                $('.auth-btn').addClass('abled');
                $('.auth-btn').attr('disabled', false);
            }
            
        }
        if ($id.length == 0) {
            $('.auth-error-box').html('');
            $('.auth-input-box').css({'border-bottom': '2px solid black'});
            $('.auth-title').css({'color': 'black'});
        }

        
    });

    $('#auth').blur( (e) => {
        let $id = $('#auth').val();
        const value = $(e.target).parent();
        if ($id.length != 6) {
            value.css({'border-bottom': '1px solid red'});
            $('.auth-btn').removeClass('abled');
            $('.auth-btn').addClass('disabled');
            $('.auth-btn').attr('disabled', true);
        } else {
            if (!$(e.target).hasClass('complete')) {
                value.css({'border-bottom': '1px solid #F5F5F5'});
                $('.auth-btn').removeClass('disabled');
                $('.auth-btn').addClass('abled');
                $('.auth-btn').attr('disabled', false);
            }
        }
        if ($id.length == 0) {
            $('.auth-error-box').html('');
            $('.auth-input-box').css({'border-bottom': '1px solid #F5F5F5'});
            $('.auth-title').css({'color': 'black'});
        }
    });

    $('#auth_close_btn').click( () => {
        $('.auth-error-box').html('');
        $('.auth-input-box').css({'border-bottom': '1px solid #F5F5F5'});
        $('.auth-title').css({'color': 'black'});
        $('.auth-btn').removeClass('abled');
        $('.auth-btn').addClass('disabled');
        $('.auth-btn').attr('disabled', true);
    });

    // 인증번호 전송
    $('#auth_send_btn').click( () => {

        var memberidcheck = document.getElementById("member_loginid_forgot").value;

        var data = { member_id: memberidcheck};
        var datastr = JSON.stringify(data);
        
        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                var data = xhr.responseText;
    
                var obj = JSON.parse(data);
                if(obj.flag == "1"){
                    alert(obj.result_msg);
                    $('#auth').attr('readonly', false);
                    $('#auth').focus();
                    $('.auth-send-btn').removeClass('abled');
                    $('.auth-send-btn').addClass('disabled');
                    $('.auth-send-btn').attr('disabled', true);
                    $("#member_loginid_forgot").attr("readonly",true);
                    $("#member_loginid_forgot").addClass("complete");
                    $('.email-forgot-error-box').html('인증번호를 전송했습니다.');
                    $('#email_forgot_close_btn').removeClass('active');
                } else {
                    alert(obj.result_msg);
                }
            }
        };
        xhr.open("POST", "/auth_forgot_id");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(datastr);
    
    });

    // 인증번호 전송
    $('#auth_btn').click( () => {

        var auth = document.getElementById("auth").value;

        var data = { auth: auth};
        var datastr = JSON.stringify(data);
        
        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                var data = xhr.responseText;
    
                var obj = JSON.parse(data);
                if(obj.flag == "0"){
                    $('.auth-btn').removeClass('abled');
                    $('.auth-btn').addClass('disabled');
                    $('.auth-btn').attr('disabled', true);
                    $("#auth").attr("readonly",true);
                    $("#auth").addClass("complete");
                    $('#auth_close_btn').removeClass('active');
                    $('.auth-next-btn').removeClass('disabled');
                    $('.auth-next-btn').addClass('abled');
                    $('.auth-next-btn').attr('disabled', false);
                } else {
                    alert(obj.result_msg);
                }
            }
        };
        xhr.open("POST", "/auth_forgot_id");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(datastr);
    
    });
    
});