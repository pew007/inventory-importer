$(document).ready(function() {

    $("#tabs").tabs();

    $('[name="sku"]').focus();

    $("form[name='new_product'] #submit_button").click(function(){
        $('.form-error').remove();
        validateForm();
    });

    function validateForm() {
        var form = $("form[name='new_product']");
        // var url = 'http://jadran.sdsu.edu/perl/jadrn048/proj1/validate.cgi';
        var url = "/cgi-bin/validate.cgi";
        var serializedParams = $(form).serializeArray();
        var params = {};

        var inputValid = true;
        $.each(serializedParams, function(index, field){
            var currentField = $("*[name='" + field.name + "']");
            if (field.value == '') {
                inputValid = false;
                currentField.addClass('error-field');
                currentField.after("<span class='form-error'> <-- This field is required</span>");
            } else {
                currentField.removeClass('error-field');
                params[field.name] = field.value;
            }
        });

        params['image'] = $('#image')[0].files[0];
        console.log(params);
        if (inputValid) {
            $.post(url, params, function(data){
                console.log(data);
            }, 'json').fail(function(){
                console.log('failed');
            });
        };
    }
});
