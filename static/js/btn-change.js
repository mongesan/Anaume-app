$(document).on('click', ".footer-btn", function (e) {
    const button = $(this)
    const icon = button.children("i")
    const c = icon.hasClass("fa-eye-slash")
    console.log(button)
    if (c) {
        $(icon).removeClass("fa-eye-slash");
        $(icon).addClass("fa-eye");
        // button.style.color = "#FFFFFF";
        // button.style.background = "#FF530D";
    } else {
        $(icon).addClass("fa-eye-slash");
        $(icon).removeClass("fa-eye")
        $(this).style.color = "#FF530D";
        $(this).style.backgroundColor = "#FFFFFF";
    }
})