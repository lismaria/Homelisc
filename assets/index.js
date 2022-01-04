$(document).ready(function () {


  let init_vh = window.innerHeight * 0.01;
  document.documentElement.style.setProperty('--init_vh', `${init_vh}px`);


  // For changing the nav bar design of homepage
  $(".wrapper").scroll(function () {
      var $nav = $(".lower-nav-ul, .lowernav-home-svg, .lowernav-ul-p, .lowernav-ul-p__hide");
      $nav.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
  });


  // For toggling between Food and Places in Wishlist
  $(".wishlist-header div").on('click', function(){
    $(".wishlist-sec").removeClass('wishlist-sec');
    $(this).addClass('wishlist-sec');
  });


  // For bottom nav bar in almost every mobile device
  window.addEventListener('resize', () => {
    // First we get the viewport height and we multiple it by 1% to get a value for a vh unit
    let vh = window.innerHeight * 0.01;
    // Then we set the value in the --vh custom property to the root of the document
    document.documentElement.style.setProperty('--vh', `${vh}px`);
  });

  $( "input[type=text]" ).focus(function() {
    $(".homepage-one, .signup-wrapper, .login-wrapper").css({'min-height':init_vh*90+'px'});
  });

  $( "input[type=text]" ).blur(function() {
    $(".homepage-one, .signup-wrapper, .login-wrapper").css({'min-height':'auto'});
  });


  // Scrolling to hash
  // $('.scroll-link').click(function() {
  //   var scrollTo = $(this).data('scroll-to');
  //   var nav = $('.wrapper');
  //   if (nav.length) {
  //     $(nav).animate({
  //       scrollTop: $('#'+scrollTo).offset().top}, 400);
  //   }
  // });

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