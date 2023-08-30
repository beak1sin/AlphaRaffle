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
            $(".backL").css("display", "none");
            return false;
        }
    
        memberpwd = document.getElementById("member_loginpwd").value;
        if(!passwordRegEx.test(memberpwd)) {
            $('.password-error-box').html('비밀번호를 입력하세요.');
            document.getElementById("member_loginpwd").focus();
            $(".backL").css("display", "none");
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
                    location.href = "/main/";
                }
                else {
                    $('.error-box').html(obj.result_msg);
                    $('#member_loginid').focus();
                    if(obj.inactive == "1") {
                        $('.email-resend-msg').html('인증메일을 못받으셨다면 재전송 버튼을 누르신 후 다시 인증해주시기 바랍니다.<a id="resend_mail" style="font-size: 12px;  margin-left: 10px; color: #202020; border-bottom: 1px solid #202020; cursor: pointer;">재전송</a>');
                        $('#resend_mail').attr('data-value', memberid);

                        $('#resend_mail').click(function() {
                            $(".backL").css("display", "");
                            let memberid = $('#resend_mail').attr('data-value')

                            var data = { member_id: memberid};
                            var datastr = JSON.stringify(data);
                            
                            xhr = new XMLHttpRequest();
                            xhr.onreadystatechange = function() {
                                if (xhr.readyState == 4) {
                                    var data = xhr.responseText;
                        
                                    var obj = JSON.parse(data);
                                    if(obj.flag == "1"){
                                        $('.email-resend-complete-msg').html(obj.result_msg);
                                    }
                                    $(".backL").css("display", "none");
                                }
                            };
                            xhr.open("POST", "resend_mail");
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                            xhr.send(datastr);
                        });
                    }
                }
                $(".backL").css("display", "none");
            }
        };
        xhr.open("POST", "/member_login");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(datastr);
    
    });

    $('#resend_mail').click(function() {
        let memberid = $('#resend_mail').attr('data-value')
        console.log(memberid);
        // return false;
        // var data = { member_id: memberid};
        // var datastr = JSON.stringify(data);
        
        // xhr = new XMLHttpRequest();
        // xhr.onreadystatechange = function() {
        //     if (xhr.readyState == 4) {
        //         var data = xhr.responseText;
    
        //         var obj = JSON.parse(data);
        //         if(obj.flag == "0"){
        //             location.href = "/main/";
        //         }
        //         else {
        //             $('.error-box').html(obj.result_msg);
        //             $('#member_loginid').focus();
        //             if(obj.inactive == "1") {
        //                 $('.email-resend-msg').html('인증메일을 못받으셨다면 재전송 버튼을 누르신 후 다시 인증해주시기 바랍니다.<a id="resend_mail" style="font-size: 12px;  margin-left: 10px; color: #202020; border-bottom: 1px solid #202020; cursor: pointer;">재전송</a>');
        //                 $('#resend_mail').attr('data-value', memberid);
        //             }
        //         }
        //         $(".backL").css("display", "none");
        //     }
        // };
        // xhr.open("POST", "auth/login/send_mail");
        // xhr.setRequestHeader("X-CSRFToken", csrftoken);
        // xhr.send(datastr);
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

    $('.auth-next-btn').click(function() {
        $('.password-forgot-box').hide();
        $('.password-forgot-box-2').show();
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

    // new_password focus
    $("#new_password").keyup( () => {
        let $pwd = $('#new_password').val();
        if (!passwordRegEx.test($pwd)) {
            $('.password-forgot-error-box').html('영문, 숫자, 특수문자를 조합해서 입력해주세요. (8-20자)');
            $('.password-forgot-input-box').css({'border-bottom': '2px solid red'});
            $('.password-forgot-title').css({'color': 'red'});
        } else {
            $('.password-forgot-error-box').html('');
            $('.password-forgot-input-box').css({'border-bottom': '2px solid black'});
            $('.password-forgot-title').css({'color': 'black'});
        }
        if ($pwd.length == 0) {
            $('.password-forgot-error-box').html('');
            $('.password-forgot-input-box').css({'border-bottom': '2px solid black'});
            $('.password-forgot-title').css({'color': 'black'});
        }
    });

    $('#new_password').focus( (e) => {
        let $pwd = $('#new_password').val();
        const value = $(e.target).parent();
        if (!passwordRegEx.test($pwd)) {
            value.css({'border-bottom': '2px solid red'});
        } else {
            value.css({'border-bottom': '2px solid black'});
            
        }
        if ($pwd.length == 0) {
            $('.password-forgot-error-box').html('');
            $('.password-forgot-input-box').css({'border-bottom': '2px solid black'});
            $('.password-forgot-title').css({'color': 'black'});
        }

        
    });

    $('#new_password').blur( (e) => {
        let $pwd = $('#new_password').val();
        const value = $(e.target).parent();
        if (!passwordRegEx.test($pwd)) {
            value.css({'border-bottom': '1px solid red'});
        } else {
            value.css({'border-bottom': '1px solid #F5F5F5'});
        }
        if ($pwd.length == 0) {
            $('.password-forgot-error-box').html('');
            $('.password-forgot-input-box').css({'border-bottom': '1px solid #F5F5F5'});
            $('.password-forgot-title').css({'color': 'black'});
        }
    });

    $('#password_close_btn').click( () => {
        $('.password-forgot-error-box').html('');
        $('.password-forgot-input-box').css({'border-bottom': '1px solid #F5F5F5'});
        $('.password-forgot-title').css({'color': 'black'});
    });

    // new_password_2 focus
    $("#new_password_2").keyup( () => {
        let $pwd = $('#new_password').val();
        let $pwd2 = $('#new_password_2').val();
        if ($pwd != $pwd2) {
            $('.password-forgot-error-box-2').html('비밀번호가 일치하지 않습니다.');
            $('.password-forgot-input-box-2').css({'border-bottom': '2px solid red'});
            $('.password-forgot-title-2').css({'color': 'red'});
            $('.new-password-btn').removeClass('abled');
            $('.new-password-btn').addClass('disabled');
            $('.new-password-btn').attr('disabled', true);
        } else {
            $('.password-forgot-error-box-2').html('');
            $('.password-forgot-input-box-2').css({'border-bottom': '2px solid black'});
            $('.password-forgot-title-2').css({'color': 'black'});
            $('.new-password-btn').removeClass('disabled');
            $('.new-password-btn').addClass('abled');
            $('.new-password-btn').attr('disabled', false);
        }
        if ($pwd2.length == 0) {
            $('.password-forgot-error-box-2').html('');
            $('.password-forgot-input-box-2').css({'border-bottom': '2px solid black'});
            $('.password-forgot-title-2').css({'color': 'black'});
            $('.new-password-btn').removeClass('abled');
            $('.new-password-btn').addClass('disabled');
            $('.new-password-btn').attr('disabled', true);
        }
    });

    $('#new_password_2').focus( (e) => {
        let $pwd = $('#new_password').val();
        let $pwd2 = $('#new_password_2').val();
        const value = $(e.target).parent();
        if ($pwd != $pwd2) {
            value.css({'border-bottom': '2px solid red'});
            $('.new-password-btn').removeClass('abled');
            $('.new-password-btn').addClass('disabled');
            $('.new-password-btn').attr('disabled', true);
        } else {
            value.css({'border-bottom': '2px solid black'});
            $('.new-password-btn').removeClass('disabled');
            $('.new-password-btn').addClass('abled');
            $('.new-password-btn').attr('disabled', false);
            
        }
        if ($pwd2.length == 0) {
            $('.password-forgot-error-box-2').html('');
            $('.password-forgot-input-box-2').css({'border-bottom': '2px solid black'});
            $('.password-forgot-title-2').css({'color': 'black'});
            $('.new-password-btn').removeClass('abled');
            $('.new-password-btn').addClass('disabled');
            $('.new-password-btn').attr('disabled', true);
        }

        
    });

    $('#new_password_2').blur( (e) => {
        let $pwd = $('#new_password').val();
        let $pwd2 = $('#new_password_2').val();
        const value = $(e.target).parent();
        if ($pwd != $pwd2) {
            value.css({'border-bottom': '1px solid red'});
            $('.new-password-btn').removeClass('abled');
            $('.new-password-btn').addClass('disabled');
            $('.new-password-btn').attr('disabled', true);
        } else {
            value.css({'border-bottom': '1px solid #F5F5F5'});
            $('.new-password-btn').removeClass('disabled');
            $('.new-password-btn').addClass('abled');
            $('.new-password-btn').attr('disabled', false);
        }
        if ($pwd2.length == 0) {
            $('.password-forgot-error-box-2').html('');
            $('.password-forgot-input-box-2').css({'border-bottom': '1px solid #F5F5F5'});
            $('.password-forgot-title-2').css({'color': 'black'});
            $('.new-password-btn').removeClass('abled');
            $('.new-password-btn').addClass('disabled');
            $('.new-password-btn').attr('disabled', true);
        }
    });

    $('#password_close_btn_2').click( () => {
        $('.password-forgot-error-box-2').html('');
        $('.password-forgot-input-box-2').css({'border-bottom': '1px solid #F5F5F5'});
        $('.password-forgot-title-2').css({'color': 'black'});
        $('.new-password-btn').removeClass('abled');
        $('.new-password-btn').addClass('disabled');
        $('.new-password-btn').attr('disabled', true);
    });

    // 인증번호 전송
    $('#auth_send_btn').click( () => {
        $(".backL").css("display", "");
        var memberidcheck = document.getElementById("member_loginid_forgot").value;

        var data = { member_id: memberidcheck};
        var datastr = JSON.stringify(data);
        
        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                var data = xhr.responseText;
    
                var obj = JSON.parse(data);
                if(obj.flag == "1"){
                    $('#auth').attr('readonly', false);
                    $('#auth').focus();
                    $('.auth-send-btn').removeClass('abled');
                    $('.auth-send-btn').addClass('disabled');
                    $('.auth-send-btn').attr('disabled', true);
                    $("#member_loginid_forgot").attr("readonly",true);
                    $("#member_loginid_forgot").addClass("complete");
                    $('.email-forgot-error-box').html('인증번호를 전송했습니다.');
                    $('#email_forgot_close_btn').removeClass('active');
                    $('#auth_send_btn').text('05:00')
                    startCountdown();
                } else {
                    $('.email-forgot-error-box').html('존재하지 않는 이메일입니다.');
                }
                $(".backL").css("display", "none");
            }
        };
        xhr.open("POST", "/auth_forgot_id");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(datastr);
    
    });

    let countdownInterval;

    function startCountdown() {
        let minutes = 5;
        let seconds = 0;
        
        clearInterval(countdownInterval);  // 기존의 카운트다운 인터벌을 제거
        countdownInterval = setInterval(() => {
            if (seconds === 0) {
                if (minutes === 0) {
                    clearInterval(countdownInterval);
                } else {
                    minutes--;
                    seconds = 59;
                }
            } else {
                seconds--;
            }
            $('#auth_send_btn').text(`${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`);
        }, 1000);
    }

    // 인증번호 재전송
    $('#auth_re_send_btn').click( () => {
        if ($('#auth_send_btn').hasClass('disabled')) {
            $(".backL").css("display", "");
            var memberidcheck = document.getElementById("member_loginid_forgot").value;

            var data = { member_id: memberidcheck};
            var datastr = JSON.stringify(data);
            
            xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4) {
                    var data = xhr.responseText;
        
                    var obj = JSON.parse(data);
                    if(obj.flag == "1"){
                        // $('#auth').attr('readonly', false);
                        $('#auth').focus();
                        // $('.auth-send-btn').removeClass('abled');
                        // $('.auth-send-btn').addClass('disabled');
                        // $('.auth-send-btn').attr('disabled', true);
                        // $("#member_loginid_forgot").attr("readonly",true);
                        // $("#member_loginid_forgot").addClass("complete");
                        $('.email-forgot-error-box').html('인증번호를 재전송했습니다.');
                        $('.auth-error-box').html('');
                        // $('#email_forgot_close_btn').removeClass('active');
                        $('#auth_send_btn').text('05:00')
                        startCountdown();
                    } else {
                        alert(obj.result_msg);
                    }
                    $(".backL").css("display", "none");
                }
            };
            xhr.open("POST", "/auth_forgot_id");
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            xhr.send(datastr);
        } else {
            $('.email-forgot-error-box').html('이메일을 입력하지 않았습니다.');
        }
    });

    // 인증번호 확인
    $('#auth_btn').click( () => {
        $(".backL").css("display", "");
        var code = document.getElementById("auth").value;

        var data = { code: code};
        var datastr = JSON.stringify(data);
        
        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                var data = xhr.responseText;
    
                var obj = JSON.parse(data);
                if(obj.flag == "1"){
                    $('.auth-btn').removeClass('abled');
                    $('.auth-btn').addClass('disabled');
                    $('.auth-btn').attr('disabled', true);
                    $("#auth").attr("readonly",true);
                    $("#auth").addClass("complete");
                    $('#auth_close_btn').removeClass('active');
                    $('.auth-next-btn').removeClass('disabled');
                    $('.auth-next-btn').addClass('abled');
                    $('.auth-error-box').html('인증완료');
                    $('.auth-next-btn').attr('disabled', false);
                } else {
                    $('.auth-error-box').html('인증실패');
                }
                $(".backL").css("display", "none");
            }
        };
        xhr.open("POST", "/verification");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(datastr);
    
    });

    // 비밀번호 변경
    $('#new_password_btn').click( () => {
        $(".backL").css("display", "");
        let memberid = document.getElementById("member_loginid_forgot").value;
        let $pwd = $('#new_password').val();
        let $pwd2 = $('#new_password_2').val();
        if ($pwd != $pwd2) {
            $(".backL").css("display", "none");
            return false;
        }
        let pwdencrypted = hex_sha1($pwd);

        var data = {memberid: memberid ,pwdencrypted: pwdencrypted};
        var datastr = JSON.stringify(data);
        
        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                var data = xhr.responseText;
    
                var obj = JSON.parse(data);
                if(obj.flag == "1"){
                    location.href = '/auth/login/';
                } else {
                    alert(obj.result_msg);
                }
                $(".backL").css("display", "none");
            }
        };
        xhr.open("POST", "/new_password");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(datastr);
    
    });
    
});