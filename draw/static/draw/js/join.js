$(document).ready( () => {

    $('.next-btn').click( () => {
        $('.1').hide();
        $('.2').show();
    });

    $('.back-btn').click( () => {
        $('.2').hide();
        $('.1').show();
    });

    $('.next-btn-2').click( () => {
        $('.2').hide();
        $('.3').show();
    });

    $('.back-btn-2').click( () => {
        $('.3').hide();
        $('.2').show();
    });
    
    $('.back-btn-3').click( () => {
        $('.4').hide();
        $('.3').show();
    });

    $('.draw-btn').click( () => {
        location.href='/main/';
    })

      // input focus
    $('.input-focus').focus( (e) => {
        const value = $(e.target).parent();
        value.css({'border-bottom': '2px solid black'});
    });

    $('.input-focus').blur( (e) => {
        const value = $(e.target).parent();
        value.css({'border-bottom': '1px solid #F5F5F5'});
    });

    const emailRegEx = /^[A-Za-z0-9]([-_.]?[A-Za-z0-9])*@[A-Za-z0-9]([-_.]?[A-Za-z0-9])*\.[A-Za-z]{2,3}$/i;
    const passwordRegEx = /^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,20}$/;
    // var passwordRegEx = /^[A-Za-z0-9]{6,20}$/;

    $('#email_close_btn').click( () => {
        $('.email-error-box').html('');
        $('.join-email-input-value-box').css({'border-bottom': '2px solid black'});
        $('.join-email-input-title').css({'color': 'black'});
        $('.duplicate-btn').removeClass('abled');
        $('.duplicate-btn').addClass('disabled');
        $('.duplicate-btn').attr('disabled', true);
    })

    $("#member_id").keyup( () => {
        let $id = $('#member_id').val();
        if (!emailRegEx.test($id)) {
            $('.email-error-box').html('이메일 형식이 아닙니다.');
            $('.join-email-input-value-box').css({'border-bottom': '2px solid red'});
            $('.join-email-input-title').css({'color': 'red'});
            $('.duplicate-btn').removeClass('abled');
            $('.duplicate-btn').addClass('disabled');
            $('.duplicate-btn').attr('disabled', true);
            $('.next-btn').removeClass('abled');
            $('.next-btn').addClass('disabled');
            $('.next-btn').attr('disabled', true);
        } else {
            $('.email-error-box').html('');
            $('.join-email-input-value-box').css({'border-bottom': '2px solid black'});
            $('.join-email-input-title').css({'color': 'black'});
            $('.duplicate-btn').removeClass('disabled');
            $('.duplicate-btn').addClass('abled');
            $('.duplicate-btn').attr('disabled', false);
        }
        if ($id.length == 0) {
            $('.email-error-box').html('');
            $('.join-email-input-value-box').css({'border-bottom': '2px solid black'});
            $('.join-email-input-title').css({'color': 'black'});
        }
    });

    // 로그인 id focus
    $('#member_id').focus( (e) => {
        let $id = $('#member_id').val();
        const value = $(e.target).parent();
        if (!emailRegEx.test($id)) {
            value.css({'border-bottom': '2px solid red'});
        } else {
            value.css({'border-bottom': '2px solid black'});
        }
        if ($id.length == 0) {
            $('.email-error-box').html('');
            $('.join-email-input-value-box').css({'border-bottom': '2px solid black'});
            $('.join-email-input-title').css({'color': 'black'});
        }
    });

    $('#member_id').blur( (e) => {
        let $id = $('#member_id').val();
        const value = $(e.target).parent();
        if (!emailRegEx.test($id)) {
            value.css({'border-bottom': '1px solid red'});
        } else {
            value.css({'border-bottom': '1px solid #F5F5F5'});
        }
        if ($id.length == 0) {
            $('.email-error-box').html('');
            $('.join-email-input-value-box').css({'border-bottom': '1px solid #F5F5F5'});
            $('.join-email-input-title').css({'color': 'black'});
        }
    });

    $("#member_pwd").keyup( (e) => {
        let $pwd = $('#member_pwd').val();
        if (!passwordRegEx.test($pwd)) {
            $('.password-error-box').html('영문, 숫자, 특수문자를 조합해서 입력해주세요. (8-20자)');
            // $('.password-error-box').html('영문, 숫자를 조합해서 입력해주세요. (6-20자)');
            $('.join-password-input-value-box').css({'border-bottom': '2px solid red'});
            $('.join-password-input-title').css({'color': 'red'});
            $('.next-btn-2').removeClass('abled');
            $('.next-btn-2').addClass('disabled');
            $('.next-btn-2').attr('disabled', true);
        } else {
            $('.password-error-box').html('');
            $('.join-password-input-value-box').css({'border-bottom': '2px solid black'});
            $('.join-password-input-title').css({'color': 'black'});
        }
        if ($pwd.length == 0) {
            $('.password-error-box').html('');
            $('.join-password-input-value-box').css({'border-bottom': '2px solid black'});
            $('.join-password-input-title').css({'color': 'black'});
            $('.next-btn-2').removeClass('abled');
            $('.next-btn-2').addClass('disabled');
            $('.next-btn-2').attr('disabled', true);
        }

    });

    // 로그인 pwd focus
    $('#member_pwd').focus( (e) => {
        let $pwd = $('#member_pwd').val();
        const value = $(e.target).parent();
        if (!passwordRegEx.test($pwd)) {
            value.css({'border-bottom': '2px solid red'});
        } else {
            value.css({'border-bottom': '2px solid black'});
        }
        if ($pwd.length == 0) {
            $('.password-error-box').html('');
            $('.join-password-input-value-box').css({'border-bottom': '2px solid black'});
            $('.join-password-input-title').css({'color': 'black'});
        }
    });

    $('#member_pwd').blur( (e) => {
        let $pwd = $('#member_pwd').val();
        const value = $(e.target).parent();
        if (!passwordRegEx.test($pwd)) {
            value.css({'border-bottom': '1px solid red'});
        } else {
            value.css({'border-bottom': '1px solid #F5F5F5'});
        }
        if ($pwd.length == 0) {
            $('.password-error-box').html('');
            $('.join-password-input-value-box').css({'border-bottom': '1px solid #F5F5F5'});
            $('.join-password-input-title').css({'color': 'black'});
        }
    });

    $('#password_close_btn').click( () => {
        $('.password-error-box').html('');
        $('.join-password-input-value-box').css({'border-bottom': '2px solid black'});
        $('.join-password-input-title').css({'color': 'black'});
        $('.next-btn-2').removeClass('abled');
        $('.next-btn-2').addClass('disabled');
        $('.next-btn-2').attr('disabled', true);
    })

    $("#member_pwd2").keyup( (e) => {
        let $pwd = $('#member_pwd').val();
        let $pwd2 = $('#member_pwd2').val();
        if ($pwd != $pwd2) {
            $('.password2-error-box').html('비밀번호가 일치하지 않습니다.');
            $('.join-password2-input-value-box').css({'border-bottom': '2px solid red'});
            $('.join-password2-input-title').css({'color': 'red'});
            $('.next-btn-2').removeClass('abled');
            $('.next-btn-2').addClass('disabled');
            $('.next-btn-2').attr('disabled', true);
        } else {
            $('.password2-error-box').html('');
            $('.join-password2-input-value-box').css({'border-bottom': '2px solid black'});
            $('.join-password2-input-title').css({'color': 'black'});
            $('.next-btn-2').removeClass('disabled');
            $('.next-btn-2').addClass('abled');
            $('.next-btn-2').attr('disabled', false);
        }
        if ($pwd2.length == 0) {
            $('.password2-error-box').html('');
            $('.join-password2-input-value-box').css({'border-bottom': '2px solid black'});
            $('.join-password2-input-title').css({'color': 'black'});
            $('.next-btn-2').removeClass('abled');
            $('.next-btn-2').addClass('disabled');
            $('.next-btn-2').attr('disabled', true);
        }

    });

    // 로그인 pwd2 focus
    $('#member_pwd2').focus( (e) => {
        let $pwd = $('#member_pwd').val();
        let $pwd2 = $('#member_pwd2').val();
        const value = $(e.target).parent();
        if ($pwd != $pwd2) {
            value.css({'border-bottom': '2px solid red'});
        } else {
            value.css({'border-bottom': '2px solid black'});
        }
        if ($pwd2.length == 0) {
            $('.password2-error-box').html('');
            $('.join-password2-input-value-box').css({'border-bottom': '2px solid black'});
            $('.join-password2-input-title').css({'color': 'black'});
        }
    });

    $('#member_pwd2').blur( (e) => {
        let $pwd = $('#member_pwd').val();
        let $pwd2 = $('#member_pwd2').val();
        const value = $(e.target).parent();
        if ($pwd != $pwd2) {
            value.css({'border-bottom': '1px solid red'});
        } else {
            value.css({'border-bottom': '1px solid #F5F5F5'});
        }
        if ($pwd2.length == 0) {
            $('.password2-error-box').html('');
            $('.join-password2-input-value-box').css({'border-bottom': '1px solid #F5F5F5'});
            $('.join-password2-input-title').css({'color': 'black'});
        }
    });

    $('#password2_close_btn').click( () => {
        $('.password2-error-box').html('');
        $('.join-password2-input-value-box').css({'border-bottom': '2px solid black'});
        $('.join-password2-input-title').css({'color': 'black'});
        $('.next-btn-2').removeClass('abled');
        $('.next-btn-2').addClass('disabled');
        $('.next-btn-2').attr('disabled', true);
    })



    // 이름 정규식
    const nameRegEx = /^[가-힣]{2,10}$/;

    $("#member_realname").keyup( (e) => {
        let $name = $('#member_realname').val();
        let targetParent = e.target.parentElement.parentElement;
        
        if (!nameRegEx.test($name)) {
            targetParent.nextElementSibling.childNodes[1].innerText = '2 ~ 10자로 입력해주세요.';
            targetParent.childNodes[3].style.borderBottom = '2px solid red';
            targetParent.childNodes[1].style.color = 'red';
        } else {
            targetParent.nextElementSibling.childNodes[1].innerText = '';
            targetParent.childNodes[3].style.borderBottom = '2px solid black';
            targetParent.childNodes[1].style.color = 'black';
        }
        if ($name.length == 0) {
            targetParent.nextElementSibling.childNodes[1].innerText = '';
            targetParent.childNodes[3].style.borderBottom = '2px solid black';
            targetParent.childNodes[1].style.color = 'black';
        }

    });

    // name focus
    $('#member_realname').focus( (e) => {
        let $name = $('#member_realname').val();
        let targetParent = e.target.parentElement.parentElement;
        if (!nameRegEx.test($name)) {
            targetParent.childNodes[3].style.borderBottom = '2px solid red';
        } else {
            targetParent.childNodes[3].style.borderBottom = '2px solid black';
        }
        if ($name.length == 0) {
            targetParent.nextElementSibling.childNodes[1].innerText = '';
            targetParent.childNodes[3].style.borderBottom = '2px solid black';
            targetParent.childNodes[1].style.color = 'black';
        }
    });

    $('#member_realname').blur( (e) => {
        let $name = $('#member_realname').val();
        let targetParent = e.target.parentElement.parentElement;
        if (!nameRegEx.test($name)) {
            targetParent.childNodes[3].style.borderBottom = '1px solid red';
        } else {
            targetParent.childNodes[3].style.borderBottom = '1px solid #F5F5F5';
        }
        if ($name.length == 0) {
            targetParent.nextElementSibling.childNodes[1].innerText = '';
            targetParent.childNodes[3].style.borderBottom = '1px solid #F5F5F5';
            targetParent.childNodes[1].style.color = 'black';
        }
    });

    $('#name_close_btn').click( (e) => {
        let targetParent = e.target.parentElement.parentElement;
        targetParent.nextElementSibling.childNodes[1].innerText = '';
        targetParent.childNodes[3].style.borderBottom = '2px solid black';
        targetParent.childNodes[1].style.color = 'black';
    })

    // 닉네임 정규식
    const nicknameRegEx = /^([a-zA-Z0-9ㄱ-ㅎ|ㅏ-ㅣ|가-힣]).{1,20}$/;

    $("#member_nickname").keyup( (e) => {
        let $nickname = $('#member_nickname').val();
        let targetParent = e.target.parentElement.parentElement;
        
        if (!nicknameRegEx.test($nickname)) {
            targetParent.nextElementSibling.childNodes[1].innerText = '한글, 영문, 숫자를 조합해서 입력해주세요. (2-20자)';
            targetParent.childNodes[3].style.borderBottom = '2px solid red';
            targetParent.childNodes[1].style.color = 'red';
        } else {
            targetParent.nextElementSibling.childNodes[1].innerText = '';
            targetParent.childNodes[3].style.borderBottom = '2px solid black';
            targetParent.childNodes[1].style.color = 'black';
        }
        if ($nickname.length == 0) {
            targetParent.nextElementSibling.childNodes[1].innerText = '';
            targetParent.childNodes[3].style.borderBottom = '2px solid black';
            targetParent.childNodes[1].style.color = 'black';
        }

    });

    // nickname focus
    $('#member_nickname').focus( (e) => {
        let $nickname = $('#member_nickname').val();
        let targetParent = e.target.parentElement.parentElement;
        if (!nicknameRegEx.test($nickname)) {
            targetParent.childNodes[3].style.borderBottom = '2px solid red';
        } else {
            targetParent.childNodes[3].style.borderBottom = '2px solid black';
        }
        if ($nickname.length == 0) {
            targetParent.nextElementSibling.childNodes[1].innerText = '';
            targetParent.childNodes[3].style.borderBottom = '2px solid black';
            targetParent.childNodes[1].style.color = 'black';
        }
    });

    $('#member_nickname').blur( (e) => {
        let $nickname = $('#member_nickname').val();
        let targetParent = e.target.parentElement.parentElement;
        if (!nicknameRegEx.test($nickname)) {
            targetParent.childNodes[3].style.borderBottom = '1px solid red';
        } else {
            targetParent.childNodes[3].style.borderBottom = '1px solid #F5F5F5';
        }
        if ($nickname.length == 0) {
            targetParent.nextElementSibling.childNodes[1].innerText = '';
            targetParent.childNodes[3].style.borderBottom = '1px solid #F5F5F5';
            targetParent.childNodes[1].style.color = 'black';
        }
    });

    $('#nickname_close_btn').click( (e) => {
        let targetParent = e.target.parentElement.parentElement;
        targetParent.nextElementSibling.childNodes[1].innerText = '';
        targetParent.childNodes[3].style.borderBottom = '2px solid black';
        targetParent.childNodes[1].style.color = 'black';
    })

    // 생일 정규식
    const birthRegEx = /([0-9]{2}(0[1-9]|1[0-2])(0[1-9]|[1,2][0-9]|3[0,1]))/;

    $("#member_birth").keyup( (e) => {
        let $birth = $('#member_birth').val();
        let targetParent = e.target.parentElement.parentElement;
        
        if (!birthRegEx.test($birth)) {
            targetParent.nextElementSibling.childNodes[1].innerText = '생년월일 6자리를 입력해주세요.';
            targetParent.childNodes[3].style.borderBottom = '2px solid red';
            targetParent.childNodes[1].style.color = 'red';
        } else {
            targetParent.nextElementSibling.childNodes[1].innerText = '';
            targetParent.childNodes[3].style.borderBottom = '2px solid black';
            targetParent.childNodes[1].style.color = 'black';
        }
        if ($birth.length == 0) {
            targetParent.nextElementSibling.childNodes[1].innerText = '';
            targetParent.childNodes[3].style.borderBottom = '2px solid black';
            targetParent.childNodes[1].style.color = 'black';
        }

    });

    // birth focus
    $('#member_birth').focus( (e) => {
        let $birth = $('#member_birth').val();
        let targetParent = e.target.parentElement.parentElement;
        if (!birthRegEx.test($birth)) {
            targetParent.childNodes[3].style.borderBottom = '2px solid red';
        } else {
            targetParent.childNodes[3].style.borderBottom = '2px solid black';
        }
        if ($birth.length == 0) {
            targetParent.nextElementSibling.childNodes[1].innerText = '';
            targetParent.childNodes[3].style.borderBottom = '2px solid black';
            targetParent.childNodes[1].style.color = 'black';
        }
    });

    $('#member_birth').blur( (e) => {
        let $birth = $('#member_birth').val();
        let targetParent = e.target.parentElement.parentElement;
        if (!birthRegEx.test($birth)) {
            targetParent.childNodes[3].style.borderBottom = '1px solid red';
        } else {
            targetParent.childNodes[3].style.borderBottom = '1px solid #F5F5F5';
        }
        if ($birth.length == 0) {
            targetParent.nextElementSibling.childNodes[1].innerText = '';
            targetParent.childNodes[3].style.borderBottom = '1px solid #F5F5F5';
            targetParent.childNodes[1].style.color = 'black';
        }
    });

    $('#birth_close_btn').click( (e) => {
        let targetParent = e.target.parentElement.parentElement;
        targetParent.nextElementSibling.childNodes[1].innerText = '';
        targetParent.childNodes[3].style.borderBottom = '2px solid black';
        targetParent.childNodes[1].style.color = 'black';
    })



    // 전화번호 정규식
    const phonenumberRegEx = /\d{11}/;

    $("#member_phonenumber").keyup( (e) => {
        let $phonenumber = $('#member_phonenumber').val();
        let targetParent = e.target.parentElement.parentElement;
        
        if (!phonenumberRegEx.test($phonenumber)) {
            targetParent.nextElementSibling.childNodes[1].innerText = '전화번호 11자리를 입력해주세요. ( - 하이픈 제외)';
            targetParent.childNodes[3].style.borderBottom = '2px solid red';
            targetParent.childNodes[1].style.color = 'red';
        } else {
            targetParent.nextElementSibling.childNodes[1].innerText = '';
            targetParent.childNodes[3].style.borderBottom = '2px solid black';
            targetParent.childNodes[1].style.color = 'black';
        }
        if ($phonenumber.length == 0) {
            targetParent.nextElementSibling.childNodes[1].innerText = '';
            targetParent.childNodes[3].style.borderBottom = '2px solid black';
            targetParent.childNodes[1].style.color = 'black';
        }

    });

    // birth focus
    $('#member_phonenumber').focus( (e) => {
        let $phonenumber = $('#member_phonenumber').val();
        let targetParent = e.target.parentElement.parentElement;
        if (!phonenumberRegEx.test($phonenumber)) {
            targetParent.childNodes[3].style.borderBottom = '2px solid red';
        } else {
            targetParent.childNodes[3].style.borderBottom = '2px solid black';
        }
        if ($phonenumber.length == 0) {
            targetParent.nextElementSibling.childNodes[1].innerText = '';
            targetParent.childNodes[3].style.borderBottom = '2px solid black';
            targetParent.childNodes[1].style.color = 'black';
        }
    });

    $('#member_phonenumber').blur( (e) => {
        let $phonenumber = $('#member_phonenumber').val();
        let targetParent = e.target.parentElement.parentElement;
        if (!phonenumberRegEx.test($phonenumber)) {
            targetParent.childNodes[3].style.borderBottom = '1px solid red';
        } else {
            targetParent.childNodes[3].style.borderBottom = '1px solid #F5F5F5';
        }
        if ($phonenumber.length == 0) {
            targetParent.nextElementSibling.childNodes[1].innerText = '';
            targetParent.childNodes[3].style.borderBottom = '1px solid #F5F5F5';
            targetParent.childNodes[1].style.color = 'black';
        }
    });

    $('#phonenumber_close_btn').click( (e) => {
        let targetParent = e.target.parentElement.parentElement;
        targetParent.nextElementSibling.childNodes[1].innerText = '';
        targetParent.childNodes[3].style.borderBottom = '2px solid black';
        targetParent.childNodes[1].style.color = 'black';
    })

    // 나이키id 정규식
    const nikeidRegEx = /^[A-Za-z0-9]([-_.]?[A-Za-z0-9])*@[A-Za-z0-9]([-_.]?[A-Za-z0-9])*\.[A-Za-z]{2,3}$/i;

    $("#member_nikeid").keyup( (e) => {
        let $nikeid = $('#member_nikeid').val();
        let targetParent = e.target.parentElement.parentElement;
        
        if (!nikeidRegEx.test($nikeid)) {
            targetParent.nextElementSibling.childNodes[1].innerText = '이메일 형식이 아닙니다.';
            targetParent.childNodes[3].style.borderBottom = '2px solid red';
            targetParent.childNodes[1].style.color = 'red';
        } else {
            targetParent.nextElementSibling.childNodes[1].innerText = '';
            targetParent.childNodes[3].style.borderBottom = '2px solid black';
            targetParent.childNodes[1].style.color = 'black';
        }
        if ($nikeid.length == 0) {
            targetParent.nextElementSibling.childNodes[1].innerText = '';
            targetParent.childNodes[3].style.borderBottom = '2px solid black';
            targetParent.childNodes[1].style.color = 'black';
        }

    });

    // nikeid focus
    $('#member_nikeid').focus( (e) => {
        let $nikeid = $('#member_nikeid').val();
        let targetParent = e.target.parentElement.parentElement;
        if (!nikeidRegEx.test($nikeid)) {
            targetParent.childNodes[3].style.borderBottom = '2px solid red';
        } else {
            targetParent.childNodes[3].style.borderBottom = '2px solid black';
        }
        if ($nikeid.length == 0) {
            targetParent.nextElementSibling.childNodes[1].innerText = '';
            targetParent.childNodes[3].style.borderBottom = '2px solid black';
            targetParent.childNodes[1].style.color = 'black';
        }
    });

    $('#member_nikeid').blur( (e) => {
        let $nikeid = $('#member_nikeid').val();
        let targetParent = e.target.parentElement.parentElement;
        if (!nikeidRegEx.test($nikeid)) {
            targetParent.childNodes[3].style.borderBottom = '1px solid red';
        } else {
            targetParent.childNodes[3].style.borderBottom = '1px solid #F5F5F5';
        }
        if ($nikeid.length == 0) {
            targetParent.nextElementSibling.childNodes[1].innerText = '';
            targetParent.childNodes[3].style.borderBottom = '1px solid #F5F5F5';
            targetParent.childNodes[1].style.color = 'black';
        }
    });

    $('#nikeid_close_btn').click( (e) => {
        let targetParent = e.target.parentElement.parentElement;
        targetParent.nextElementSibling.childNodes[1].innerText = '';
        targetParent.childNodes[3].style.borderBottom = '2px solid black';
        targetParent.childNodes[1].style.color = 'black';
    })


    $('#member_id, #member_pwd, #member_realname, #member_nickname, #member_birth, #member_nikeid, #member_phonenumber').keyup( () => {
        memberid = document.getElementById("member_id").value;
        memberpwd = document.getElementById("member_pwd").value;

        memberrealname = document.getElementById("member_realname").value;
        membernickname = document.getElementById("member_nickname").value;
        memberbirth = document.getElementById("member_birth").value;
        membernikeid = document.getElementById("member_nikeid").value;
        memberphonenumber = document.getElementById("member_phonenumber").value;

        if (emailRegEx.test(memberid) && passwordRegEx.test(memberpwd) && nameRegEx.test(memberrealname) && nicknameRegEx.test(membernickname) && birthRegEx.test(memberbirth) && nikeidRegEx.test(membernikeid) && phonenumberRegEx.test(memberphonenumber)) {
            $('.next-btn-3').removeClass('disabled');
            $('.next-btn-3').addClass('abled');
            $('.next-btn-3').attr('disabled', false);
        } else {
            $('.next-btn-3').removeClass('abled');
            $('.next-btn-3').addClass('disabled');
            $('.next-btn-3').attr('disabled', true);
        }
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
    
    // 새로운 회원가입
    $('#join_btn').click( () => {
    
        memberid = document.getElementById("member_id").value;
    
        memberpwd = document.getElementById("member_pwd").value;
    
        pwdencrypted = hex_sha1(memberpwd);
    
        // wflag = document.getElementById("warrantcheck").checked;
        // if(wflag == false) {
        //     Swal.fire({
        //       icon: 'error',
        //       title: '약관에 동의해주세요.',
        //       confirmButtonColor: '#000000',
        //       timer: 2000,
        //       timerProgressBar: true
        //     })
        //     return false;
        // }
    
        memberrealname = document.getElementById("member_realname").value;
        membernickname = document.getElementById("member_nickname").value;
        memberbirth = document.getElementById("member_birth").value;
        membernikeid = document.getElementById("member_nikeid").value;
        memberphonenumber = document.getElementById("member_phonenumber").value;
    
    
        var data = { member_id: memberid, member_pwd: pwdencrypted, member_realname: memberrealname, member_nickname: membernickname, member_birth: memberbirth, member_nikeid: membernikeid, member_phonenumber: memberphonenumber};
        var datastr = JSON.stringify(data);
    
    
        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                var data = xhr.responseText;
    
                var obj = JSON.parse(data);
                if(obj.flag == "1"){
                    $('.3').hide();
                    $('.4').show();
                } else {
                    alert(obj.result_msg);
                }
            }
        };
        xhr.open("POST", "/member_insert");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(datastr);
    });

    // 중복확인
    $('#idcheck_btn').click( () => {

        memberidcheck = document.getElementById("member_id").value;
        // if (!emailRegEx.test(memberidcheck)) {
        //     Swal.fire({
        //     icon: 'error',
        //     title: '이메일 형식이 아닙니다.',
        //     confirmButtonColor: '#000000',
        //     timer: 2000,
        //     timerProgressBar: true
        //     })
        //     document.getElementById("member_id").focus();
        //     return false;
        // }
        // if(memberidcheck == "") {
        //     Swal.fire({
        //     icon: 'error',
        //     title: '아이디가 비어있습니다.',
        //     confirmButtonColor: '#000000',
        //     timer: 2000,
        //     timerProgressBar: true
        //     })
        //     document.getElementById("member_id").focus();
        //     return false;
        // }
    
        var data = { member_id: memberidcheck};
        var datastr = JSON.stringify(data);
        
        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                var data = xhr.responseText;
    
                var obj = JSON.parse(data);
                if(obj.flag == "0"){
                    // $('#member_id').attr('readonly', true);
                    $('.next-btn').removeClass('disabled');
                    $('.next-btn').addClass('abled');
                    $('.next-btn').attr('disabled', false);
                } else {
                    alert(obj.result_msg);
                }
            }
        };
        xhr.open("POST", "/member_idcheck");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(datastr);
    
    });

});