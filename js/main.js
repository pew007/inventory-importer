$(document).ready(function() {

    // Use DataTable to display products
    // DataTable provides sorting, search, and pagination
    // Source: http://www.datatables.net/
    $('.products_table').DataTable();

    $('[name="sku"]').focus();

    $("form[name='new_product'] #submit_button").click(function(){
        $('.form-error').remove();
        processForm();
    });

    $(document).on('click', '.delete', function(){
        var clickedElement = $(this);
        var container = clickedElement.closest('#productRecord');
        var sku = container.data('sku');

        processDelete(sku);
    });

    $(document).on('click', '.edit', function(){
        var clickedElement = $(this);
        var container = clickedElement.closest('#productRecord');
        var sku = container.data('sku');

        processEdit(sku);
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
                var emptyDataRow = $('.dataTables_empty');
                if (emptyDataRow) {
                    emptyDataRow.remove();
                };
                $('.products_table tbody').append(response.status);
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

            // Get number of records and if there was only 1 record left in the table
            // then display no data available after deletion
            var records = $('.products_table tbody tr');
            if (records.length == 1) {
                var emptyDataRow = "<td valign='top' colspan='12' class='dataTables_empty'>No data available in table</td>";
                $('.products_table tbody').append(emptyDataRow);
            };
        }, 'json').fail(function(){
            alert('Failed to delete record');
        })
    }

    function processEdit(sku) {
        var url = "/cgi-bin/fetch_product.cgi";
        var param = {sku: sku};

        $.post(url, param, function(data){
            console.log(data);
        }, 'json').fail(function(){
            alert('Failed to get record.');
        })
    }
});
