function testXhr(){
    if(window.XMLHttpRequest){
        var xhr=new XMLHttpRequest();
        console.log(xhr)
    }else{
        var xhr=new ActiveXObject('Microsoft.XMLHTTP')
    }
}