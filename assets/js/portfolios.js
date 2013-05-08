$(document).ready(function() {
    $.fn.digits = function(){
        return this.each(function(){
            $(this).text( $(this).text().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,") );
        })
    }

    var total_holding_count = 0;
    var total_book_value = 0.00;
    var total_market_value = 0.00;
    var total_net_gain_dollar = 0.00;

    $('#portfolios tbody tr').each(function() {
        total_holding_count += parseInt($(this).find('td:nth-child(2)').text());
        total_book_value += parseFloat($(this).find('td:nth-child(3)').text().replace('$', '').replace(',', ''));
        total_market_value += parseFloat($(this).find('td:nth-child(4)').text().replace('$', '').replace(',', ''));
        total_net_gain_dollar += parseFloat($(this).find('td:nth-child(5)').text().replace('$', '').replace(',', ''));
    });

    $('#total_holding_count').html(total_holding_count);
    $('#total_book_value').html('$' + total_book_value.toFixed(2)).digits();
    $('#total_market_value').html('$' + total_market_value.toFixed(2)).digits();
    $('#total_net_gain_dollar').html('$' + total_net_gain_dollar.toFixed(2)).digits();

    if (total_net_gain_dollar.toFixed(2) > 0) {
        $('#total_net_gain_dollar').addClass('indicator-gain')
    }
    else if (total_net_gain_dollar.toFixed(2) < 0 ) {
        $('#total_net_gain_dollar').addClass('indicator-loss')
    }

    /* make entire row clickable */
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