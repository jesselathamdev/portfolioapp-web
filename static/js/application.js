$(function() {
  // Setup drop down menu
  $('.dropdown-toggle').dropdown();

  // Fix input element click problem
  $('.login-menu, #btn-login').click(function(e) {
    e.stopPropagation();
  });


});