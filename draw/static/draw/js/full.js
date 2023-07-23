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

    $('.like').click(function() {
        var serialno = $(this).attr('data-value');
        var $clickedBtn = $(this).next();
        var $this = $(this);

        var data = {serialnoAJAX: serialno};
        var datastr = JSON.stringify(data);
        
        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                var data = xhr.responseText;
    
                var obj = JSON.parse(data);

                if (obj.flag == '0') {
                    alert(obj.result_msg);
                    location.href = '/auth/login/'
                } else {
                    // alert(obj.liked);
                    if(obj.liked) {
                        alert(obj.liked);
                        $this.text('좋아요 취소');
                    } else {
                        alert(obj.liked);
                        $this.text('좋아요');
                    }
                    $clickedBtn.text(obj.count);
                }
            }
        };
        xhr.open("POST", 'like2');
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(datastr);

    });


    // 필터링 버튼을 클릭하면 사이드바 열림
    $(document).on("click", ".menu-icon-label", function (e){
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

    function exitBtn() {
        $(".filter-layer").removeClass("on");
        $('.u-section-1').removeClass("blurOn");
        $(".filter-layer").addClass("off");
        $('.u-section-1').addClass("blurOff");
    }

    // 필터링 브랜드 아코디언
    // $(document).on("click", "#brand .filter-layer-content-content-title", function (e){
    //     if ($('#brand').hasClass("on")) {
    //         $('#brand').removeClass("on");
    //     } else {
    //         $('#brand').addClass("on");
    //     }
    // });

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
        let text = $(this).parent().parent(".circle-icon").next().text();
        // 필터링 타이틀
        let title = '';
        if($(this).attr('name') == 'brand'){
            title = $(this).parents(".filter-layer-content-content").children(".filter-layer-content-content-title").text().trim().split(' ')[0];
        } else {
            title = $(this).parents(".filter-layer-content-content").children(".filter-layer-content-content-title").text().trim();
        }
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
                case '국내 해외':
                    regionList.push(valueName.val());
                    break;
                case '발매 장소':
                    onofflineList.push(valueName.val());
                    break;
                case '발매 유형':
                    releaseList.push(valueName.val());
                    break;
                case '배송방식':
                    deliveryList.push(valueName.val());
                    break;
                default:
                    alert('아무것도 선택 안됨');
                    break;
            }
            console.log(brandList);
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
                case '국내 해외':
                    for(var i = 0; i < regionList.length; i++){ 
                        if (regionList[i] === valueName.val()) { 
                            regionList.splice(i, 1);
                            valueName.val('');
                        }
                    }
                    break;
                case '발매 장소':
                    for(var i = 0; i < onofflineList.length; i++){ 
                        if (onofflineList[i] === valueName.val()) { 
                            onofflineList.splice(i, 1);
                            valueName.val('');
                        }
                    }
                    break;
                case '발매 유형':
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

    

    // 필터링 적용 버튼
    // $(document).on("click", "#apply_btn", function() {

    //     var data = {brandListAJAX: brandList, regionListAJAX: regionList, onofflineListAJAX: onofflineList, releaseListAJAX: releaseList, deliveryListAJAX: deliveryList};
    //     var datastr = JSON.stringify(data);
        
    //     xhr = new XMLHttpRequest();
    //     xhr.onreadystatechange = function() {
    //         if (xhr.readyState == 4) {
    //             var data = xhr.responseText;
    
    //             var obj = JSON.parse(data);
    //             if(obj.flag == "0"){
    //                 // alert(obj.result_msg);
    //                 $('#all').hide();
    //                 $('#filter').show();
    //                 let shoe = obj.shoe;
    //                 let productsHTML = '';
    //                 for (let i=0; i<shoe.length; i++) {
    //                     let shoe2 = shoe[i];
    //                     let imgURL = STATIC_IMAGES_URL + shoe2.shoename + shoe2.serialno + "0.jpeg"
    //                     productsHTML += '<div class="u-align-center u-container-style u-products-item u-repeater-item product-item product-item-filter"><div class="u-container-layout u-similar-container u-valign-top u-container-layout-1"><a class="hover_temp" style="display: block; width: auto; margin: 5px 5px 10px 5px;"><div class="screen u-radius-50"><div class="bookmark-icon"><label class="bookmark-icon-label"><input type="checkbox" name="bookmark"><span class="icon"></span></label></div><img alt="" class="lazyload u-expanded-width u-image u-image-default u-product-control u-image-1 u-radius-50" data-src="' + imgURL + '" data-image-width="842" data-image-height="595"></div></a><h4 class="u-align-center u-product-control u-text u-text-grey-80 u-text-2" style="display: table;"><a class="u-product-title-link" style="font-size: 18px; display: table-cell; vertical-align: middle;"> ' + shoe2.shoename + '</a></h4><a href="' + TEMPLATES_DETAILS_URL + '?serialnum=' + shoe2.serialno + '" id = "serial" class="u-border-2 u-border-grey-80 u-btn u-btn-round u-button-style u-hover-grey-80 u-none u-product-control u-radius-50 u-text-grey-80 u-text-hover-white u-btn-2" data-value = ' + shoe2.serialno + '>응모하기</a></div></div>'
    //                 }
    //                 $('#filter_repeater').html(productsHTML);
    //                 $(".product-item-filter").each(function(i, div) {
    //                     $(this).animate({"opacity": 1});
    //                     $(this).attr("loading", "1");
    //                 });
    //             }
    //         }
    //     };
    //     xhr.open("POST", "filtering");
    //     xhr.setRequestHeader("X-CSRFToken", csrftoken);
    //     xhr.send(datastr);
    // });


    // $(document).on("click", "#apply_btn", function() {
    //     $(".backL").css("display", "");
    //     var data = {brandListAJAX: brandList, regionListAJAX: regionList, onofflineListAJAX: onofflineList, releaseListAJAX: releaseList, deliveryListAJAX: deliveryList};
    //     var datastr = JSON.stringify(data);
        
    //     xhr = new XMLHttpRequest();
    //     xhr.onreadystatechange = function() {
    //         if (xhr.readyState == 4) {
    //             var data = xhr.responseText;
    
    //             var obj = JSON.parse(data);
                
    //             if(obj.flag == "0"){
    //                 // alert(obj.result_msg);
    //                 $('#all').hide();
    //                 $('#filter').show();
    //                 var shoe = JSON.parse(obj.shoes);
    //                 var likes = obj.likes;  // 멤버별 신발 좋아요 여부
    //                 let html = '';
    //                 html += '<div class="viewsort-filter-flex off"><div class="viewsort-fliter-items"><div class="viewsort-items-box"><div class="circle-icon"><label class="circle-icon-label"><input type="radio"id="circle-checkbox"name="order"checked><span class="icon"></span></label></div><label class="viewsort-items-text"for="circle-checkbox">최신순</label></div><p class="viewsort-items-comment">가장 최근에 올라온 게시글 순서대로 정렬합니다.</p></div><div class="viewsort-fliter-items"><div class="viewsort-items-box"><div class="circle-icon"><label class="circle-icon-label"><input type="radio"id="circle-checkbox2"name="order"><span class="icon"></span></label></div><label class="viewsort-items-text"for="circle-checkbox2">찜한순</label></div><p class="viewsort-items-comment">가장 많은 북마크를 보유한 순서대로 정렬합니다.</p></div><div class="viewsort-fliter-items"><div class="viewsort-items-box"><div class="circle-icon"><label class="circle-icon-label"><input type="radio"id="circle-checkbox3"name="order"><span class="icon"></span></label></div><label class="viewsort-items-text"for="circle-checkbox3">조회순</label></div><p class="viewsort-items-comment">가장 많이 조회한 순서대로 정렬합니다.</p></div><div class="viewsort-fliter-items"><div class="viewsort-items-box"><div class="circle-icon"><label class="circle-icon-label"><input type="radio"id="circle-checkbox4"name="order"><span class="icon"></span></label></div><label class="viewsort-items-text"for="circle-checkbox4">댓글순</label></div><p class="viewsort-items-comment">댓글이 가장 많은 순서대로 정렬합니다.</p></div></div>';
    //                 for (let i=0; i<shoe.length; i++) {
    //                     let shoe1 = shoe[i].fields;
    //                     let liked = likes[i];
    //                     html += '<div class="grid-box" data-value="' + shoe1.serialno + '">';
    //                     html += '<div class="grid-container"><div class="grid-img-box">';
    //                     html += '<div class="comment-icon"><label class="comment-icon-label"><span class="icon"></span></label></div>';
    //                     html += '<div class="commentCount-box"><p class="commentCount">0</p></div>';
    //                     html += '<div class="img-box" onclick="location.href = \'' + STATIC_FULL_URL + shoe1.serialno + '\'">';
    //                     html += '<img class="lazyload shoeimg" data-src="' + STATIC_IMAGES_URL + shoe1.shoename + shoe1.serialno + '0.jpeg"></div>';
    //                     html += '<div class="bookmark-icon">';
    //                     html += '<label class="bookmark-icon-label' + (liked ? ' on' : '') + '">';
    //                     html += '<span class="icon"></span></label></div>';
    //                     html += '<div class="shoelikecount-box"><p class="shoelikecount">' + shoe1.shoelikecount + '</p></div></div>';
    //                     html += '<div class="grid-shoename-box"><p class="shoename">' + shoe1.shoename + '</p></div>';
    //                     html += '<div class="grid-pubdate-box"><p class="pubdate">' + shoe1.pubdate + '</p></div>';
    //                     html += '<div class="grid-goBtn-box"><button class="goBtn" onclick="location.href = \'' + STATIC_FULL_URL + shoe1.serialno + '\'">바로가기</button></div>';
    //                     html += '</div></div>';
    //                 }
    //                 $('.infinite-container').html('');
    //                 $('.infinite-container').append(html);
    //                 $('#shoe_count').text(obj.shoe_count + '개');
    //                 exitBtn();
    //                 $(".backL").css("display", "none");
    //                 $('.bookmark-icon-label').click(function() {
    //                     let $serialno = $(this).parent().parent().parent().parent().attr('data-value');
                    
    //                     var $this = $(this);
    //                     var $count = $(this).parent().next().children();
                    
    //                     var data = {serialnoAJAX: $serialno};
    //                     var datastr = JSON.stringify(data);
                    
    //                     xhr = new XMLHttpRequest();
    //                     xhr.onreadystatechange = function() {
    //                         if (xhr.readyState == 4) {
    //                             var data = xhr.responseText;
                    
    //                             var obj = JSON.parse(data);
                    
    //                             if (obj.flag == '0') {
    //                                 alert(obj.result_msg);
    //                                 location.href = '/auth/login/';
    //                             } else {
    //                                 if(obj.liked) {
    //                                     $this.addClass('on');
    //                                 } else {
    //                                     $this.removeClass('on');
    //                                 }
    //                                 $count.text(obj.count);
    //                             }
    //                         }
    //                     };
    //                     xhr.open("POST", "likeShoe");
    //                     xhr.setRequestHeader("X-CSRFToken", csrftoken);
    //                     xhr.send(datastr);
    //                 });
    //             }
    //         }
    //     };
    //     xhr.open("POST", "filtering");
    //     xhr.setRequestHeader("X-CSRFToken", csrftoken);
    //     xhr.send(datastr);
    // });

    $('#apply_btn').click(function() {
        
        // 현재 페이지 URL을 가져옵니다.
        const currentURL = window.location.search;

        // 새로운 URL 파라미터를 만듭니다. 여러 값을 쉼표로 연결합니다.
        const newURLParams = new URLSearchParams(currentURL);
        newURLParams.set("brand", brandList.join(","));


        // 기존 URL의 경로와 파라미터를 유지하면서 업데이트된 파라미터를 반영
        const newURL = currentURL.split("?")[0] + "?" + newURLParams;

        // 새로운 URL로 페이지를 이동합니다.
        window.location.href = newURL;
    });


    $("input[type=radio][name=order]").change(function() {
        return
        $(".backL").css("display", "");
        let $order = $(this).attr('id');

        var data = {orderAJAX: $order};
        var datastr = JSON.stringify(data);

        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                var data = xhr.responseText;
                var obj = JSON.parse(data);
                if (obj.flag == '1') {
                    var shoe = JSON.parse(obj.shoes);
                    var likes = obj.likes;  // 멤버별 신발 좋아요 여부
                    let html = '';
                    html += '<div class="viewsort-filter-flex off"><div class="viewsort-fliter-items"><div class="viewsort-items-box"><div class="circle-icon"><label class="circle-icon-label"><input type="radio"id="circle-checkbox"name="order"checked><span class="icon"></span></label></div><label class="viewsort-items-text"for="circle-checkbox">최신순</label></div><p class="viewsort-items-comment">가장 최근에 올라온 게시글 순서대로 정렬합니다.</p></div><div class="viewsort-fliter-items"><div class="viewsort-items-box"><div class="circle-icon"><label class="circle-icon-label"><input type="radio"id="circle-checkbox2"name="order"><span class="icon"></span></label></div><label class="viewsort-items-text"for="circle-checkbox2">찜한순</label></div><p class="viewsort-items-comment">가장 많은 북마크를 보유한 순서대로 정렬합니다.</p></div><div class="viewsort-fliter-items"><div class="viewsort-items-box"><div class="circle-icon"><label class="circle-icon-label"><input type="radio"id="circle-checkbox3"name="order"><span class="icon"></span></label></div><label class="viewsort-items-text"for="circle-checkbox3">조회순</label></div><p class="viewsort-items-comment">가장 많이 조회한 순서대로 정렬합니다.</p></div><div class="viewsort-fliter-items"><div class="viewsort-items-box"><div class="circle-icon"><label class="circle-icon-label"><input type="radio"id="circle-checkbox4"name="order"><span class="icon"></span></label></div><label class="viewsort-items-text"for="circle-checkbox4">댓글순</label></div><p class="viewsort-items-comment">댓글이 가장 많은 순서대로 정렬합니다.</p></div></div>';
                    for (let i=0; i<shoe.length; i++) {
                        let shoe1 = shoe[i].fields;
                        let liked = likes[i];
                        html += '<div class="grid-box" data-value="' + shoe1.serialno + '">';
                        html += '<div class="grid-container"><div class="grid-img-box">';
                        html += '<div class="comment-icon"><label class="comment-icon-label"><span class="icon"></span></label></div>';
                        html += '<div class="commentCount-box"><p class="commentCount">0</p></div>';
                        html += '<div class="img-box" onclick="location.href = \'' + STATIC_FULL_URL + shoe1.serialno + '\'">';
                        html += '<img class="lazyload shoeimg" data-src="' + STATIC_IMAGES_URL + shoe1.shoename + shoe1.serialno + '0.jpeg"></div>';
                        html += '<div class="bookmark-icon">';
                        html += '<label class="bookmark-icon-label' + (liked ? ' on' : '') + '">';
                        html += '<span class="icon"></span></label></div>';
                        html += '<div class="shoelikecount-box"><p class="shoelikecount">' + shoe1.shoelikecount + '</p></div></div>';
                        html += '<div class="grid-shoename-box"><p class="shoename">' + shoe1.shoename + '</p></div>';
                        html += '<div class="grid-pubdate-box"><p class="pubdate">' + shoe1.pubdate + '</p></div>';
                        html += '<div class="grid-goBtn-box"><button class="goBtn" onclick="location.href = \'' + STATIC_FULL_URL + shoe1.serialno + '\'">바로가기</button></div>';
                        html += '</div></div>';
                    }
                    $('.infinite-container').html('');
                    $('.infinite-container').append(html);
                    $(".backL").css("display", "none");
                    $('.bookmark-icon-label').click(function() {
                        let $serialno = $(this).parent().parent().parent().parent().attr('data-value');
                    
                        var $this = $(this);
                        var $count = $(this).parent().next().children();
                    
                        var data = {serialnoAJAX: $serialno};
                        var datastr = JSON.stringify(data);
                    
                        xhr = new XMLHttpRequest();
                        xhr.onreadystatechange = function() {
                            if (xhr.readyState == 4) {
                                var data = xhr.responseText;
                    
                                var obj = JSON.parse(data);
                    
                                if (obj.flag == '0') {
                                    alert(obj.result_msg);
                                    location.href = '/auth/login/';
                                } else {
                                    if(obj.liked) {
                                        $this.addClass('on');
                                    } else {
                                        $this.removeClass('on');
                                    }
                                    $count.text(obj.count);
                                }
                            }
                        };
                        xhr.open("POST", "likeShoe");
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        xhr.send(datastr);
                    });
                }
            }
        };
        xhr.open("POST", "filtering_order");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(datastr);
    });


    $("input[type=radio][name=sort]").change(function() {
        const url = window.location.href;
        const paramName = $(this).attr('name');
        const paramValue = $(this).val();
        const newURL = addParamToURL(url, paramName, paramValue);
        window.location.href = newURL;
        // $('#viewsort_form').submit();
    });

    function getParam(sname) {
        var params = location.search.substr(location.search.indexOf("?") + 1);
        var sval = "";
        params = params.split("&");
        for (var i = 0; i < params.length; i++) {
            temp = params[i].split("=");
            if ([temp[0]] == sname) { sval = decodeURIComponent(temp[1]); }
        }
        return sval;
    }

    if (getParam('sort') == 'latest') {
        $("input[type=radio][name=sort][value=latest]").prop("checked", true);
        $('#sort_name').text("최신 순");
    } else if (getParam('sort') == 'bookmark') {
        $("input[type=radio][name=sort][value=bookmark]").prop("checked", true);
        $('#sort_name').text("찜한 순");
    } else if (getParam('sort') == 'views') {
        $("input[type=radio][name=sort][value=views]").prop("checked", true);
        $('#sort_name').text("조회 순");
    } else if (getParam('sort') == 'comments') {
        $("input[type=radio][name=sort][value=comments]").prop("checked", true);
        $('#sort_name').text("댓글 순");
    }

    function getParamNameBool(sname) {
        var params = location.search.substr(location.search.indexOf("?") + 1);
        params = params.split("&");
        for (var i = 0; i < params.length; i++) {
            temp = params[i].split("=");
            if ([temp[0]] == sname) { return true }
        }
    }

    if (getParamNameBool('search_term')) {
        if (getParam('search_term') == ''){
            $('.search-result').hide();
        } else {
            $('.search-result-value').text('‘' + getParam('search_term') +  '’ ');
            $('.search-result').show();
        }
        
    } else {
        $('.search-result').hide();
    }
    
    // var waypoint = new Waypoint({
    //     element: document.getElementById('scroll-container'),
    //     handler: function(direction) {
    //         if (direction === 'down') {
    //             // 추가 데이터를 불러오는 API 엔드포인트 호출
    //             alert('Bottom of element hit top of viewport');
    //             loadData();
    //             // alert('밑이야');
    //             // console.log('밑이야');
    //         }
    //     },
    //     // offset: '100%'
    //     // offset: 'bottom-in-view'
    //     offset: function() {
    //         return this.element.clientHeight - window.innerHeight;
    //     }
    // });

    function addParamToURL(url, paramName, paramValue) {
        const urlParams = new URLSearchParams(window.location.search);
        urlParams.set(paramName, paramValue);
      
        // 기존 URL의 경로와 파라미터를 유지하면서 새로운 파라미터를 덧붙임
        const newURL = `${url.split('?')[0]}?${urlParams}`;
      
        return newURL;
    }

    $('#recent_searches_value').click(function() {
        const url = window.location.href;
        const paramName = 'search_term';
        const paramValue = $(this).text();
        const newURL = addParamToURL(url, paramName, paramValue);
        window.location.href = newURL;
    });

    var isLoading = false;

    window.addEventListener('scroll', function() {
        var scrollContainer = document.getElementById('scroll-container');
        var scrollHeight = scrollContainer.scrollHeight;
        var scrollTop = Math.ceil(window.pageYOffset || document.documentElement.scrollTop);
        var windowHeight = window.innerHeight;

        //   console.log('scrollContainer의 scrollHeight: ' + scrollHeight, 'scrollTop: ' + scrollTop, 'windowHeight: ' + windowHeight);
        
        if (!isLoading && scrollTop + windowHeight >= scrollHeight) {
            // 추가 데이터를 불러오는 작업 수행
            isLoading = true;
            loadData(function() {
                isLoading = false;
            });
        }
    });

    var nextPage = 2;  // 초기 페이지 번호

    function loadData(callback) {
        // AJAX 요청을 통해 추가 데이터를 백엔드에 요청합니다.
        // 백엔드에서는 페이지 번호 등을 기반으로 필요한 데이터를 반환해야 합니다.

        // AJAX 요청 예시 (jQuery 사용):
        var data = {page: nextPage};
        var datastr = JSON.stringify(data);
        
        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                var data = xhr.responseText;
    
                var obj = JSON.parse(data);
                var shoe = JSON.parse(obj.shoes);
                var likes = obj.likes;  // 멤버별 신발 좋아요 여부
                nextPage += 1;
                // alert();
                var html = '';
                for (var i = 0; i < shoe.length; i++) {
                    var shoe1 = shoe[i].fields;
                    var liked = likes[i];
                    html += '<div class="grid-box" data-value="' + shoe1.serialno + '">';
                    html += '<div class="grid-container"><div class="grid-img-box">';
                    html += '<div class="comment-icon"><label class="comment-icon-label"><span class="icon"></span></label></div>';
                    html += '<div class="commentCount-box"><p class="commentCount">0</p></div>';
                    html += '<div class="img-box" onclick="location.href = \'' + STATIC_FULL_URL + shoe1.serialno + '\'">';
                    html += '<img class="lazyload shoeimg" data-src="' + STATIC_IMAGES_URL + shoe1.shoename + shoe1.serialno + '0.jpeg"></div>';
                    html += '<div class="bookmark-icon">';
                    html += '<label class="bookmark-icon-label' + (liked ? ' on' : '') + '">';
                    html += '<span class="icon"></span></label></div>';
                    html += '<div class="shoelikecount-box"><p class="shoelikecount">' + shoe1.shoelikecount + '</p></div></div>';
                    html += '<div class="grid-shoename-box"><p class="shoename">' + shoe1.shoename + '</p></div>';
                    html += '<div class="grid-pubdate-box"><p class="pubdate">' + shoe1.pubdate + '</p></div>';
                    html += '<div class="grid-goBtn-box"><button class="goBtn" onclick="location.href = \'' + STATIC_FULL_URL + shoe1.serialno + '\'">바로가기</button></div>';
                    html += '</div></div>';
                }
                $('.infinite-container').append(html);

                $('.bookmark-icon-label').click(function() {
                    let $serialno = $(this).parent().parent().parent().parent().attr('data-value');
                
                    var $this = $(this);
                    var $count = $(this).parent().next().children();
                
                    var data = {serialnoAJAX: $serialno};
                    var datastr = JSON.stringify(data);
                
                    xhr = new XMLHttpRequest();
                    xhr.onreadystatechange = function() {
                        if (xhr.readyState == 4) {
                            var data = xhr.responseText;
                
                            var obj = JSON.parse(data);
                
                            if (obj.flag == '0') {
                                alert(obj.result_msg);
                                location.href = '/auth/login/';
                            } else {
                                if(obj.liked) {
                                    $this.addClass('on');
                                } else {
                                    $this.removeClass('on');
                                }
                                $count.text(obj.count);
                            }
                        }
                    };
                    xhr.open("POST", "likeShoe");
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    xhr.send(datastr);
                });

                if (typeof callback === 'function') {
                    callback();
                }
            }
        };
        xhr.open("POST", "");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(datastr);
    }

    $('.viewSort-icon-label').click(function () {
        if ($('.viewsort-filter-flex').hasClass('off')) {
            $('.viewsort-filter-flex').removeClass('off');
        } else {
            $('.viewsort-filter-flex').addClass('off');
        }
    });

});



