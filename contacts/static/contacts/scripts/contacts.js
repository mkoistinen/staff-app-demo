(function($){
  "use strict";

  $(function(){

    $('.contacts-plugin input[type=submit]').on('click', function(evt){
      var $form = $(this).parents('form').eq(0);

      function handleResponse(data){
        if (data.pk) { // Success!
          $form.siblings('.success').html(data.success).show(100);

          //
          // NOTE: We hide the form if there was ANY success to prevent
          // duplicate submissions. There can be no success if there are
          // form-validation errors, in which case, the form remains
          // visible so the visitor can correct their mistakes.  In the
          // event that there are no validation errors and yet, nothing is
          // successful, the form remains visible so the user can try again.
          //
          $form.add('.legend').hide(100);
        }

        else { // Validation Issues...
          //
          // data will a dictionary like so:
          // { 'field_name': ['error1', 'error2'], ... }
          //
          $form.find('.error').empty();
          $.each(data, function(key, value){
            var $field = $form.find('input[name='+key+']').first();
            $field.parents('.field-wrapper').find('.error').html(value.join(' '));
          });

          //
          // General errors will be appended to the template-driven standard
          // message.
          //
          if (data.__all__) {
            $form.siblings('.errors').find('.form-errors').html(data.__all__.join(' '));
          }
          else {
            $form.siblings('.errors').find('.form-errors').empty();
          }
          $form.siblings('.errors').show(100);
        }
      }

      evt.preventDefault();
      $form.siblings('.errors, .success').hide(100);

      $.ajax({
        type: 'POST',
        url: $form.attr('action'),
        data: $form.serialize()
      }).always(handleResponse);
    });

  });
}(window.jQuery));
