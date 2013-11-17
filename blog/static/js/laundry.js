var request = undefined;
var pending = false;

$(document).ready(function () {
    if ($.cookie('hall') !== undefined) {
        $('#hall-select').val($.cookie('hall'));
    }
    update_charts($('#hall-select option:selected').text());
    $('#hall-select').change(function () {
        $.cookie('hall', $('#hall-select option:selected').text(), {expires: 1825});
        update_charts($('#hall-select option:selected').text());
    });
});

$(document).ajaxStart(function () { pending = true; });

$(document).ajaxStop(function () { pending = false; });

function update_charts(selected) {
    if (!pending) {
        if (request !== undefined) {
            request.abort();
        }
        $('.current-chart').empty();
        var svg = $('<embed id="current-svg" type="image/svg+xml">');
        $('.current-chart').append('<img id="loading" style="margin-top: 5%" src="http://www.google.com/images/loading.gif" />');
        request = $.ajax({
            url: '/laundry/ajax/current/' + halls[selected]
        }).done(function (result) {
            svg.attr('src', result);
            $('#loading').remove();
            console.log(svg);
            $('.current-chart').append(svg);
        }).error(function (jqXHR, textStatus, errorThrown) {
            $('#loading').remove();
            $('.current-chart').append(
                '<p class="error">Oops. My webscraping script broke. Either ' +
                'eSuds changed their website or Mason switched the laundry ' +
                'rooms up. I\'ve been emailed and will try to fix it soon. ' +
                ':)</p>');
        });
    }
}
