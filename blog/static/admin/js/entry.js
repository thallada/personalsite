$.ajaxSetup({ 
    beforeSend: function(xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    } 
}); 
function openPreview(url, date) { 
    $('#preview-button').button('loading');
    $.ajax({
        type: 'POST',
        url: url,
        dataType:"json",
        data: {'comment': $('#id_comment').val()},
        success: function(data) {
            $('#preview-content').html(data['comment']);
            if ($('#id_url').val().length > 0) {
                $('#preview-header').html('<a href="'+$('#id_url').val()+'">'+$('#id_name').val()+'</a> - ' + date);
            } else {
                $('#preview-header').text($('#id_name').val()+' - {% now "N j, Y, h:i a" %}');
            }
            var wWidth = $(window).width();
            var dWidth = wWidth * 0.6;
            $('#preview').dialog({
                width: dWidth,
                buttons: {
                    Post: function() {
                        $('#post-button').click();
                    },
                    Cancel: function() {
                        $(this).dialog('close');
                    }
                }
            });
            $('#preview-button').button('reset');
        }
    });
}
function reply(event) {
    var id = $(event.target).parents('.comment').attr('id').replace('comment_', '');
    $.ajax({
        type:'GET',
        url:"{% url get_comment %}?id="+id,
        dataType:"json",
        success: function(data) {
            var lines = data.text.split('\n');
            var indented = 'Re: ['+data.user+'](#comment_'+id+')\n\n';
            $.each(lines, function(key, line) {
                indented = indented + '> ' + line + '\n\n';
            });
            $('#id_comment').prepend(indented);
        }
    });
}
function flag(event) {
    $('#report').dialog({
        buttons: {
            Yes: function() {
                $(this).dialog('close');
                var id = $(event.target).parents('.comment').attr('id').replace('comment_', '');
                $.ajax({
                    type:'GET',
                    url:"{% url flag_comment %}?id="+id,
                    dataType:"json",
                    success: function(data) {
                        if (data.success) {
                            $('#report-success').slideDown();
                        }
                    }
                });
            },
            Cancel: function() {
                $(this).dialog('close');
            }
        }
    });
}
