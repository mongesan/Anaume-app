$(document).on('click', ".footer-btn", function (e) {
    const button = $(this)
    const icon = button.children("i")
    const c = icon.hasClass("fa-eye-slash")
    const check_box = document.getElementsByClassName('check_box')

    if (c) {
        $(icon).removeClass("fa-eye-slash");
        $(icon).addClass("fa-eye");
        button[0].style.color = "#FF530D";
        button[0].style.backgroundColor = "#FFFFFF";
        for(let i = 0; i < check_box.length; i++){
            check_box[i].checked = true;
        }
        // cb[1].checked = false;
        // for (let cb in document.getElementsByClassName('check_box')){
        //     console.log(cb)
        // }
    } else {
        $(icon).addClass("fa-eye-slash");
        $(icon).removeClass("fa-eye");
        button[0].style.color = "#FFFFFF";
        button[0].style.background = "#FF530D";
        for(let i = 0; i < check_box.length; i++){
            check_box[i].checked = false;
        }
    }
})