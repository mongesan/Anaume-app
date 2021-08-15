$('[data-toggle="tooltip"]').tooltip();
$('[data-toggle="modal"]').tooltip();
$(function(){
        $("input"). keydown(function(e) {
            if ((e.which && e.which === 13) || (e.keyCode && e.keyCode === 13)) {
                return false;
            } else {
                return true;
            }
        });
    });

new ClipboardJS('.copy-btn');