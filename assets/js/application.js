$(function() {
    // Setup drop down menu
    $('.dropdown-toggle').dropdown();

    // Fix input element click problem
    $('.login-dropdown, #btn-login').click(function(e) {
        e.stopPropagation();
    });
});

// For floating/following main header on long pages
var distanceToTop = 0;
var fixed = false;

$(document).ready(function(){
    distanceToTop = $('#bottom').offset().top;  // 112px for unauth'd home, 128px for auth'd dashboard, 148px for auth'd page with breadcrumbs
});

$(document).scroll(function() {
    if ($(this).scrollTop() > 70) {  // this is the height of the header above the main navigation
        if(!fixed) {
            fixed = true;
            $('#fixed-nav').addClass('fixed-navbar');
            if (distanceToTop == 112) {
                $('#bottom').css('marginTop', '41px');  // 78px  // 58px for dashboard page // 41px for unauth'd home
            } else if (distanceToTop == 128) {
                $('#bottom').css('marginTop', '58px');
            } else if (distanceToTop == 148) {
                $('#bottom').css('marginTop', '78px');
            }
        }
    } else {
        if(fixed) {
            fixed = false;
            $('#fixed-nav').removeClass('fixed-navbar');
            $('#bottom').css('marginTop', '0px');
        }
    }
});