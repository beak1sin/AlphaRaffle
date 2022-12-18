$(document).ready(function() {
    $('.signin_tab').on('click', function() {
        $('.error_box').hide();
        $('#error_message').addClass('hidden');
        $('.login_error_message').addClass('hidden');
        $(this).addClass('active');
        $(this).removeClass('disable');
        $('.signup_tab').addClass('disable');
        $('.signup_tab').removeClass('active');
        $('.signin_box').show();
        $('.signup_box').hide();
    });
    $('.signup_tab').on('click', function() {
        $('.error_box').hide();
        $('#error_message').addClass('hidden');
        $('.login_error_message').addClass('hidden');
        $(this).addClass('active');
        $(this).removeClass('disable');
        $('.signin_tab').addClass('disable');
        $('.signin_tab').removeClass('active');
        $('.signin_box').hide();
        $('.signup_box').show();
    });

});
function validateEmail(email) {
var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
return re.test(email);
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

// 새로운 회원가입
function registerMember() {

    memberid = document.getElementById("member_id").value;
    if(memberid == "") {
        Swal.fire({
          icon: 'error',
          title: '아이디를 입력하세요.',
          confirmButtonColor: '#000000',
          timer: 2000,
          timerProgressBar: true
        })
        document.getElementById("member_id").focus();
        return false;
    }

    memberpwd = document.getElementById("member_pwd").value;
    if(memberpwd == "") {
        document.getElementById("member_pwd").focus();
        return false;
    }

    memberpwd2 = document.getElementById("member_pwd2").value;
    if(memberpwd2 == "") {
        document.getElementById("member_pwd2").focus();
        return false;
    }

    if(memberpwd != memberpwd2) {
        Swal.fire({
          icon: 'error',
          title: '비밀번호 확인이 틀립니다.',
          confirmButtonColor: '#000000',
          timer: 2000,
          timerProgressBar: true
        })
        document.getElementById("member_pwd2").focus();
        return false;
    }

    if(memberpwd.length < 6) {
        Swal.fire({
          icon: 'error',
          title: '6자리 이상이어야 합니다.',
          confirmButtonColor: '#000000',
          timer: 2000,
          timerProgressBar: true
        })
        document.getElementById("member_pwd").focus();
        return false;
    }

    pwdencrypted = hex_sha1(memberpwd);

    wflag = document.getElementById("warrantcheck").checked;
    if(wflag == false) {
        Swal.fire({
          icon: 'error',
          title: '약관에 동의해주세요.',
          confirmButtonColor: '#000000',
          timer: 2000,
          timerProgressBar: true
        })
        return false;
    }
    
    idchk = document.getElementById("idcheck").value;
    if(idchk != "1") {
        Swal.fire({
          icon: 'error',
          title: '아이디 중복확인을 하세요.',
          confirmButtonColor: '#000000',
          timer: 2000,
          timerProgressBar: true
        })
        return false;
    }

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
            alert(obj.result_msg);
            if(obj.flag == "1"){
                location.href = "/";
            }
        }
    };
    xhr.open("POST", "/member_insert");
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.send(datastr);
}

function checkId() {
    memberidcheck = document.getElementById("member_id").value;
    regExp = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i;
    if (memberidcheck.match(regExp) == null) {
        Swal.fire({
          icon: 'error',
          title: '이메일 형식이 아닙니다.',
          confirmButtonColor: '#000000',
          timer: 2000,
          timerProgressBar: true
        })
        document.getElementById("member_id").focus();
        return false;
    }
    if(memberidcheck == "") {
        Swal.fire({
          icon: 'error',
          title: '아이디가 비어있습니다.',
          confirmButtonColor: '#000000',
          timer: 2000,
          timerProgressBar: true
        })
        document.getElementById("member_id").focus();
        return false;
    }

    var strurl = "/member_idcheck?member_id=" + memberidcheck;
    //alert(strurl);
    //return false;

    xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            var data = xhr.responseText;

            var obj = JSON.parse(data);
            if(obj.flag == "1") {
                Swal.fire({
                  icon: 'error',
                  title: obj.result_msg,
                  confirmButtonColor: '#000000',
                  timer: 2000,
                  timerProgressBar: true
                })
                document.getElementById("member_id").focus();
            }
            else {
                Swal.fire({
                  icon: 'success',
                  title: obj.result_msg,
                  confirmButtonColor: '#000000',
                  timer: 2000,
                  timerProgressBar: true
                })
                document.getElementById("idcheck").value = "1";
                document.getElementById("member_id").readOnly = true; 
            }
        }
    };
    xhr.open("POST",strurl);
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.send(null);
}

// 새로운방법 로그인체크
function loginCheck() {

    memberid = document.getElementById("member_loginid").value;
    if(memberid == "") {
        $('.error_box').show();
        $('.error_message').html('이메일을 입력하세요.');
        document.getElementById("member_loginid").focus();
        return false;
    }

    memberpwd = document.getElementById("member_loginpwd").value;
    if(memberpwd == "") {
        $('.error_box').show();
        $('.error_message').html('비밀번호를 입력하세요.');
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
                location.href = "/";
            }
            else {
                $('.error_box').show();
                $('.error_message').html(obj.result_msg);
                $('#member_id').focus();
                if(obj.inactive == "1") {
                    $('.sendmail_btn').show();
                }
            }
        }
    };
    xhr.open("POST", "/member_login");
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.send(datastr);

}