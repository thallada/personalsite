var request = undefined;

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

function update_charts(selected) {
    if (request !== undefined) {
        request.abort();
    }
    var svg = $('#current-svg');
    $('#current-svg').remove();
    $('div.current-chart').append('<img id="loading" style="margin-top: 5%" src="http://www.google.com/images/loading.gif" />');
    request = $.ajax({
        url: '/laundry/ajax/current/' + halls[selected]
    }).done(function (result) {
        svg = svg.attr('src', result);
        $('#loading').remove();
        $('.current-chart').append(svg);
    });
}
