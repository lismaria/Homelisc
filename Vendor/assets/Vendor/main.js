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

    // For bottom nav bar in almost every mobile device
    window.addEventListener('resize', () => {
        // First we get the viewport height and we multiple it by 1% to get a value for a vh unit
        let vh = window.innerHeight * 0.01;
        // Then we set the value in the --vh custom property to the root of the document
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    });

    $("#vendor_profile").click(() => {
        $(".vendor-acc-profile").slideToggle("slow");
    });

    $( "input[type=text], input[type=email], input[type=password], input[type=tel], textarea" ).focus(function() {
        $(".register-shop-wrapper").css({'min-height':init_vh*100+'px'});
        $(".shop-wrapper, .add-item-wrapper").css({'min-height':init_vh*81+'px'});
        $(".vendor-nav-ul").css({'display': 'none'});
    });
    
    $( "input[type=text], input[type=email], input[type=password], input[type=tel], textarea" ).blur(function() {
        $(".register-shop-wrapper, .shop-wrapper, .add-item-wrapper").css({'min-height':'auto'});
        $(".vendor-nav-ul").css({'display': 'grid'});
    });


    $(function(){

        that = $(".shop-info__main")
        shop_src = that.find('img:first').attr('src')
        if(shop_src == '/media/default-shop.svg')
        {
            shop_name = that.find('h2').text()
            shop_initial = shop_name.charAt(0).toLowerCase()
            defaultColors(that,shop_initial)
        }

        user_upper_that = $(".vendor-uppernav-div")
        user_that = $(".vendor-acc-imgdiv")
        user_src = user_that.find('img:first').attr('src')
        if(user_src == '/media/default-user.svg')
        {
            user_name = user_that.siblings('div').find('input[name=name]').val()
            user_initial = user_name.charAt(0).toLowerCase()
            defaultColors(user_that,user_initial)
            defaultColors(user_upper_that,user_initial)
        }
    })
});
