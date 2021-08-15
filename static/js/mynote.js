$(function () {
    $(document).on('click', '.del_note_confirm',function () {
        $("#del_note_pk").text($(this).data("pk"));
        $('#del_note_url').attr('href', $(this).data("url"));
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// 送信ボタンで呼ばれる
$("form#ajax-add-note").on('submit', e => {
    // デフォルトのイベントをキャンセルし、ページ遷移しないように!
    e.preventDefault();
    const form = $('form#ajax-add-note');
    $.ajax({
        url: form.attr("action"),
        method: form.attr("method"),
        data: form.serialize(),
        timeout: 10000,
    })
        .done(response => {
            // <p>はろー</p>のような要素を作成し、それを記事一覧エリアに追加し、入力欄をクリアする。
            let p = "<div class=\"note m-75 py-3 mb-4 mx-3 row new\"\n" +
                "                     onclick=\"location.href='/note/" +
                response['note_id'] + "'\">\n" +
                "                    <div class=\"col-1 d-flex align-items-center\" style=\"min-width: 50px; min-height: 50px\">\n" +
                "                        <p class=\"circle\"></p>\n" +
                "                    </div>\n" +
                "                    <div class=\"col-9 px-0 d-flex align-items-center\">\n" +
                "                        <p><br> タイトル:<a href=\"/note/" +
                response['note_id'] + "\">" +
                response['title'] +
                "                           </a><br>" +
                "                              作成者: " + response["user"] +
                "" +
                "                        </p></div>\n" +
                "                </div>"
            p +="<div class=\"text-right position-relative\">\n" +
                "\n" +
                "                    <button class=\"btn-fav position-absolute\" style=\"top:40px ;right: 5px\"\n" +
                "                            formaction=\"/note/fav/" + response['note_id'] + "\"\n" +
                "                            data-toggle=\"tooltip\"\n" +
                "                            title=\"お気に入り/解除\">\n" +
                "                            <i class=\"far fa-star\"></i>\n" +
                "                    </button>\n" +
                "                    <button class=\"btn btn-sm btn-danger position-absolute del_note_confirm\"\n" +
                "                            style=\"top: 130px; right: 7px\"\n" +
                "                            id=\"n" + response['note_id'] +"\"\n" +
                "                            data-toggle=\"modal\"\n" +
                "                            title=\"この英文帳を削除\"\n" +
                "                            data-target=\"#deleteNoteModal\" data-pk=\""+ response['title'] +"\"\n" +
                "                            data-url=\"/note/delete/"+ response['note_id'] + "\"><i\n" +
                "                            class=\"fas fa-trash-alt\"></i>\n" +
                "                    </button>\n" +
                "                </div>"
            // console.log(p)
            $("input#id_title").val("");
            $('#notes').after(p);
        });
});


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

