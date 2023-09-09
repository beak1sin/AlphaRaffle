$(document).ready(function() {
    $('#bookmark_tab, #checked_tab, #comment_tab, #setting_tab').click(function() {
        var targetID = $(this).attr('id');
        // console.log($(this).attr('id'));
        if (targetID == 'bookmark_tab') {
            if ($(this).hasClass('checked')) {
                return
            } else {
                $(this).addClass('checked');
                $('.bookmark-content').show();
                $('.checked-content').hide();
                $('.comment-content').hide();
                $('.setting-content').hide();
                $('.setting-content').removeClass('on');
                $('.delete-content').hide();
                $('#delete_tab').hide();
                $('#checked_tab').removeClass('checked');
                $('#comment_tab').removeClass('checked');
                $('#setting_tab').removeClass('checked');
                $('#delete_tab').removeClass('checked');
            }
        } else if (targetID == 'checked_tab') {
            if ($(this).hasClass('checked')) {
                return
            } else {
                $(this).addClass('checked');
                $('.bookmark-content').hide();
                $('.checked-content').show();
                $('.comment-content').hide();
                $('.setting-content').hide();
                $('.setting-content').removeClass('on');
                $('.delete-content').hide();
                $('#delete_tab').hide();
                $('#bookmark_tab').removeClass('checked');
                $('#comment_tab').removeClass('checked');
                $('#setting_tab').removeClass('checked');
                $('#delete_tab').removeClass('checked');
            }
        } else if (targetID == 'comment_tab') {
            if ($(this).hasClass('checked')) {
                return
            } else {
                $(this).addClass('checked');
                $('.bookmark-content').hide();
                $('.checked-content').hide();
                $('.comment-content').show();
                $('.setting-content').hide();
                $('.setting-content').removeClass('on');
                $('.delete-content').hide();
                $('#delete_tab').hide();
                $('#bookmark_tab').removeClass('checked');
                $('#checked_tab').removeClass('checked');
                $('#setting_tab').removeClass('checked');
                $('#delete_tab').removeClass('checked');
            }
        } else if (targetID == 'setting_tab') {
            if ($(this).hasClass('checked')) {
                return
            } else {
                $(this).addClass('checked');
                $('.bookmark-content').hide();
                $('.checked-content').hide();
                $('.comment-content').hide();
                $('.setting-content').addClass('on');
                $('.delete-content').hide();
                $('#delete_tab').show();
                $('#bookmark_tab').removeClass('checked');
                $('#checked_tab').removeClass('checked');
                $('#comment_tab').removeClass('checked');
                $('#delete_tab').removeClass('checked');
            }
        }
    });

    $('#delete_tab').click(function() {
        $(this).addClass('checked');
        $('.bookmark-content').hide();
        $('.checked-content').hide();
        $('.comment-content').hide();
        $('.setting-content').hide();
        $('.delete-content').show();
        $('#bookmark_tab').removeClass('checked');
        $('#checked_tab').removeClass('checked');
        $('#comment_tab').removeClass('checked');
        $('#setting_tab').removeClass('checked');
    });

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

    $('.comment-delete-btn').click(function () {
        $(".backL").css("display", "");
        let pk = $(this).parent().parent().attr('data-value');
        let comment = $(this).parent().parent().children(':nth-child(2)').children(':nth-child(1)').text();
        let created_date = $(this).parent().parent().children(':nth-child(2)').children(':nth-child(2)').text();
        let shoename = $(this).parent().parent().children(':nth-child(2)').children(':nth-child(3)').text();
        const data = {'pk': pk,'comment': comment, 'created_date': created_date, 'shoename': shoename};

        fetch('comment_delete', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            $(this).parent().parent().css({'text-align': 'center'});
            $(this).parent().parent().html(data.message);
            $(".backL").css("display", "none");
        })
        .catch(error => {
            console.log('Error: ' + error);
        });
    });

    document.getElementById('redirectAndClick').addEventListener('click', function() {
        window.location.href = `${window.location.protocol}//${window.location.host}/auth/login/?autoClick=true`;
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
