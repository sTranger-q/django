function createXhr(){
    if(window.XMLHttpRequest){
        var xhr=new XMLHttpRequest();
        
    }else{
        var xhr=new ActiveXObject('Microsoft.XMLHTTP');
    }
    return xhr;
}

function getXhr(){
    var xhr=createXhr();
    xhr.open('GET','/test_xhr_get_server',true);
    xhr.onreadystatechange=function(){
        if(xhr.readyState==4&&xhr.status==200){
            var div=document.getElementById('show');
            div.innerHTML=xhr.responseText;
            // 增加计时器，限制按钮点击次数
        }
    }
    xhr.send(null);
}