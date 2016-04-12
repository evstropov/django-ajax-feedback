(function($) {
    $.fn.ajaxFeedback = function(settings) {
        var form = $(this);
        settings = $.extend({
            messagesBlock: form,
            beforeSend: null,
            successCallback: defaultSuccessCallback,
            validationErrorCallback: defaultValidationErrorCallback,
            errorCallback: null,
            completeCallback: defaultCompleteCallback
        }, settings);

        form.on("submit", function(e) {
            e.preventDefault();
            if ($(this).hasClass('disabled')) return;
            $.ajax({
                data: form.serialize(),
                dataType: 'json',
                type: 'POST',
                url: form.attr('action'),
                error: settings.errorCallback,
                beforeSend: function() {
                    if ($.isFunction(settings.beforeSend))
                        settings.beforeSend(form, settings.messagesBlock);
                    form.find('.ajax-feedback-msg').remove();
                    form.find('.has-error').find('.help-block-error').remove().end().removeClass('has-error')
                },
                success: function(response) {
                    if (response.status == true) {
                        if ($.isFunction(settings.successCallback))
                            settings.successCallback(response, form, settings.messagesBlock);
                    }
                    else
                        settings.validationErrorCallback(response, form, settings.messagesBlock);
                },
                complete: function () {
                    if ($.isFunction(settings.completeCallback))
                        settings.completeCallback(form, form, settings.messagesBlock);
                }
            });
        });
    };

    function addMsg(sel, text, type) {
        sel.prepend('<div class="alert alert-'+type+' fade in ajax-feedback-msg">'
                    +'<a class="close" data-dismiss="alert" href="#" aria-hidden="true">&times;</a>'
                    +text+'</div>');
    }

    function defaultSuccessCallback(response, form, msgBlock) {
        console.log(response.data);
        addMsg(msgBlock, response.data, 'success');
    }

    function defaultCompleteCallback(response, form) {
        form.find('input[type=text], textarea').val('');
    }

    function defaultValidationErrorCallback(response, form, msgBlock) {
        $.each(response.data, function(index, value){
            if (index == '__all__')
                addMsg(msgBlock, value, 'danger');
            else {
                var field =  form.find('#id_' + index);
                field.parents('.form-group').addClass('has-error');
                field.after('<span class="help-block help-block-error">'+value+'</span>');
            }
        })
    }
})(jQuery);
