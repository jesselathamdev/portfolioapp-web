$(document).ready(function() {
    $.fn.digits = function(){
        return this.each(function(){
            $(this).text( $(this).text().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,") );
        })
    }

    var total_book_value = 0.00;
    var total_market_value = 0.00;
    var total_net_gain_dollar = 0.00;

    $('#holdings tbody tr').each(function() {
        total_book_value += parseFloat($(this).find('td:nth-child(4)').text().replace('$', '').replace(',', ''));
        total_market_value += parseFloat($(this).find('td:nth-child(5)').text().replace('$', '').replace(',', ''));
        total_net_gain_dollar += parseFloat($(this).find('td:nth-child(6)').text().replace('$', '').replace(',', ''));
    });

    $('#holdings tfoot tr.cash').each(function() {
        total_book_value += parseFloat($(this).find('td:nth-child(4)').text().replace('$', '').replace(',', ''));
        total_market_value += parseFloat($(this).find('td:nth-child(5)').text().replace('$', '').replace(',', ''));
    });

    $('#total_book_value').html('$' + total_book_value.toFixed(2)).digits();
    $('#total_market_value').html('$' + total_market_value.toFixed(2)).digits();
    $('#total_net_gain_dollar').html('$' + total_net_gain_dollar.toFixed(2)).digits();

    if (total_net_gain_dollar.toFixed(2) > 0) {
        $('#total_net_gain_dollar').addClass('indicator-gain')
    }
    else if (total_net_gain_dollar.toFixed(2) < 0 ) {
        $('#total_net_gain_dollar').addClass('indicator-loss')
    }

    $('#holdings tbody tr').each(function() {
        $(this).find('.makeup').text((parseFloat($(this).find('td:nth-child(5)').text().replace('$', '').replace(',', ''))/total_market_value * 100).toFixed(2) + '%');
    });

    $('#holdings tfoot tr.cash').each(function() {
        $(this).find('.makeup').text((parseFloat($(this).find('td:nth-child(5)').text().replace('$', '').replace(',', ''))/total_market_value * 100).toFixed(2) + '%');
    });

    $('table.table-clickable tbody tr')
        .click(function() {
            var href = $(this).find("a").attr("href");
            if(href) {
                window.location = href;
            }
        });

    $('table.table-clickable .table-context-menu a')
            .click(function(e) {
                e.preventDefault();

                var portfolio_id = $(this).data('portfolio-id');
                var holding_id = $(this).data('holding-id');
                var holding_name = $(this).data('name');
                $('#portfolio_id').val(portfolio_id);
                $('#holding_id').val(holding_id);
                $('#holding_name').html(holding_name);
                $('#modalDelete').modal('show');
                $('#modalDeleteButton').attr('href', '/portfolios/'+portfolio_id+'/holdings/'+holding_id+'/delete');
            });

    $(document).bind({
        keydown: function(e) {
            if (e.keyCode == 27) {
                $('table.table-clickable tbody tr .row-options')
                    .find('.table-context-menu').toggle().hide();
            }
        },
        click: function(e) {
            $('table.table-clickable tbody tr .row-options')
                .find('.table-context-menu').toggle().hide();
        }
    });

    $('table.table-clickable tbody tr .row-options')
        .bind('click', function(e) {return false})
        .click(function(e){
            e.stopPropagation();
            $(this).find('.table-context-menu').toggle();
            $(this).parent().siblings().find('.table-context-menu').toggle().hide();
        });

    $('#stock_display')
        .autocomplete({
            source: '/api/markets/stocks',
            minLength: 2,
            autoFocus: true,
            delay: 200,
            select:function(event,ui){
                $("#id_stock").val(ui.item.id)
            }
        })
        .data('uiAutocomplete')
        ._renderItem = function(ul, item){
            item.label = item.label.replace(new RegExp("(?![^&;]+;)(?!<[^<>]*)(" + $.ui.autocomplete.escapeRegex(this.term) + ")(?![^<>]*>)(?![^&;]+;)", "gi"), "<strong>$1</strong>");

            return $("<li></li>")
                .data("item.autocomplete", item)
                .append("<a>" + item.label + "</a>")
                .appendTo(ul);
        };
});