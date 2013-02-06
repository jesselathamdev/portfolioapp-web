$(document).ready(function(){
  $('#stocks').focus();
});

// creates custom HTML in lookup list; also solves for custom autocomplete functionality across all autocompletes on a page rather than just one
// taken from http://stackoverflow.com/questions/2435964/jqueryui-how-can-i-custom-format-the-autocomplete-plug-in-results


// simple example, no modification of returned results
$(function(){
  $('#stocks').autocomplete({
    source: '/api/markets/stocks',
    minLength: 2,
    autoFocus: true,
    delay: 200
  });
});

// more complex which customizes the results in the select
$(function(){
  $('#stocks').autocomplete({
    source: '/api/markets/stocks',
    minLength: 2,
    autoFocus: true,
    delay: 200
  })
  .data('uiAutocomplete')._renderItem = function(ul, item){
    item.label = item.label.replace(new RegExp("(?![^&;]+;)(?!<[^<>]*)(" + $.ui.autocomplete.escapeRegex(this.term) + ")(?![^<>]*>)(?![^&;]+;)", "gi"), "<strong>$1</strong>");

    return $("<li></li>")
      .data("item.autocomplete", item)
      .append("<a>" + item.label + "</a>")
      .appendTo(ul);
  };
});
