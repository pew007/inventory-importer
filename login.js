$(document).ready(function() {

    $("[name='username']").val('');
    $("[name='username']").focus();

    $('.reset').click(function(){
        $('[name=username]').val('');
        $("[name='username']").focus();
        $('[name=password]').val('');
    })

});
