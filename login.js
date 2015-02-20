$(document).ready(function() {

    var token = generateToken();

    $("[name='username']").val('');
    $("[name='username']").focus();

    $('#login').submit(function(){
        $('[name=token]').val(token);
        console.log('re submit');
    })

    $('.reset').click(function(){
        $('[name=username]').val('');
        $("[name='username']").focus();
        $('[name=password]').val('');
    })

    function generateToken(){
        var token = "";
        var charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

        for( var i=0; i < 20; i++ ) {
            token += charset.charAt(Math.floor(Math.random() * charset.length));
        }

        return token;
    }

});
