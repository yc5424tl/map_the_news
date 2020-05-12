
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


    if ($(window).width() > 1561) {
        alert('Width > 1561');
        lg_nav_div.css('display', 'flex');
        lg_nav_content.css('display', 'block');
        lg_nav_img.css('display', 'block');
        md_nav_div.css('display', 'none');
        md_nav_img.css('display', 'none');
        md_nav_div_desc('display', 'none');
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
    }

    if ($(window).width() < 1200) {
        alert('Width < 1200');
        md_nav_img_div.css('display', 'none');
        md_nav_img.css('display', 'none');
    }

};

