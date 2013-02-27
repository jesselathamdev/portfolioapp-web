$(document).ready(function() {
    $('table.table-clickable tbody tr')
        .click(function() {
            var href = $(this).find("a").attr('href');
            if(href) {
                window.location = href;
            }
        });

    $('table.table-clickable .table-context-menu a')
            .click(function(e) {
                e.preventDefault();

                var portfolio_id = $(this).data('id');
                var portfolio_name = $(this).data('name');
                $('#portfolio_id').val(portfolio_id);
                $('#portfolio_name').html(portfolio_name);
                $('#modalDelete').modal('show');
                $('#modalDeleteButton').attr('href', '/portfolios/'+portfolio_id+'/delete');

            });

    $('#modalCreate').on('shown', function() {
        $('#id_name').focus();
    });

    $(document).bind({
        keydown: function(e) {
            if (e.keyCode == 27) {
                $('table.table-clickable tbody tr .row-options').find('.table-context-menu').toggle().hide();
            }
        },
        click: function(e) {
            $('table.table-clickable tbody tr .row-options').find('.table-context-menu').toggle().hide();
        }
    });

    $('table.table-clickable tbody tr .row-options')
        .bind('click', function(e) {return false})
        .click(function(e){
            e.stopPropagation();
            $(this).find('.table-context-menu').toggle();
            $(this).parent().siblings().find('.table-context-menu').toggle().hide();
        });
});