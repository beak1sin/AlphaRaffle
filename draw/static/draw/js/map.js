$(document).ready(function() {
    var mapOptions = {
        center: new naver.maps.LatLng(37.554722, 126.970833),
        zoom: 10,
        zoomControl: true,
        zoomControlOptions: {
            style: naver.maps.ZoomControlStyle.SMALL,
            position: naver.maps.Position.TOP_RIGHT
        }
    };
    var map = new naver.maps.Map('map', mapOptions);

    var $firstAddress = $('.address-items.on').find('.small-text').eq(1).text();
    var apiUrl = `${window.location.protocol}//${window.location.host}/auth/details/map/api/get_geocode/?query=${encodeURIComponent($firstAddress)}`;
    // console.log(apiUrl);
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            // 네이버 API의 응답 처리
            console.log(data);
            var x = data.addresses[0].x; // 경도
            var y = data.addresses[0].y; // 위도
            var location = new naver.maps.LatLng(y, x);
            // var marker = new naver.maps.Marker({
            //     position: location,
            //     map: map
            // });
            var currentHost = window.location.protocol + "//" + window.location.hostname + (window.location.port ? ':' + window.location.port : '');
            placeImageMarker(x, y, currentHost + '/static/draw/images/jordan1OFF.avif');
            map.setCenter(location); // 해당 위치로 지도 중심 이동
            // // map.panTo(location);
            map.setZoom(17); // 지도 확대 수준 설정
        })
        .catch(error => {
            console.error("Error fetching geocode:", error);
    });

    // var marker = new naver.maps.Marker({
    //     position: new naver.maps.LatLng(37.554722, 126.970833),
    //     map: map
    // });

    // 주소 검색 API 호출
    function searchAddressToCoordinate(address) {
        // Client ID와 Client Secret 키를 네이버 개발자 센터에서 발급받아 입력해주세요.
        var clientId = 'f7pin7r31a';
        var clientSecret = 'lULMysuFlNCXBkmF4TjdouyHi8oZEmPR4oCbKpct';

        // API 요청 URL
        var apiURL = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query=' + encodeURI(address);
        console.log(apiURL);
        // AJAX 요청
        $.ajax({
            method: "GET",
            url: apiURL,
            headers: {
                "X-NCP-APIGW-API-KEY-ID": clientId,
                "X-NCP-APIGW-API-KEY": clientSecret
            },
            success: function(response) {
                if (response.status === 'OK') {
                    var x = response.addresses[0].x; // 경도
                    var y = response.addresses[0].y; // 위도
                    alert('성공 ');
                    // 해당 위치에 지도 마커 표시나 다른 작업 수행
                    var mapOptions = {
                        center: new naver.maps.LatLng(x, y),
                        zoom: 10
                    };
                    var map = new naver.maps.Map('map', mapOptions);
                } else {
                    console.error("주소를 찾지 못했습니다.");
                }
            },
            error: function(xhr, status, error) {
                console.error("주소 검색 요청 실패:", error);
            }
        });
    }
    
    $('.address-items').click(function() {
        $('.address-items').removeClass('on');
        $(this).addClass('on');
        var address = $(this).find('.small-text').eq(1).text();
        // var apiUrl = "http://127.0.0.1:8000/api/get_geocode/?query=" + encodeURIComponent(address);
        var apiUrl = `${window.location.protocol}//${window.location.host}/auth/details/map/api/get_geocode/?query=${encodeURIComponent(address)}`;
        console.log(apiUrl);
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                // 네이버 API의 응답 처리
                console.log(data);
                var x = data.addresses[0].x; // 경도
                var y = data.addresses[0].y; // 위도
                var location = new naver.maps.LatLng(y, x);
                // var marker = new naver.maps.Marker({
                //     position: location,
                //     map: map
                // });
                var currentHost = window.location.protocol + "//" + window.location.hostname + (window.location.port ? ':' + window.location.port : '');
                placeImageMarker(x, y, currentHost + '/static/draw/images/jordan1OFF.avif');
                map.setCenter(location); // 해당 위치로 지도 중심 이동
                // map.panTo(location);
                map.setZoom(17); // 지도 확대 수준 설정
            })
            .catch(error => {
                console.error("Error fetching geocode:", error);
        });
    });

    function placeImageMarker(x, y, imageUrl) {
        var location = new naver.maps.LatLng(y, x);
        var marker = new naver.maps.Marker({
            position: location,
            map: map,
            icon: {
                url: imageUrl, // 마커 이미지 URL
                // size: new naver.maps.Size(ORIGINAL_IMAGE_WIDTH, ORIGINAL_IMAGE_HEIGHT),
                scaledSize: new naver.maps.Size(25, 25),
                origin: new naver.maps.Point(0, 0), // 이미지의 시작점
                anchor: new naver.maps.Point(25, 25) // 이미지 중심점 설정
            }
        });
    }
});