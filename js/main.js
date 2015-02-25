$(document).ready(function() {

    // Use DataTable to display products
    // DataTable provides sorting, search, and pagination
    // Source: http://www.datatables.net/
    $('.products_table').DataTable();

    $('[name="sku"]').focus();

    $(document).on('click', '.add_new_product', function(){
        var button = $(this);
        if (isFormValid()) {
            if (button.text() == 'Add Product') {
                processInsert();
            } else {
                processEdit();
            }
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

    $(document).on('click', '.reset', function(){
        resetForm();
    });

    function resetForm() {
        var form = $("form[name='new_product']");
        var button = $(".add_new_product");

        form.find("input").val('').attr('readonly', false);
        form.find("textarea").val('');
        form.find("select").val(1);
        form.find("img").hide();
        button.text('Add Product');
        $('.error_input').removeClass('error_input');
    }

    function isFormValid() {
        var form = $("form[name='new_product']");
        var serializedParams = $(form).serializeArray();
        var fieldsNotEmpty = true;
        var validSku = false;
        var validCost = false;
        var validRetail = false;
        var isValid = false;

        $.each(serializedParams, function(index, field){
            var currentField = $("*[name='" + field.name + "']");
            // Check for empty input
            if (field.value == '') {
                fieldsNotEmpty = false;
                currentField.addClass('error_input');
                currentField.attr('placeholder', 'Required');
            } else { // Validate SKU, Cost, Retail
                currentField.removeClass('error_input');
                if (field.name == 'sku') {
                    validSku = isValidSku(field);
                }

                if (field.name == 'cost') {
                    validCost = isValidCurrency(field);
                }

                if (field.name == 'retail') {
                    validRetail = isValidCurrency(field);
                }
            }
        });

        if ( validSku && validCost && validRetail && fieldsNotEmpty ) {
            isValid = true;
        }

        return isValid;
    }

    function isValidSku(field) {
        var currentField = $("*[name='" + field.name + "']");
        if (field.value.match(/^[A-Z]{3}-{1}[0-9]{3}$/)) {
            return true;
        } else {
            currentField.addClass('error_input');
            currentField.val('Invalid SKU format');
            return false;
        }
    }

    function isValidCurrency(field) {
        var currentField = $("*[name='" + field.name + "']");
        if (field.value.match(/^[0-9]{0,}(\.[0-9]{2})?$/)) {
            return true;
        } else {
            currentField.addClass('error_input');
            currentField.val('Invalid currency format');
            return false;
        }
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
            $("#product-image").attr('src', image_url).show();

            button.text('Update Product');

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
