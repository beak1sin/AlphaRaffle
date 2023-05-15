$(document).ready( () => {

    // alert(window.innerWidth + ', ' + window.innerHeight);

    $('#main-btn').click( () => {
        location.href = '/main/';
    });

    $('#join-btn').click( () => {
        location.href = '/auth/login/';
    });

    window.addEventListener("wheel", (e) =>{
        e.preventDefault();
    },{passive : false});

    var $html = $("html");
    var page = 1;
    var lastPage = $(".content").length;
    $html.animate({scrollTop:0},10);

    let page1 = page2 = page3 = true;

    // if($html.is(":animated")) return;
     
    //     if(e.originalEvent.deltaY > 0){
    //         if(page== lastPage) return;
    //         page++;
    //     }else if(e.originalEvent.deltaY < 0){
    //         if(page == 1) return;
    //         page--;
    //     }

    //     page = 1;
    //     var posTop = (page-1) * $(window).height();
     
    //     $html.animate({scrollTop : posTop});

    //     if (page1) {
    //         if ($('.snow')) removeSnow();
    //         if ($('.shoe')) removeShoe();
    //         clearInterval(interVal);
    //         typing("다양한 발매정보와 응모를 한 번에 간편하게!", document.querySelector('.text'));
    //         setTimeout(typing, 2500, "발매 정보를 확인하고 응모하고 싶은 신발을 응모하세요.", document.querySelector('.text2'));
    //         page1 = false;
    //     }

    $(window).on("wheel", (e) => {
 
        if($html.is(":animated")) return;
     
        if(e.originalEvent.deltaY > 0){
            if(page== lastPage) return;
            page++;
        }else if(e.originalEvent.deltaY < 0){
            if(page == 1) return;
            page--;
        }
        var posTop = (page-1) * $(window).height();
     
        $html.animate({scrollTop : posTop});

        if (page == 3) {
            for (let i = 0; i < 20; i++) { createSnow() }
            setTimeout(function () {
                removeSnow();
            }, 10000);
            interVal = setInterval(startSnow, 10000);
            if (page3) {
                setTimeout(zindexSnow0, 1000);
                typing("지금 바로 시작하세요!!", document.querySelector('.text5'));
                document.querySelector('.text6').classList.add('delay');
                setTimeout(typing, 1000, "비용 걱정 없이 회원 가입만으로도 이용 가능합니다.", document.querySelector('.text6'));
                page3 = false;
            }
        } else if (page == 2) {
            if ($('.snow')) removeSnow();
            if ($('.shoe')) removeShoe();
            clearInterval(interVal);
            // wait(2000);
            // document.querySelector('.text').innerText = "";
            // document.querySelector('.text2').innerText = "";
            if (page2) {
                typing("클릭 한 번으로 응모하세요!", document.querySelector('.text3'));
                document.querySelector('.text4').classList.add('delay');
                setTimeout(typing, 1500, "알파라플만의 간편한 자동 응모 서비스를 경험해보세요.", document.querySelector('.text4'));
                page2 = false;
            }
        } else if (page == 1) {
            if ($('.snow')) removeSnow();
            if ($('.shoe')) removeShoe();
            clearInterval(interVal);
            if (page1) {
                typing("다양한 발매정보와 응모를 한 번에 간편하게!", document.querySelector('.text'));
                setTimeout(typing, 2500, "발매 정보를 확인하고 응모하고 싶은 신발을 응모하세요.", document.querySelector('.text2'));
                page1 = false;
            }
        }
     
    });
    

    $(window).on("load", (e) => {
 
        if($html.is(":animated")) return;
     
        if(e.originalEvent.deltaY > 0){
            if(page== lastPage) return;
            page++;
        }else if(e.originalEvent.deltaY < 0){
            if(page == 1) return;
            page--;
        }

        page = 1;
        var posTop = (page-1) * $(window).height();
     
        $html.animate({scrollTop : posTop});

        if (page1) {
            if ($('.snow')) removeSnow();
            if ($('.shoe')) removeShoe();
            clearInterval(interVal);
            typing("다양한 발매정보와 응모를 한 번에 간편하게!", document.querySelector('.text'));
            setTimeout(typing, 2500, "발매 정보를 확인하고 응모하고 싶은 신발을 응모하세요.", document.querySelector('.text2'));
            page1 = false;
        }
        

        // if (page == 3) {
        //     for (let i = 0; i < 20; i++) { createSnow() }
        //     setTimeout(function () {
        //         removeSnow();
        //     }, 10000);
        //     interVal = setInterval(startSnow, 10000);
        // } else if (page == 2) {
        //     if ($('.snow')) removeSnow();
        //     if ($('.shoe')) removeShoe();
        //     clearInterval(interVal);
        // } else if (page == 1) {
            // if ($('.snow')) removeSnow();
            // if ($('.shoe')) removeShoe();
            // clearInterval(interVal);
            // typing("다양한 발매정보와 응모를 한 번에 간편하게!", document.querySelector('.text'));
            // setTimeout(typing, 2500, "발매 정보를 확인하고 응모하고 싶은 신발을 응모하세요.", document.querySelector('.text2'));
        // }
     
    });

    let interVal = setInterval(startSnow, 10000);
    clearInterval(interVal);

    $('.first-btn, .second-btn, .third-btn').click( () => {
        var $clicked = $(event.target);
        if ($clicked.is('.first-btn')) {
            page = 1;
            var posTop = (page-1) * $(window).height();
            $html.animate({scrollTop : posTop});
            if ($('.snow')) removeSnow();
            if ($('.shoe')) removeShoe();
            clearInterval(interVal);
            if (page1) {r
                typing("다양한 발매정보와 응모를 한 번에 간편하게!", document.querySelector('.text'));
                setTimeout(typing, 2500, "발매 정보를 확인하고 응모하고 싶은 신발을 응모하세요.", document.querySelector('.text2'));
                page1 = false;
            }
        } else if($clicked.is('.second-btn')) {
            page = 2;
            var posTop = (page-1) * $(window).height();
            $html.animate({scrollTop : posTop});
            if ($('.snow')) removeSnow();
            if ($('.shoe')) removeShoe();
            clearInterval(interVal);
            if (page2) {
                typing("클릭 한 번으로 응모하세요!", document.querySelector('.text3'));
                document.querySelector('.text4').classList.add('delay');
                setTimeout(typing, 1500, "알파라플만의 간편한 자동 응모 서비스를 경험해보세요.", document.querySelector('.text4'));
                page2 = false;
            }
        } else if($clicked.is('.third-btn')) {
            page = 3;
            var posTop = (page-1) * $(window).height();
            $html.animate({scrollTop : posTop});
            for (let i = 0; i < 20; i++) { createSnow() }
            setTimeout(function () {
                removeSnow();
            }, 10000);
            interVal = setInterval(startSnow, 10000);
            if (page3) {
                setTimeout(zindexSnow0, 1000);
                typing("지금 바로 시작하세요!!", document.querySelector('.text5'));
                document.querySelector('.text6').classList.add('delay');
                setTimeout(typing, 1000, "비용 걱정 없이 회원 가입만으로도 이용 가능합니다.", document.querySelector('.text6'));
                page3 = false;
            }
        }
    });

    const shoe0 = STATIC_NECESSARY + "scott.png";
    const shoe1 = STATIC_NECESSARY + "chicago.png";
    const shoe2 = STATIC_NECESSARY + "scott2.png";
    const shoe3 = STATIC_NECESSARY + "dunkpanda.png";
    const shoe4 = STATIC_NECESSARY + "nb.png";
    const shoe5 = STATIC_NECESSARY + "superstar.png";


    // 신발 비
    // function createSnow () {
    //     const el = document.createElement('div');
    //     el.classList.add('snow');
    //     el.style.position = 'absolute';
    //     el.style.marginLeft = Math.floor(Math.random() * window.innerWidth - 300) + 'px';
    //     el.style.marginTop = Math.floor(Math.random() * window.innerHeight - 300) + 'px';
    //     const elImg = document.createElement('img');
    //     elImg.src = eval('shoe' + Math.floor(Math.random() * 6));
    //     el.appendChild(elImg);
    //     $('.content.snowSection').prepend(el);
    // }

    const createSnow = async () => {
        const el = document.createElement('div');
        el.classList.add('snow');
        el.style.position = 'absolute';
        el.style.marginLeft = Math.floor(Math.random() * window.innerWidth - 300) + 'px';
        el.style.marginTop = Math.floor(Math.random() * window.innerHeight - 300) + 'px';
        const elImg = document.createElement('img');
        elImg.src = eval('shoe' + Math.floor(Math.random() * 6));
        el.appendChild(elImg);
        $('.content.snowSection').prepend(el);
    }

    function removeSnow() {
        $('.snow').remove();
    }

    function removeShoe() {
        $('.shoe').remove();
    }
    
    function startSnow () {
        for (let i = 0; i < 20; i++) { 
            if (i % 2 == 0) {
                createSnow(); 
            } else {
                setTimeout(function () {
                    createShoe();
                }, 5000);
            }
        }
        setTimeout(function () {
            removeSnow();
        }, 10000);
        setTimeout(function () {
            removeShoe();
        }, 15000);
    }

    function createShoe () {
        const el = document.createElement('div');
        el.classList.add('shoe');
        el.style.position = 'absolute';
        el.style.marginLeft = Math.floor(Math.random() * window.innerWidth - 300) + 'px';
        el.style.marginTop = Math.floor(Math.random() * window.innerHeight - 300) + 'px';
        const elImg = document.createElement('img');
        elImg.src = eval('shoe' + Math.floor(Math.random() * 6));
        el.appendChild(elImg);
        $('.content.snowSection').prepend(el);
    }

    function zindexSnow0() {
        $('.snow').css({'z-index': '0'});
        $('.show').css({'z-index': '0'});
    }
    function zindexSnowMinus() {
        $('.snow').css({'z-index': '-1'});
        $('.show').css({'z-index': '-1'});
        alert('complete');
    }
    // for (let i = 0; i < 20; i++) {
    //     // if (i % 2 == 0) {
    //     //     createSnow();
    //     // } else {
    //     //     createShoe();
    //     // }
    //     createSnow();
    // }

    // const $text = document.querySelector('.text');

    // 글자 입력 속도
    const speed = 100;

    const changeLineBreak = (letter) => {
        return letter.map(text => text === "\n" ? "<br>" : text);
    }

    const letters = "다양한 발매정보와 응모를 한 번에 간편하게!"

    // 타이핑 효과
    const typing = async (letters, $text) => {  
        const letter = changeLineBreak(letters.split(""));
        
        while (letter.length) {
            await wait(speed);
            $text.innerHTML += letter.shift(); 
        }
        $text.classList.remove('text');
        $text.classList.add('textremove');
        $text.classList.remove('text2');
        $text.classList.add('textremove');
        $text.classList.remove('text3');
        $text.classList.add('textremove');
        $text.classList.remove('text4');
        $text.classList.add('textremove');
        $text.classList.remove('text5');
        $text.classList.add('textremove');
        $text.classList.remove('text6');
        $text.classList.add('textremove');

    // 잠시 대기
    // await wait(1500)
    
    // 지우는 효과
    // remove();
    }

    // 글자 지우는 효과
    const remove = async () => {
        const letter = changeLineBreak(letters.split(""));
        
        while (letter.length) {
            await wait(speed);
            
            letter.pop();
            $text.innerHTML = letter.join(""); 
        }
        
        await wait(1000)
        // 다음 순서의 글자로 지정, 타이핑 함수 다시 실행
        typing();
    }

    // 딜레이 기능 ( 마이크로초 )
    function wait(ms) {
        return new Promise(res => setTimeout(res, ms))
    }

    // 초기 실행
    // setTimeout(typing, 1500, "다양한 발매정보와 응모를 한 번에 간편하게!", document.querySelector('.text'));
    // typing(letters);
});