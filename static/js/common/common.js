//douteng
require(['jquery'], function($){
    $(window).scroll(function(){
        var top = $(window).scrollTop();
        if(top > 40){
            $('#search-wrapper').animate({'top':-100},{queue:false,duration:1200});
        }else{
            $('#search-wrapper').animate({'top':70},{queue:false,duration:1200});
        }
    });

    $(document).ready(function(){
        $(window).scrollTop(0);
    })
});