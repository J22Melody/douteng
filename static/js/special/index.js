require(['jquery','handlebars'], function($){

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

    $('.J_comment_add').click(function(){
        var wrapper = $(this).closest('.addtion').next().toggleClass('none');
        // if($(this).hasClass('J_get_comment')){
        //     var source = wrapper.find('.comments-template').html();
        //     var template = Handlebars.compile(source);
        //     var context = {};
        //     $.ajax({
        //         type: 'GET',
        //         url: $(this).attr('href'), 
        //         async: false,
        //         success: function(result){
        //             if(result.success){
        //                 context['comments'] = result.comments;
        //             }
        //         }
        //     });
        //     var html = template(context);
        //     if(wrapper.hasClass('none')){
        //         wrapper.find('.comments').empty();
        //     }else{
        //         wrapper.find('.comments').html(html);
        //     } 
        // }
        return false;
    });

    $('.J_comment_new').submit(function(){
        var formData = new FormData($(this)[0]);
        $.ajax({ 
            data: formData,
            type: $(this).attr('method'), 
            url: $(this).attr('action'), 
            success: function(response) { 
                if(response.success){

                }
            },
            cache: false,
            contentType: false,
            processData: false
        });
        return false;
    });

    $('.J_comment_del').click(function(){
        if(!confirm('删除这条评论？')){
            return false;
        }
        var that = $(this);
        $.ajax({ 
            type: 'GET', 
            url: that.attr('href'), 
            success: function(response) { 
                if(response.success){
                    that.closest('.comment').animate({'opacity':0,'height':0,'margin-bottom':0},500,'swing',function(){
                        that.closest('.comment').remove();
                    });
                }
            }
        });
        return false;
    });
});