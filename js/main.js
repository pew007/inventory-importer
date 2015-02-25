$(document).ready(function() {

    // Use DataTable to display products
    // DataTable provides sorting, search, and pagination
    // Source: http://www.datatables.net/
    $('.products_table').DataTable();

    $('[name="sku"]').focus();

    $(document).on('click', '.add_new_product', function(){
        var button = $(this);

        if (button.val() == 'Add Product') {
            $('.form-error').remove();
            processForm();
        } else {
            processEdit();
        }
    })

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

        fetchProductInfo(sku);
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
                currentField.after("<span class='form-error'>");
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
            if (records.length == 0) {
                var emptyDataRow = "<td valign='top' colspan='12' class='dataTables_empty'>No data available in table</td>";
                $('.products_table tbody').append(emptyDataRow);
            };
        }, 'json').fail(function(){
            alert('Failed to delete record');
        })
    }

    function fetchProductInfo(sku) {
        var container = $("#productRecord[data-sku='" + sku + "']");
        var url = "/cgi-bin/fetch_product.cgi";
        var param = {sku: sku};

        $.post(url, param, function(data){
            var product = data.result[0];
            var image_url = "/_p_images/" + product.image;
            var button = $('.add_new_product');

            $("input[name='sku']").val(product.sku).attr('readonly', true);
            $("select[name='category']").val(product.categoryID);
            $("select[name='vendor']").val(product.vendorID);
            $("select[name='platform']").val(product.platformID);
            $("input[name='vendorModel']").val(product.vendorModel);
            $("input[name='cost']").val(product.cost);
            $("input[name='retail']").val(product.retail);
            $("textarea[name='description']").val(product.description);
            $("textarea[name='features']").val(product.features);
            $("#product-image").attr('src', image_url).removeClass('hide');

            button.val('Update Product');

        }, 'json').fail(function(){
            alert('Failed to get record.');
        })
    }

    function processEdit() {
        var url = "/cgi-bin/edit.cgi";
        var form_data = new FormData($('form[name=new_product]')[0]);

        $.ajax( {
            url: url,
            type: "post",
            data: form_data,
            processData: false,
            contentType: false,
            success: function(response) {
                var sku = $('[name="sku"]').val();
                var newRow = response.result;
                var currentRow = $("#productRecord[data-sku='" + sku + "']");
                currentRow.replaceWith(newRow);
            },
            error: function(response) {}
        });
    }

});
