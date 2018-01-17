$('.wf-navbar').scrollspynav({
    className: {
        active: 'wf-navbar-btn-active'
    }
});
$(function(){
    function home_height () {
        var cover = $('.wf-cover');
        var element = $('.wf-cover-title');
        elemHeight = element.height();
        winHeight = $(window).height();
        cover_height = winHeight;
        if (cover_height >1440){
            cover_height = 1440;
        }
        element_padding = (cover_height - elemHeight - 200) /2;
        if (element_padding < 150 ) {
            element_padding = 150;
        }

        element.css('padding', element_padding+'px 0');
        cover.css('height', cover_height+'px');
        $('#explore').attr("data-am-smooth-scroll","{position: "+cover_height+"}");
    }
    home_height ();

    $(window).resize(function () {
        home_height ();
    });
});
