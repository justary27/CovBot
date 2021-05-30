$(document).scroll(function () {
    var y = $(this).scrollTop();
    if (y > 1000) {
        $('.info').fadeIn();
        console.log(y)
    } else {
        $('.info').fadeOut();
    }

});