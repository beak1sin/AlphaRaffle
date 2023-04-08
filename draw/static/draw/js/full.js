$(document).ready(function() {
    // 현재 제품은 opacity만 1
    $(window).on("load", function() {
        let scrTop = $(this).scrollTop();
        let wH = $(this).height();
        $(".product-item").each(function(i, div) {
            let oT = $(div).offset().top;
            if (oT > scrTop && oT < (scrTop+wH)) {
                $(div).animate({"opacity": 1});
                $(div).attr("loading", "1");
            }
        });
    });

    // 스크롤할때 제품들 fadeInUp 2s
    $(window).on("scroll", function() {
        let scrTop = $(this).scrollTop();
        let wH = $(this).height();
        $(".product-item").each(function(i, div) {
            let oT = $(div).offset().top;
            if (oT > scrTop && oT < (scrTop+wH)) {
                if ($(div).attr("loading") == undefined) {
                    $(div).css({
                        'animation': 'fadeInUp 2s',
                        'opacity': 1
                    });
                }
            }
        });
    });

    // 필터링 버튼을 클릭하면 사이드바 열림
    $(document).on("click", ".filter-btn", function (e){
        $(".filter-layer").removeClass("off");
        $('.u-section-1').removeClass("blurOff");
        $(".filter-layer").addClass("on");
        $('.u-section-1').addClass("blurOn");
        // alert(target.has(e.target).length);

    });
    
    // 외부영역 클릭 시 사이드바 닫기
    $(document).on("click", ".u-section-1.blurOn", function (e){
        $(".filter-layer").removeClass("on");
        $('.u-section-1').removeClass("blurOn");
        $(".filter-layer").addClass("off");
        $('.u-section-1').addClass("blurOff");
    });

    // 필터링 종료 버튼 클릭 시 닫기
    $(document).on("click", ".exit-btn", function (e){
        $(".filter-layer").removeClass("on");
        $('.u-section-1').removeClass("blurOn");
        $(".filter-layer").addClass("off");
        $('.u-section-1').addClass("blurOff");
    });

    // 필터링 브랜드 아코디언
    $(document).on("click", "#brand .filter-layer-content-content-title", function (e){
        if ($('#brand').hasClass("on")) {
            $('#brand').removeClass("on");
        } else {
            $('#brand').addClass("on");
        }
    });

    // 필터링 brand count
    let filterCount = 0;
    let brandCount = 0;

    // 필터링 brand
    $('input[type=checkbox][name=brand]').change(function() {
        if ($(this).is(':checked')) {
            brandCount++;
            $('span#brandCount').text('('+brandCount+')');
        } else {
            brandCount--;
            if (brandCount < 1) {
                $('span#brandCount').text('');
            } else {
                $('span#brandCount').text('('+brandCount+')');
            }
        }

        // if ($('input:checkbox[name="brand"]').is(":checked") == true) {
        //     alert('check됨');
        // } else {
        //     alert('체크해제');
        // }
    });

    

    // 필터링 all
    let brandList = [];
    let regionList = [];
    let onofflineList = [];
    let releaseList = [];
    let deliveryList = [];
    $("input[type=checkbox][name=brand], input[type=checkbox][name=region], input[type=checkbox][name=onoffline], input[type=checkbox][name=release], input[type=checkbox][name=delivery]").change(function() {
        // 필터링 checkbox 값
        let text = $(this).parent(".checkbox-icon").next().text();
        // 필터링 타이틀
        let title = $(this).parents(".filter-layer-content-content").children(".filter-layer-content-content-title").text().trim().split(' ')[0];
        let valueName = $(this).val(text);
        if ($(this).is(':checked')) {
            // 브랜드만 비교시 false로 나와 임의설정
            if (title.includes("브랜드")) {
                title = '브랜드';
            }
            // 필터링별 체크시 리스트 추가
            switch (title) {
                case '브랜드':
                    brandList.push(valueName.val());
                    break;
                case '국가':
                    regionList.push(valueName.val());
                    break;
                case '온라인/오프라인':
                    onofflineList.push(valueName.val());
                    break;
                case '발매유형':
                    releaseList.push(valueName.val());
                    break;
                case '배송방식':
                    deliveryList.push(valueName.val());
                    break;
                default:
                    alert('아무것도 선택 안됨');
                    break;
            }
            // 체크박스 체크 시 필터링 개수 증가
            filterCount++;
            $('span#filterCount').text('('+filterCount+')');
            $('a.u-apply-btn').removeClass('disabled');
        } else {
            // 브랜드만 비교시 false로 나와 임의설정
            if (title.includes("브랜드")) {
                title = '브랜드';
            }
            // 필터링별 체크해제시 리스트 삭제
            switch (title) {
                case '브랜드':
                    for(var i = 0; i < brandList.length; i++){ 
                        if (brandList[i] === valueName.val()) { 
                            brandList.splice(i, 1);
                            valueName.val('');
                        }
                    }
                    break;
                case '국가':
                    for(var i = 0; i < regionList.length; i++){ 
                        if (regionList[i] === valueName.val()) { 
                            regionList.splice(i, 1);
                            valueName.val('');
                        }
                    }
                    break;
                case '온라인/오프라인':
                    for(var i = 0; i < onofflineList.length; i++){ 
                        if (onofflineList[i] === valueName.val()) { 
                            onofflineList.splice(i, 1);
                            valueName.val('');
                        }
                    }
                    break;
                case '발매유형':
                    for(var i = 0; i < releaseList.length; i++){ 
                        if (releaseList[i] === valueName.val()) { 
                            releaseList.splice(i, 1);
                            valueName.val('');
                        }
                    }
                    break;
                case '배송방식':
                    for(var i = 0; i < deliveryList.length; i++){ 
                        if (deliveryList[i] === valueName.val()) { 
                            deliveryList.splice(i, 1);
                            valueName.val('');
                        }
                    }
                    break;
                default:
                    alert('아무것도 선택되지 않음2');
                    break;
            }
            // 체크박스 해제 시 필터링 개수 감소
            filterCount--;
            if (filterCount < 1) {
                $('span#filterCount').text('');
                $('a.u-apply-btn').addClass('disabled');
            } else {
                $('span#filterCount').text('('+filterCount+')');
            }
        }
    });

    // 초기화 버튼
    $(document).on("click", "#reset_btn", function() {
        $("input[type=checkbox][name=brand], input[type=checkbox][name=region], input[type=checkbox][name=onoffline], input[type=checkbox][name=release], input[type=checkbox][name=delivery]").each(function() {
            if ($(this).is(':checked')) {
                this.checked = false;
                filterCount = 0;
                brandCount = 0;
                brandList = [];
                regionList = [];
                onofflineList = [];
                releaseList = [];
                deliveryList = [];
                $('span#brandCount').text('');
                $('span#filterCount').text('');
                $('a.u-apply-btn').addClass('disabled');
            }
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

    // 필터링 적용 버튼
    $(document).on("click", ".u-apply-btn", function() {

        var data = {brandListAJAX: brandList, regionListAJAX: regionList, onofflineListAJAX: onofflineList, releaseListAJAX: releaseList, deliveryListAJAX: deliveryList};
        var datastr = JSON.stringify(data);
        
        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                var data = xhr.responseText;
    
                var obj = JSON.parse(data);
                if(obj.flag == "0"){
                    // alert(obj.result_msg);
                    $('#all').hide();
                    $('#filter').show();
                    let temp = obj.shoe;
                    let productsHTML = '';
                    for (let i=0; i<temp.length; i++) {
                        let temp2 = temp[i];
                        let imgURL = STATIC_URL + temp2.shoename + temp2.serialno + "0.jpeg"
                        // productsHTML += '<div class="u-align-center u-container-style u-products-item u-repeater-item product-item"><div class="u-container-layout u-similar-container u-valign-top u-container-layout-1"><a class="hover_temp" style="display: block; width: auto; margin: 5px 5px 10px 5px;"><div class="screen u-radius-50"><div class="bookmark-icon"><label class="bookmark-icon-label"><input type="checkbox" name="bookmark"><span class="icon"></span></label></div><img alt="" class="lazyload u-expanded-width u-image u-image-default u-product-control u-image-1 u-radius-50" data-src="{% static ' + 'draw/images/' + ' %}' + temp2.shoename + temp2.serialno + '0.jpeg" data-image-width="842" data-image-height="595"></div></a><h4 class="u-align-center u-product-control u-text u-text-grey-80 u-text-2" style="display: table;"><a class="u-product-title-link" style="font-size: 18px; display: table-cell; vertical-align: middle;"> ' + temp2.shoename + '</a></h4><a href="{% url ' + 'draw:상세정보' + ' %}?serialnum=' + temp2.serialno + '" id = "serial" class="u-border-2 u-border-grey-80 u-btn u-btn-round u-button-style u-hover-grey-80 u-none u-product-control u-radius-50 u-text-grey-80 u-text-hover-white u-btn-2" data-value = ' + temp2.serialno + '>응모하기</a></div></div>'
                        productsHTML += '<div class="u-align-center u-container-style u-products-item u-repeater-item product-item"><div class="u-container-layout u-similar-container u-valign-top u-container-layout-1"><a class="hover_temp" style="display: block; width: auto; margin: 5px 5px 10px 5px;"><div class="screen u-radius-50"><div class="bookmark-icon"><label class="bookmark-icon-label"><input type="checkbox" name="bookmark"><span class="icon"></span></label></div><img alt="" class="lazyload u-expanded-width u-image u-image-default u-product-control u-image-1 u-radius-50" data-src="' + imgURL + '" data-image-width="842" data-image-height="595"></div></a><h4 class="u-align-center u-product-control u-text u-text-grey-80 u-text-2" style="display: table;"><a class="u-product-title-link" style="font-size: 18px; display: table-cell; vertical-align: middle;"> ' + temp2.shoename + '</a></h4><a href="{% url ' + 'draw:상세정보' + ' %}?serialnum=' + temp2.serialno + '" id = "serial" class="u-border-2 u-border-grey-80 u-btn u-btn-round u-button-style u-hover-grey-80 u-none u-product-control u-radius-50 u-text-grey-80 u-text-hover-white u-btn-2" data-value = ' + temp2.serialno + '>응모하기</a></div></div>'
                    }
                    $('#temp').html(productsHTML);
                }
            }
        };
        xhr.open("POST", "filtering");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(datastr);
    });

});

