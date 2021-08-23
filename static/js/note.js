const el = document.getElementById('note-list');
const sortable = Sortable.create(el, {
    animation: 300,
    handle: ".handle",
    onEnd: function (evt) {
        let all_order = Array()
        let all_id = Array()
        $(".list-group-item").each(function (i, elem) {
            all_order.push($(elem).val())
            all_id.push($(elem).attr("id"))
        })
        $.ajax({
            url: '/change_order/' + $('.hiddenNoteID').attr('id'),
            method: 'POST',
            data: {
                "all_order": all_order,
                "all_id": all_id
            },
            timeout: 10000,
        }).done(response => {
            $(".list-group-item").each(function (i, elem) {
                $(elem).children('.num').text(String(i + 1) + '.')
            })
        })
    }
});

$("button.maker").on('click', function () {
    $("form#ajax-add-text").val($(this).val())
})

$("form#ajax-add-text").on('submit', e => {
    e.preventDefault()
    const form = $('form#ajax-add-text');
    $.ajax({
        url: form.attr("action"),
        method: form.attr("method"),
        data: form.serialize() + '&name=' + form.attr("name") + '&index=' + form.val(),
        timeout: 10000,
    })
        .done(response => {
            $("#id_sentence").val('')
            $("#id_translation").val('')
            $("form#ajax-checkbox-text").remove();
            const p = '<p>' + response['sentence'] + '<br>' + response['translation'] + '</p>'
            const aid = response['ajaxed_id']
            $('<form id="ajax-checkbox-text" text_id=' + aid + ' action="/note/0' + '" method="POST" name="add_check"></form>').appendTo('#add-text')
            // $('#texts').prepend('<form id="ajax-checkbox-text" text_id=' + aid + ' action="/note/0' +'" method="POST" name="add_check"></form>' + p)
            const words = response['words'];
            // console.log(words)
            let i = 0
            $("#STEP2").removeClass("opacity");
            $.each(words, function (index, elem) {
                box_id = String(aid) + '_' + String(i)
                $('<input class="d-none check_box" type="checkbox" id=' + box_id + ' name="check[]">' + '<label class="toggle" for=' + box_id + '>' + elem + '</label>' + '<span> </span>').appendTo('#ajax-checkbox-text');
                i += 1
            });
            $('<br><button type="submit" class="btn btn-success w-50"><i class="fas fa-check mx-1"></i>穴埋め</button>' + '{% csrf_token %}').appendTo('#ajax-checkbox-text');
            if (form.val() === "first"){
                $(".list-group").prepend("<li class=\"list-group-item\" id=\"" + String(aid) + "\"></li>")
            } else {
                $(".list-group").append("<li class=\"list-group-item\" id=\"" + String(aid) + "\"></li>")
            }
            $('<div class="text-right position-relative"><button class="btn btn-sm btn-danger position-absolute del_text_confirm" data-toggle="modal"\n' +
                '                        data-target="#deleteTextModal" data-pk="' + response['sentence'] + '"\n' +
                '                        data-url="/text/delete/' + response['ajaxed_id'] + '"><i class="fas fa-trash-alt"></i>\n' +
                '                            </button></div>' + '<span class="user-select-none num" style="font-size: 30px"></span><span>' + response['sentence'] + '</span><br><span>' + response['translation'] + '</span><br><p class="handle m-0" style="font-size: 20px"><i class="fas fa-sort" data-toggle="tooltip" title="ドラックで順番の変更"></i></p>').appendTo('#' + String(aid));
            const total_t = Number($("span#total_t").text()) + 1;
            const total_w = Number($("span#total_w").text()) + words.length;
            $("#total_t").text(String(total_t))
            $("#total_w").text(String(total_w))

            $(".list-group-item").each(function (i, elem) {
                $(elem).children('.num').text(String(i + 1) + '.')
            })
        });
});

$(document).on('submit', "form#ajax-checkbox-text", e => {
    e.preventDefault();
    const form = $('form#ajax-checkbox-text');
    let checks = [];
    $("[name='check[]']").each(function () {
        $(this).prop('disabled', true);
        checks.push($(this).prop("checked"));
    });
    $.ajax({
        url: form.attr("action"),
        method: form.attr("method"),
        data: {
            "checks": checks,
            "name": form.attr("name"),
            "text_id": form.attr("text_id"),
        },
        timeout: 10000,

    })
        .done(response => {
            const hides = response["hides"]
            const words = response["words"]
            const translation = response["translation"]
            const order = $("#" + String(response["text_id"])).children('.num').text()
            $("#" + String(response["text_id"])).empty();
            $('<div class="text-right position-relative">\n' +
                '                            <button class="btn btn-sm btn-danger position-absolute del_text_confirm" data-toggle="modal"\n' +
                '                        data-target="#deleteTextModal" data-pk="' + response['sentence'] + '"\n' +
                '                        data-url="/text/delete/' + response['text_id'] + '"><i class="fas fa-trash-alt"></i></button>' +
                '                        </div><span class="user-select-none num" style="font-size: 30px"></span>').appendTo('#' + String(response["text_id"]));
            for (let i = 0; i < hides.length; i++) {
                let word_id = "t" + String(response["text_id"]) + "w" + String(i)
                if (hides[i] === 'Y') {
                    $('<input class="d-none check_box" type="checkbox"\n' +
                        '                                       id="' + word_id + '"\n' +
                        '                                       name="scales" checked>' +
                        ' <label class="toggle"\n' +
                        '                                       for="' + word_id + '">' + words[i].replace('/', ',') + '</label>' + '<span> </span>').appendTo('#' + String(response["text_id"]));
                } else if (hides[i] === 'N') {
                    $('<span>' + words[i].replace('/', ',') + '</span>' + '<span> </span>').appendTo('#' + String(response["text_id"]));
                }
                // console.log(hides[i])
                // console.log(words[i])
            }
            $('<br><span>' + translation + '</span><br><p class="handle m-0" style="font-size: 20px"><i class="fas fa-sort" data-toggle="tooltip" title="ドラックで順番の変更"></i></p>\').appendTo(\'#\' + String(aid))').appendTo('#' + String(response["text_id"]));
            $("#" + String(response["text_id"])).children('.num').text(order)
            $("form#ajax-checkbox-text").remove();
            $("#STEP2").addClass("opacity");
            // $(window).scrollTop(500);
        });

});

$("form#name_form").on('submit', e => {
    e.preventDefault();
    const form = $('form#name_form');
    $.ajax({
        url: form.attr("action"),
        method: form.attr("method"),
        data: form.serialize() + '&name=' + form.attr("name"),
        timeout: 10000,

    })
        .done(response => {
            $('input#name_change').prop("checked", false);
            $('h4#title').text("英文帳:" + response["title"])
        });

});

$(document).on('click', '.copy-btn', function () {
    const t = $(this)
    t.text('copied!')
    setTimeout(function () {
        t.text("copy");
    }, 300);
})

$(function () {
    $('.del_note_confirm').on('click', function () {
        $("#del_note_pk").text($(this).data("pk"));
        $('#del_note_url').attr('href', $(this).data("url"));
    });
});

$(function () {
    $(document).on('click', '.del_text_confirm', function () {
        $("#del_text_pk").text($(this).data("pk"));
        $('#del_text_url').attr('href', $(this).data("url"));
    });
});

$(".btn-fav").on('click', e => {
    const icon = $(".btn-fav").children("i")
    const c = $(icon).hasClass("fas")
    e.preventDefault()
    $.ajax({
        url: $(".btn-fav").attr("formaction"),
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

