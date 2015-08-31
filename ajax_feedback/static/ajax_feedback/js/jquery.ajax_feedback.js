(function($) {
    $.fn.ajaxFeedback = function(settings) {
        var form = $(this);
        settings = $.extend({
            messagesBlock: null,
            beforeSend: null,
            successCallback: null,
            validationErrorCallback: null,
            errorCallback: null,
            completeCallback: null
        }, settings);

        function defaultValidationErrorCallback(response) {
            $.each(response.data, function(index, value){
                if (index == '__all__')
                    messagesBlock.append('<div class="alert alert-danger fade in">'
                        +'<a class="close" data-dismiss="alert" href="#" aria-hidden="true">&times;</a>'
                        +value+'</div>');
                else {
                    var field =  form.find('#id_' + index);
                    field.parents('.form-group').addClass('has-error');
                    field.after('<span class="help-block help-block-error">'+value+'</span>');
                }
            })
        }

        var messagesBlock = settings.messagesBlock || form,
            validationErrorCallback = settings.validationErrorCallback || defaultValidationErrorCallback;

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
                        settings.beforeSend(form, messagesBlock);
                    form.find('.has-error').find('.help-block-error').remove().end().removeClass('has-error')
                },
                success: function(response) {
                    if (response.status == true) {
                        if ($.isFunction(settings.successCallback))
                            settings.successCallback(response);
                    }
                    else
                        validationErrorCallback(response);
                },
                complete: function () {
                    if ($.isFunction(settings.completeCallback))
                        settings.completeCallback(form, messagesBlock);
                }
            });
        });
    };
})(jQuery);
