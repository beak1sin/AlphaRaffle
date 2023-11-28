$(document).ready(function() {
    // xpath = '/html/body/div/div/div/div[4]/div[1]/div[1]/div[2]/div/div[1]/div[4]/div/dl/div[1]/div[2]/div[1]/span[1]';
    // document.getElemtentById('test').contentWindow.document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    $("#test").on('load', function() {
        var elements = $(this).contents().find(".hidden .fixed");
        console.log(elements);
        alert(elements.val());
        var a = document.getElementById('test').contentWindow.document.querySelector(".hidden .fixed");
        console.log(a);
    });

    window.postMessage(data, [ports], 'https://editpdffree.com/')

    // 데이터 수신
    window.onmessage = function(e){
        if(e.origin === "http://127.0.0.1:8080"){
            // 처리
            console.log(e.origin);
        }
    }
});
