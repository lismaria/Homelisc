$(document).ready(function () {

  // For changing the nav bar design of homepage
  $(".wrapper").scroll(function () {
      var $nav = $(".lower-nav-ul, .lowernav-home-svg, .lowernav-ul-p");
      $nav.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
  });


  // For toggling between Food and Places in Wishlist
  $(".wishlist-header div").on('click', function(){
    $(".wishlist-sec").removeClass('wishlist-sec');
    $(this).addClass('wishlist-sec');
});

  // $(document).on('click', '.login-nav,.already-login', function (e) {
  //   e.preventDefault();
  //   $(".signup-nav .nav-line").css('background-color', 'var(--primary)');
  //   $(".login-nav .nav-line").css('background-color', 'var(--white)');
  // })

  // For bottom nav bar in almost every mobile device
  window.addEventListener('resize', () => {
    // First we get the viewport height and we multiple it by 1% to get a value for a vh unit
    let vh = window.innerHeight * 0.01;
    // Then we set the value in the --vh custom property to the root of the document
    document.documentElement.style.setProperty('--vh', `${vh}px`);
  });

  // //So that the content doesn't push up everytime the mobile keyboard is opened

  //Try 1
  // if ('ontouchstart' in window) {
  //   $(document).on('focus', 'textarea,input,select', function() {
  //     $('body, .lower-nav-ul').css('position', 'absolute');
  //   }).on('blur', 'textarea,input,select', function() {
  //     $('body, .lower-nav-ul').css('position', '');
  //   });
  // }

  //Try 2
//   setTimeout(function () {
//     var viewheight = $(window).height();
//     var viewwidth = $(window).width();
//     var viewport = $("meta[name=viewport]");
//     viewport.attr("content", "height=" + viewheight + "px, width=" + 
//     viewwidth + "px, initial-scale=1.0");
// }, 300);
});

var obj=angular.module("mod",[]);
obj.controller("cont",function($scope)
{
  $scope.acc = 'login'
  $scope.loginCol = "nav-line__red"
  $scope.signupCol = "nav-line__white"

  $scope.switcher=function ()
  {
    $scope.acc = $scope.acc == 'login' ? 'signup': 'login';
    $scope.loginCol= $scope.acc == 'login' ? 'nav-line__red' : 'nav-line__white';
    $scope.signupCol= $scope.acc == 'signup' ? 'nav-line__red' : 'nav-line__white';
  }

  // $scope.wishlist=function ()
  // {
  //   $scope.acc = $scope.acc == 'login' ? 'signup': 'login';
  //   $scope.loginCol= $scope.acc == 'login' ? 'nav-line__red' : 'nav-line__white';
  //   $scope.signupCol= $scope.acc == 'signup' ? 'nav-line__red' : 'nav-line__white';
  // }

});