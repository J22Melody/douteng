
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

// 赞、关注等操作

require(['jquery'], function($){
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
});

//comment

require(['jquery','handlebars'], function($){
    $('.J_comment_add').click(function(){
        $(this).find('.icons-upArrow').toggleClass('none');
        $(this).closest('.addtion').next().toggleClass('none');
        return false;
    });

    $('.J_comment_new').submit(function(){
        var formData = new FormData($(this)[0]);
        var that = $(this);
        if(that.find('input[name="content"]').val().length === 0){
            return false;
        }
        $.ajax({ 
            data: formData,
            type: that.attr('method'), 
            url: that.attr('action'), 
            success: function(result) { 
                if(result.success){
                    var source = $('.comment-template').html();
                    var template = Handlebars.compile(source);
                    var context = {'comment':result.comment[0]['fields'],'create_time':result.create_time,'target_username':result.target_username,'comment_id':result.comment_id,'username':result.username,'user_id':result.user_id,"father_type":result.father_type};
                    var html = template(context);
                    that.closest('.comments-wrapper').find('.comments').append(html);
                    that.find('input[name="content"]').val('');
                    that.prev().find('.no-comment').remove();
                }
            },
            cache: false,
            contentType: false,
            processData: false
        });
        return false;
    });

    $('body').on('click','.J_comment_del',function(){
        if(!confirm('删除这条评论？')){
            return false;
        }
        var that = $(this);
        $.ajax({ 
            type: 'GET', 
            url: that.attr('href'), 
            success: function(result) { 
                if(result.success){
                    that.closest('.comment').animate({'opacity':0,'height':0,'margin-bottom':0},500,'swing',function(){
                        that.closest('.comment').remove();
                    });
                }
            }
        });
        return false;
    });
});

