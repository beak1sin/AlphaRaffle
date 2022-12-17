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

function member_delete() {
    memberpwd = document.getElementById("member_pwd").value;
    if(memberpwd == "") {
        Swal.fire({
          icon: 'error',
          title: '비밀번호를 입력하세요.',
          confirmButtonColor: '#000000',
          timer: 2000,
          timerProgressBar: true
        })
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

    var data = {member_pwd: pwdencrypted};
    var datastr = JSON.stringify(data);

    xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            var data = xhr.responseText;

            var obj = JSON.parse(data);

            if(obj.flag == "1"){
                Swal.fire({
                  icon: 'success',
                  title: obj.result_msg,
                  confirmButtonColor: '#000000',
                  timer: 2000,
                  timerProgressBar: true
                })
                location.href = "/";
            } else {
              Swal.fire({
                icon: 'error',
                title: obj.result_msg,
                confirmButtonColor: '#000000',
                timer: 2000,
                timerProgressBar: true
              })
            }
        }
    };
    xhr.open("POST", "/member_delete");
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.send(datastr);
}