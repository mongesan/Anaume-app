$(document).on('click', ".btn-fav", function (e) {
    const icon = $(this).children("i")
    const c = icon.hasClass("fas")

    e.preventDefault()
    $.ajax({
        url: $(this).attr("formaction"),
        method: 'POST',
        data: 'status=' + String(c),
        timeout: 10000,

    })
        .done(response => {

        });
    if (c) { //ファボされた
        $(icon).removeClass("fas");
        $(icon).addClass("far");
    } else { //ファボはずされた
        $(icon).removeClass("far")
        $(icon).addClass("fas");
    }
})
