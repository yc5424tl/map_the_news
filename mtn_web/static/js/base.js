// $('').addClass('');

$(document).ready(setLayout);
$(window).resize(setLayout);

setLayout = function() {
    let md_nav_div = $('#md-nav-div');
    let lg_nav_div = $('#lg-nav-div');
    let lg_nav_img = $('#lg-nav-img');
    let lg_nav_content = $('#nav-content-lg');
    let md_nav_img_div = $('#md-nav-img-div');
    let md_nav_col_div = $('#md-nav-col-div');
    let md_nav_div_desc = $('#md-nav-div *');
    let md_nav_img = $('#md-nav-img');
    // let md_nav_div = $('#md-nav-div');
    // let md_nav_img_div = $('#md-nav-img-div');
    // let md_nav_img = $('#md-nav-img');
    // let nav_left = $('#nav-lft');
    // let nav_ctr = $('#nav-ctr');
    // let nav_right = $('#nav-rgt');
    // let nav_img = $('#nav-img');
    // let nav = $('nav');

    if ($(window).width() > 1561) {
        alert('Width > 1561');
        lg_nav_div.css('display', 'flex');
        lg_nav_content.css('display', 'block');
        lg_nav_img.css('display', 'block');
        md_nav_div.css('display', 'none');
        md_nav_img.css('display', 'none');
        md_nav_div_desc('display', 'none');
        // // nav.css('height', '30vh');
        // md_nav_div.css('display', 'none');
        // md_nav_img_div.css('display', 'none');
        // md_nav_img.css('display', 'none');
        // nav_ctr.css('display', 'initial');
        // nav_img.css('display', 'initial');
        // if (nav_left.hasClass('col-auto')) {
        //     nav_left.removeClass('col-auto').addClass('col-4');
        //     nav_right.removeClass('col-auto').addClass('col-4');
        //     nav_ctr.removeClass('col-0').addClass('col-4');
        // }
    }

    if ($(window).width() < 1562) {
        alert('Width < 1562');
        lg_nav_div.css('display', 'none');
        lg_nav_img.css('display', 'none');
        lg_nav_content.css('display', 'none');
        md_nav_div.css('display', 'flex');
        md_nav_div_desc('display', 'unset');
        md_nav_col_div.css('display', 'block');
        md_nav_img.css('display', 'block');
        // nav.css('height', '24vh');
        // md_nav_div.css('display', 'initial');
        // md_nav_img_div.css('display', 'initial');
        // md_nav_img.css('display', 'initial');
        // nav_ctr.css('display', 'none');
        // nav_img.css('display', 'none');
        // if (nav_left.hasClass('col-4')) {
        //     nav_left.removeClass('col-4').addClass('col-auto');
        //     nav_right.removeClass('col-4').addClass('col-auto');
        //     nar_ctr.removeClass('col').addClass('col-0');
        // }
    }

    if ($(window).width() < 1200) {
        alert('Width < 1200');
        md_nav_img_div.css('display', 'none');
        md_nav_img.css('display', 'none');
    }

};

// setLayout = function() {
//
//     let top_img_div = $('#top-nav-img-div');
//     let nav_left = $('#nav-lft');
//     let nav_ctr = $('#nav-ctr');
//     let nav_right = $('#nav-rgt');
//     let nav_img = $('#nav-img');
//
//     if (window.width() < 1562) {
//         top_img_div.show();
//         nav_ctr.hide();
//         nav_img.css('top', 0);
//         nav_img.hide();
//         if (nav_left.hasClass('col-4')) {
//             nav_right.removeClass('col-4').addClass('col');
//             nav_left.removeClass('col-4').addClass('col');
//         }
//     }
//
//     else if (window.width() > 1561) {
//         top_img_div.hide();
//         nav_ctr.show();
//         nav_img.show();
//         if (nav_img.css('top').equals(0)) {
//             nav_img.css('top', '-12vh');
//         }
//         if (nav_left.hasClass('col')) {
//             nav_right.removeClass('col').addClass('col-4');
//             nav_left.removeClass('col').addClass('col-4');
//
//         }
//     }
// };
//
// $(window).on('resize', setLayout);
// $(document).on('load', setLayout);