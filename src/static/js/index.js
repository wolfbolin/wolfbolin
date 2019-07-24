$(function() {
    function cover_screen() {
        $('.cover-title').css('padding', '0');
        clientHeight = document.documentElement.clientHeight;
        console.log(clientHeight)
        titleHeight = $('.cover-title').height();
        titlePadding = (clientHeight - titleHeight) / 2;
        $('.cover-title').css('padding', titlePadding + 'px 0');
        $('#explore').attr("data-am-smooth-scroll", "{position: " + (clientHeight - 60) + "}");
    }
    cover_screen();
    $(window).resize(function() {
        cover_screen();
    });
});