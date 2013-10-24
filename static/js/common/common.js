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
    });
});

//back-to-top

require(['jquery'], function($){
    $(window).scroll(function() {
        if($(window).scrollTop()>600){
            if($('.back-to-top').css('bottom') === '-20px'){
                $('.back-to-top').animate({bottom:"29px"});
            }
        }else{
            if($('.back-to-top').css('bottom') !== '-20px'){
                $('.back-to-top').css({bottom:'-20px'});
            }
        }
    });
});

