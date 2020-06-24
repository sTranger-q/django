// $().ready(function(){
//     $('.grade a').on('click',function(){
//         $('.grade a').removeClass('text-danger');
//         $(this).addClass('text-danger');
//     })
//     $('.campus a').on('click',function(){
//         $('.campus a').removeClass('text-danger');
//         $(this).addClass('text-danger');
//     })
// })
$().ready(function () {
    $('nav a').on('click', function () {
        // 找祖先元素
        var parents = $(this).parents('.grade');
        if (parents.length) {
            $('.grade a').removeClass('text-danger');
        } else {
            $('.campus a').removeClass('text-danger');
        }
        $(this).addClass('text-danger');
    })
})
$(document).on('scroll', function () {
    var scrollH = $(document).height();
    var scrollT = Math.ceil($(document).scrollTop());
    var clientH = $(window).height();
    var newE= $( `
    <div class="row">
    <div class="col-md-3 col-sm-6 col-xs-6">
        <a href="#" class="thumbnail">
            <img src="./img/news-img-1.jpg" class='img-responsive' alt="">    
            <p class="text-muted">优秀作品</p>
        </a>
        
    </div>
    <div class="col-md-3 col-sm-6 col-xs-6">
        <a href="#" class="thumbnail">
            <img src="./img/news-img-1.jpg" class='img-responsive' alt="">    
            <p class="text-muted">优秀作品</p>
        </a>
    
    </div>
    <div class="col-md-3 col-sm-6 col-xs-6">
        <a href="#" class="thumbnail">
            <img src="./img/news-img-1.jpg" class='img-responsive' alt="">    
            <p class="text-muted">优秀作品</p>
        </a>
    
    </div>
    <div class="col-md-3 col-sm-6 col-xs-6">
        <a href="#" class="thumbnail">
            <img src="./img/news-img-1.jpg" class='img-responsive' alt="">    
            <p class="text-muted">优秀作品</p>
        </a>
    </div>
    </div>
    <div class="row">
    <div class="col-md-3 col-sm-6 col-xs-6">
        <a href="#" class="thumbnail">
            <img src="./img/news-img-2.jpg" class='img-responsive' alt="">    
            <p class="text-muted">优秀作品</p>
        </a>
        
    </div>
    <div class="col-md-3 col-sm-6 col-xs-6">
        <a href="#" class="thumbnail">
            <img src="./img/news-img-2.jpg" class='img-responsive' alt="">    
            <p class="text-muted">优秀作品</p>
        </a>
    
    </div>
    <div class="col-md-3 col-sm-6 col-xs-6">
        <a href="#" class="thumbnail">
            <img src="./img/news-img-2.jpg" class='img-responsive' alt="">    
            <p class="text-muted">优秀作品</p>
        </a>
    
    </div>
    <div class="col-md-3 col-sm-6 col-xs-6">
        <a href="#" class="thumbnail">
            <img src="./img/news-img-2.jpg" class='img-responsive' alt="">    
            <p class="text-muted">优秀作品</p>
        </a>
    </div>
    </div>
    <div class="row">
    <div class="col-md-3 col-sm-6 col-xs-6">
        <a href="#" class="thumbnail">
            <img src="./img/news-img-3.jpg" class='img-responsive' alt="">    
            <p class="text-muted">优秀作品</p>
        </a>
        
    </div>
    <div class="col-md-3 col-sm-6 col-xs-6">
        <a href="#" class="thumbnail">
            <img src="./img/news-img-3.jpg" class='img-responsive' alt="">    
            <p class="text-muted">优秀作品</p>
        </a>
    
    </div>
    <div class="col-md-3 col-sm-6 col-xs-6">
        <a href="#" class="thumbnail">
            <img src="./img/news-img-3.jpg" class='img-responsive' alt="">    
            <p class="text-muted">优秀作品</p>
        </a>
    
    </div>
    <div class="col-md-3 col-sm-6 col-xs-6">
        <a href="#" class="thumbnail">
            <img src="./img/news-img-3.jpg" class='img-responsive' alt="">    
            <p class="text-muted">优秀作品</p>
        </a>
    </div>
    </div>
    `)

    if (scrollH-scrollT - clientH<=150) {
        $('.add').append(newE);
    }

})
