require(['jquery'], function($){
    $('.showAll').click(function(){
        $(this).parent().addClass('none').prev().removeClass('none');
    });
    $('.packUp').click(function(){
        $(this).parent().addClass('none').next().removeClass('none');
    });
});