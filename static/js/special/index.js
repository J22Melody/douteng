require(['jquery'], function($){

    $('.showAll').click(function(){
        $(this).parent().addClass('none').prev().removeClass('none');
    });
    $('.packUp').click(function(){
        $(this).parent().addClass('none').next().removeClass('none');
    });

    $('.J_operation').click(function(){
        var that = $('a[href="'+ $(this).attr('href') +'"]');
        $.ajax({
            type: 'GET',
            url: that.attr('href'), 
            success: function(result){
                if(result.success){
                    that.html(result.text);
                    that.attr('href',result.href);
                    that.prev().html(result.num);
                }
            },
            error: function(result){
                if(result.status === 403){
                    //login_required
                    window.location = "/login?next="+location.pathname;
                }
            }
        });
        return false;
    });

    $('.add-comment').click(function(){
        $(this).closest('.addtion').next().toggleClass('none');
        return false;
    });
});