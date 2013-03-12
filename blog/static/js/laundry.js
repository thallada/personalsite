$(document).ready(function () {
    if ($.cookie('hall') !== undefined) {
        $('#hall-select').val($.cookie('hall'));
    }
    $('#hall-select').change(function () {
        $.cookie('hall', $('#hall-select option:selected').text(), {expires: 1825});
    });
});
