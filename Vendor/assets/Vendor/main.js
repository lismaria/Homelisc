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
    $("#reg-n-1").click(function(){
        $("#reg-1").hide();
        $("#reg-2").show();
        $("#reg-3").hide();
    });

    $("#reg-n-2").click(function(){
        $("#reg-1").hide();
        $("#reg-2").hide();
        $("#reg-3").show();
    });
      
    // register-shop <BACK
    $("#reg-b-2").click(function(){
        $("#reg-1").show();
        $("#reg-2").hide();
        $("#reg-3").hide();
    });

    $("#reg-b-3").click(function(){
        $("#reg-1").hide();
        $("#reg-2").show();
        $("#reg-3").hide();
    });

    $('input[type="file"]').change(function() {
        // alert("A file has been selected.");
        $('.add-logolabel>p, .add-logolabel>svg').css({'z-index':-1})
    });
});
