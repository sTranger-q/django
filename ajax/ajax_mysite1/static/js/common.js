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
    xhr.open('GET','/test_xhr_get_server',true)
}