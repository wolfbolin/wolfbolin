console.log(
    " __          __   _  __ ____        _ _  \n" +
    " \\ \\        / /  | |/ _|  _ \\      | (_)  \n" +
    "  \\ \\  /\\  / /__ | | |_| |_) | ___ | |_ _ __  \n" +
    "   \\ \\/  \\/ / _ \\| |  _|  _ < / _ \\| | | '_ \\  \n" +
    "    \\  /\\  / (_) | | | | |_) | (_) | | | | | |  \n" +
    "     \\/  \\/ \\___/|_|_| |____/ \\___/|_|_|_| |_|  \n" +
    "=================================================");
console.log("Welcome to WolfBolin.com ~ \nContact me at: mailto@wolfbolin.com");
$(function () {
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

    function timeline() {
        let fatherWidth = $(".wb-timeline").width();
        console.log(fatherWidth);
        if (fatherWidth >= 960) {
            fatherWidth = 960;
        }
        if (fatherWidth > 660) {
            $(".tl-timeline").css("width", fatherWidth + "px");
            $(".tl-direction-r").css("width", (fatherWidth / 2 - 30) + "px");
            $(".tl-direction-l").css("width", (fatherWidth / 2 - 30) + "px");
        }else{
            $(".tl-timeline").css("width", "");
            $(".tl-direction-r").css("width", "");
            $(".tl-direction-l").css("width", "");
        }
    }

    cover_screen();
    timeline();
    $(window).resize(function () {
        cover_screen();
        timeline();
    });
});
