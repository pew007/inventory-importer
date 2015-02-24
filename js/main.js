$(document).ready(function() {

    $('.products_table').DataTable();
    $('[name="sku"]').focus();

    $("form[name='new_product'] #submit_button").click(function(){
        $('.form-error').remove();
        processForm();
    });

    $(".delete").click(function(){
        var clickedElement = $(this);
        var container = clickedElement.closest('#productRecord');
        var sku = container.data('sku');

        processDelete(sku);
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
            processInsert();
        };
    }

    function processInsert() {
        var url = "/cgi-bin/insert.cgi";
        var form_data = new FormData($('form[name=new_product]')[0]);

        $.ajax( {
            url: url,
            type: "post",
            data: form_data,
            processData: false,
            contentType: false,
            success: function(response) {
               console.log(response);
            },
            error: function(response) {}
        });
    }

    function processDelete(sku) {
        var url = "/cgi-bin/delete.cgi";
        var param = {sku: sku};

        $.post(url, param, function(data){
            var record = $("tr[data-sku='" + sku + "']");
            record.remove();
        }, 'json').fail(function(){
            alert('Failed to delete record');
        })
    }
});
