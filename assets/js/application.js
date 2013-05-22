$(function() {
  // Setup drop down menu
  $('.dropdown-toggle').dropdown();

  // Fix input element click problem
  $('.login-dropdown, #btn-login').click(function(e) {
    e.stopPropagation();
  });
});

// For floating/following main header on long pages
var fixed = false;

$(document).scroll(function() {
    if ($(this).scrollTop() > 70) {
        if( !fixed ) {
            fixed = true;
            $('#fixed-nav').addClass('fixed-navbar');
            $('#bottom').css('marginTop', '78px');
        }
    } else {
        if(fixed) {
            fixed = false;
            $('#fixed-nav').removeClass('fixed-navbar');
            $('#bottom').css('marginTop', '0px');
        }
    }
});