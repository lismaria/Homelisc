$(function () {
    $(document).scroll(function () {
        var $nav = $(".lower-nav-ul");
        var $nav1 = $(".lowernav-home-svg")
        var $nav2 = $(".lowernav-ul-p")
        $nav.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
        $nav1.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
        $nav2.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
      });
});