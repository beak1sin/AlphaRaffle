$(document).ready(function() {
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

  $('#member_pwd').keyup(function(e) {
    if (e.keyCode == 13) {
      e.preventDefault();
      $('.next-btn-1').click();
    }
  });

  $('.next-btn-1').click(function () {
      let memberpwd = document.getElementById("member_pwd").value;
      if(memberpwd == "") {
        $('.password-error-msg').text('비밀번호를 입력하세요.');
        return false;
      }
      pwdencrypted = hex_sha1(memberpwd);

      // wflag = document.getElementById("warrantcheck").checked;
      // if(wflag == false) {
      //     return false;
      // }

      var data = {member_pwd: pwdencrypted};
      var datastr = JSON.stringify(data);

      xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
          if (xhr.readyState == 4) {
              var data = xhr.responseText;

              var obj = JSON.parse(data);

              if(obj.flag == "0"){
                $('.password-error-msg').text(obj.result_msg);
              } else {
                // 일치
                $('.password-error-msg').text(obj.result_msg);
                $('.delete-content-1').hide();
                $('.password-icon-close').removeClass('active');
                $('#member_pwd').attr('readonly' ,true);
                $('.delete-content-1').hide();
                $('.delete-content-2').show();
              }
          }
      };
      xhr.open("POST", "/auth/mypage/delete/password_check");
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
      xhr.send(datastr);
  });

  $("#others").change(function(){
    if($(this).is(":checked")){
      console.log("Checkbox is checked.");
      // 체크박스가 체크되었을 때 수행할 작업
      $('#others_textarea').attr('readonly', false);
      $('#others_textarea').css({'background-color': '#FFFFFF'});
    } else {
      console.log("Checkbox is not checked.");
      // 체크박스가 체크되지 않았을 때 수행할 작업
      $('#others_textarea').attr('readonly', true);
      $('#others_textarea').css({'background-color': '#EEEEEE'});
      $('#others_textarea').val('');
    }
  });

  function validateCheckboxes() {
    var isChecked = false;
    var isOthersChecked = $('#others').is(':checked');
    var othersText = $('#others_textarea').val().trim();

    // 체크박스가 하나라도 선택되어 있는지 확인
    $('.checkbox-box input[type="checkbox"]').each(function() {
      if (this.checked) {
        isChecked = true;
        if (isOthersChecked && othersText === '') {
          isChecked = false;
          return false;
        }
      }
    });

    if (!isChecked) {
      $('.checkbox-error-msg').text('하나 이상의 체크박스를 선택해주세요.');
      $('.checkbox-error-msg-2').text('하나 이상의 체크박스를 선택해주세요.');
      if (isOthersChecked && othersText === '') {
        $('.checkbox-error-msg').text('기타 항목에 텍스트를 입력해주세요.');
        $('.checkbox-error-msg-2').text('기타 항목에 텍스트를 입력해주세요.');
      }
      return false;
    }

    $('.checkbox-error-msg').text('');
    $('.checkbox-error-msg-2').text('');
    return true;
  }


  $('.next-btn-2').click(function() {
    if (validateCheckboxes()) {
      $('.checkbox-error-msg').text('');
      $('.delete-content-2').hide();
      $('.delete-content-3').show();
    }
  });

  function validateAndSendData() {
    var checkedOptions = [];
  
    // 체크박스가 하나라도 선택되어 있는지 확인
    $('.checkbox-box input[type="checkbox"]').each(function() {
      if (this.checked) {
        if (this.name == 'others') {
          var othersList = [];
          othersList.push(this.name);
          othersList.push($('#others_textarea').val());
          checkedOptions.push(othersList);
        } else {
          checkedOptions.push(this.name); // 체크된 체크박스의 이름을 배열에 추가
        }
      }
    });
    return checkedOptions;
  }

  $('.delete-btn').click(function() {
    let allRequiredChecked = $('#delete_agree_1').is(':checked') && $('#delete_agree_2').is(':checked');
    if (validateCheckboxes()) {
      if (!allRequiredChecked) {
        $('.checkbox-error-msg-2').text('모든 필수 항목을 체크해주세요.');
        return false;
      }

      $('.checkbox-error-msg-2').text('');
      let memberpwd = document.getElementById("member_pwd").value;
      if(memberpwd == "") {
        $('.password-error-msg').text('비밀번호를 입력하세요.');
        $('.checkbox-error-msg-2').text('비밀번호 확인을 해주세요.');
        return false;
      }
      pwdencrypted = hex_sha1(memberpwd);

      console.log(validateAndSendData());

      var data = {member_pwd: pwdencrypted, checkboxList: validateAndSendData()};
      var datastr = JSON.stringify(data);

      xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
          if (xhr.readyState == 4) {
              var data = xhr.responseText;

              var obj = JSON.parse(data);

              if(obj.flag == "0"){
                $('.checkbox-error-msg-2').text(obj.result_msg);
              } else {
                // 일치
                $('.checkbox-error-msg-2').text(obj.result_msg);
                $('.delete-content-3').hide();
                $('.delete-content-4').show();
              }
          }
      };
      xhr.open("POST", "/auth/mypage/delete/member_delete");
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
      xhr.send(datastr);
    }
  });
  
  

});
