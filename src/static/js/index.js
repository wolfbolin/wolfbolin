console.log(
    " __          __   _  __ ____        _ _  \n" +
    " \\ \\        / /  | |/ _|  _ \\      | (_)  \n" +
    "  \\ \\  /\\  / /__ | | |_| |_) | ___ | |_ _ __  \n" +
    "   \\ \\/  \\/ / _ \\| |  _|  _ < / _ \\| | | '_ \\  \n" +
    "    \\  /\\  / (_) | | | | |_) | (_) | | | | | |  \n" +
    "     \\/  \\/ \\___/|_|_| |____/ \\___/|_|_|_| |_|  \n" +
    "=================================================");
console.log("Welcome to WolfBolin.com ~ \nContact me at: mailto@wolfbolin.com");
$(function() {
    function cover_screen() {
        let exploreBtn = $("#explore");
        let coverTitle = $("#cover-title");
        let clientHeight = document.documentElement.clientHeight;
        let titleHeight = coverTitle.height();
        let titlePadding = (clientHeight - titleHeight) / 2;
        coverTitle.css("padding", titlePadding + "px 0");
        exploreBtn.click(function () {
            $(window).scrollTo(clientHeight - 60, 400);
        })
    }
    cover_screen();
    $(window).resize(function () {
        cover_screen();
    });
});
