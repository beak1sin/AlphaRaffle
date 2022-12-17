$(document).ready(function() {
    $('#update_btn').on('click', function() {
        $('#update_box').show();
        $('#information_box').hide();
        $('#update_btn').hide();
        $('#delete_btn').show();
        $('#title_box').addClass('title_box');
        if ($(window).width() <= 767) {
            $('#label-email').removeClass('u-label-none');
            $('#label-name').removeClass('u-label-none');
            $('#label-nickname').removeClass('u-label-none');
            $('#label-phonenumber').removeClass('u-label-none');
            $('#label-nikeid').removeClass('u-label-none');
            $('#label-birth').removeClass('u-label-none');
        } else {
            if ($('#label-email').hasClass('u-label-none')) {
                // alert('good');
            } else {
                $('#label-email').addClass('u-label-none');
                $('#label-name').addClass('u-label-none');
                $('#label-nickname').addClass('u-label-none');
                $('#label-phonenumber').addClass('u-label-none');
                $('#label-nikeid').addClass('u-label-none');
                $('#label-birth').addClass('u-label-none');
            }
        }
    });
    $('#cancel_btn').on('click', function() {
        $('#update_box').hide();
        $('#information_box').show();
        $('#update_btn').show();
        $('#delete_btn').hide();
        $('#title_box').removeClass('title_box');
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