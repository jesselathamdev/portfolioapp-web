$(document).ready(function() {

    /* make entire row clickable */
    $('table.table-clickable tbody tr')
        .click(function() {
            var href = $(this).find("a").attr('href');

            if(href) {
                window.location = href;
            }
        });

});