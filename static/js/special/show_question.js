require(['jquery'], function($){

    $('.J_answerForm').submit(function(){
        var value = tinyMCE.get('answer-textarea').getContent();
        if(value.length === 0){
            return false;
        }
        return true;
    });

});