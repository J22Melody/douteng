require(['jquery'], function($){

    $('.showAll').click(function(){
        $(this).parent().addClass('none').prev().removeClass('none');
    });
    $('.packUp').click(function(){
        $(this).parent().addClass('none').next().removeClass('none');
    });

    $('.J_operation').click(function(){
        var that = $(this);
        $.get(that.attr('href'), function(result){
            if(result.success){
                that.html(result.text);
                that.attr('href',result.href);
                that.prev().html(result.num);
            }      
        });
        return false;
    })
});