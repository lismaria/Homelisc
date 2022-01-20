$(document).ready(function () {

    //Storing the initial height of the inner window
    let init_vh = window.innerHeight * 0.01;

    // For bottom nav bar in almost every mobile device
    window.addEventListener('resize', () => {
        // First we get the viewport height and we multiple it by 1% to get a value for a vh unit
        let vh = window.innerHeight * 0.01;
        // Then we set the value in the --vh custom property to the root of the document
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    });

    $("#vendor_profile").click(() => {
        $(".vendor-acc-profile").slideToggle("slow");
    })
    // register-shop NEXT>
    var image = new Image();
    $("#reg-n-1").click(function(){
        $("#reg-1").hide();
        $("#reg-2").show();
        $("#reg-3").hide();
        $(".step-two").css({"background-color":"var(--accent)"});
        $(".step-one h2").hide();
        image.url = './static/vendor/svg/tick.svg';
        $(".step-one img").append(image);
    });

    $("#reg-n-2").click(function(){
        $("#reg-1").hide();
        $("#reg-2").hide();
        $("#reg-3").show();
        $(".step-three").css({"background-color":"var(--accent)"});
    });
      
    // register-shop <BACK
    $("#reg-b-2").click(function(){
        $("#reg-1").show();
        $("#reg-2").hide();
        $("#reg-3").hide();
        $(".step-two").css({"background-color":"var(--neutral)"});
    });

    $("#reg-b-3").click(function(){
        $("#reg-1").hide();
        $("#reg-2").show();
        $("#reg-3").hide();
        $(".step-three").css({"background-color":"var(--neutral)"});
    });
});
