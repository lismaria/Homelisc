function defaultColors(that,init_letter)
  {
    switch(init_letter)
    {
      case 'a':
      case 'b':
      case 'c':
          that.find('img:first').css({'object-fit':'none','background-color':'#FFBFBF'});
          break;
      case 'd':
      case 'e':
      case 'f':
          that.find('img:first').css({'object-fit':'none','background-color':'#FFE2BF'});
          break;
      case 'g':
      case 'h':
      case 'i':
          that.find('img:first').css({'object-fit':'none','background-color':'#FEFFBF'});
          break
      case 'j':
      case 'k':
      case 'l':
          that.find('img:first').css({'object-fit':'none','background-color':'#BFFFC6'});
          break;
      case 'm':
      case 'n':
      case 'o':
          that.find('img:first').css({'object-fit':'none','background-color':'#BFFFF0'});
          break;
      case 'p':
      case 'q':
      case 'r':
          that.find('img:first').css({'object-fit':'none','background-color':'#BFD1FF'});
          break;
      case 's':
      case 't':
      case 'u':
          that.find('img:first').css({'object-fit':'none','background-color':'#D4BFFF'});
          break;
      case 'v':
      case 'w':
      case 'x':
          that.find('img:first').css({'object-fit':'none','background-color':'#FFBFF5'});
          break;
      case 'y':
      case 'z':
          that.find('img:first').css({'object-fit':'none','background-color':'#BFBFBF'});
          break;
      default:
          that.find('img:first').css({'object-fit':'none','background-color':'var(--accent)'});
          break;
    }
  }


$(document).ready(function () {

  //Storing the initial height of the inner window
  let init_vh = window.innerHeight * 0.01;


  // For changing the nav bar design of homepage
  $(".wrapper").scroll(function () {
      var $nav = $(".lower-nav-ul, .lowernav-home-svg, .lowernav-ul-p, .lowernav-ul-p__hide");
      $nav.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
  });


  $(function() {
    
    $(".fav-place-card").each(function() {
      let shop_src = $(this).find('img').attr('src')
      if(shop_src == '/media/default-shop.svg')
      {
          let shop_name = $(this).find('.favplace-cardbody-top').find('p').text()
          let shop_initial = shop_name.charAt(0).toLowerCase()
          let that = $(this)
          defaultColors(that,shop_initial)
      }
    })

    $(".product-card").each(function() {
      let item_src = $(this).find('img').attr('src')
      if(item_src == '/media/default-item.svg')
      {
          let item_name = $(this).find('h2').text()
          let item_initial = item_name.charAt(0).toLowerCase()
          let that = $(this)
          defaultColors(that,item_initial)
      }
    })

  })


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