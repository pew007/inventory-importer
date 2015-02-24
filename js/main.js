$(document).ready(function() {

    $('.products_table').DataTable();
    $('[name="sku"]').focus();

    $("form[name='new_product'] #submit_button").click(function(){
        $('.form-error').remove();
        processForm();
    });

    function processForm() {
        var form = $("form[name='new_product']");
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

        if (inputValid) {
            processUpload();
        };
    }

    function processUpload() {
        var url = "/cgi-bin/upload.cgi";
        var form_data = new FormData($('form[name=new_product]')[0]);

        $.ajax( {
            url: url,
            type: "post",
            data: form_data,
            processData: false,
            contentType: false,
            success: function(response) {
               // $('#status').css('color','blue');
               // $('#status').html("Your file has been received.");
               // var fname = $("#product_image").val().toLowerCase();
               // var toDisplay = "<img src=\"/~jadrn000/proj1_examples/ajax_upload/_p_images/" + fname + "\" />";
               // $('#pic').html(toDisplay);
               console.log(response);
            },
            error: function(response) {

            }
        });
    }
});
