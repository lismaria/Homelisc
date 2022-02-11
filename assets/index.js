$(document).ready(function () {

  //Storing the initial height of the inner window
  let init_vh = window.innerHeight * 0.01;


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

  $( "input[type=text], input[type=email], input[type=password], textarea" ).focus(function() {
    $(".homepage-one, .signup-wrapper, .login-wrapper, .cuisine-wrapper, .profile-wrapper, .reviews-wrapper").css({'min-height':init_vh*90+'px'});
    // $("body").css({'min-height':init_vh*100+'px'});
    $(".lower-nav-ul").css({'display': 'none'});
    $(".wrapper").css({'height':'calc(var(--vh, 1vh) * 100)'});
    $(".review-popup").css({'bottom':'0vh'});
    // $("body").css("position", "fixed");
  });

  $( "input[type=text], input[type=email], input[type=password], textarea" ).blur(function() {
    $(".homepage-one, .signup-wrapper, .login-wrapper, .cuisine-wrapper, .profile-wrapper, .reviews-wrapper").css({'min-height':'auto'});
    // $("body").css({'min-height':'auto'});
    $(".lower-nav-ul").css({'display': 'grid'});
    $(".wrapper").css({'height':'calc(var(--vh, 1vh) * 90)'});
    $(".review-popup").css({'bottom':'9.8vh'});
    // $("body").css("position", "fixed");
  });


  //appends an "active" class to .popup and .popup-content when the "Open" button is clicked
  $(".product-review").on("click", function() {
    $(".review-popup, .review-popup-content, .login-required-wrapper").addClass("active");
    setTimeout(function() {
      $(".login-required-wrapper").removeClass("active");
    }, 5000);
  });

  //removes the "active" class to .popup and .popup-content when the "Close" button is clicked 
  $(".review-close").on("click", function() {
    $(".review-popup, .review-popup-content").removeClass("active");
  });

});

var obj=angular.module("mod",[]);
obj.controller("cont",function($scope)
{
  $scope.acc = 'login'
  $scope.loginCol = "nav-line__red"
  $scope.signupCol = "nav-line__white"
  $scope.edit = 'noedit'

  $scope.switcher=function ()
  {
    $scope.acc = $scope.acc == 'login' ? 'signup': 'login';
    $scope.loginCol= $scope.acc == 'login' ? 'nav-line__red' : 'nav-line__white';
    $scope.signupCol= $scope.acc == 'signup' ? 'nav-line__red' : 'nav-line__white';
  }

  $scope.editor=function (){
    $scope.edit = $scope.edit == 'noedit' ? 'yesedit' : 'noedit';
  }

  // $scope.wishlist=function ()
  // {
  //   $scope.acc = $scope.acc == 'login' ? 'signup': 'login';
  //   $scope.loginCol= $scope.acc == 'login' ? 'nav-line__red' : 'nav-line__white';
  //   $scope.signupCol= $scope.acc == 'signup' ? 'nav-line__red' : 'nav-line__white';
  // }

});