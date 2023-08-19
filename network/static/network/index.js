$(document).ready(function() {
  // Attach a click event handler to the edit buttons
  $('.edit-btn').click(function() {
      var postId = $(this).data('post-id');
      
      // Hide the post text and show the edit textarea and save button
      $('.card-title[data-post-id="' + postId + '"]').hide();
      $('.edit-textarea[data-post-id="' + postId + '"]').show();
      $('.save-btn[data-post-id="' + postId + '"]').show();
      $(this).hide();
  });

  // Attach a click event handler to the save buttons
  $('.save-btn').click(function() {
      var postId = $(this).data('post-id');
      var new_text = $('.edit-textarea[data-post-id="' + postId + '"]').val();
      var cardTitle = $('.card-title[data-post-id="' + postId + '"]');
      if (!postId) {
        alert('Please log in to edit posts.');  // Optional message
        return;
      }
      $.ajax({
          type: 'POST',
          url: '/update_post/' + postId + '/',
          data: {
              new_text: new_text,
              csrfmiddlewaretoken: csrfToken,
          },
          beforeSend: function(xhr, settings) {
              xhr.setRequestHeader("X-CSRFToken", csrfToken);
          },
          success: function(data) {
              if (data.success) {
                  cardTitle.text(new_text);
                   console.log(new_text);
                  document.querySelector('.full-content').innerHTML = new_text;
                  cardTitle.show();
                  $('.edit-textarea[data-post-id="' + postId + '"]').hide();
                  $('.save-btn[data-post-id="' + postId + '"]').hide();
                  $('.edit-btn[data-post-id="' + postId + '"]').show();
              } else {
                  alert('Failed to update the post.');
              }
          },
          error: function() {
              alert('An error occurred while sending the request.');
          }
      });
  });
});


$(document).ready(function() {
    $('.read-more-btn').click(function() {
        $(this).hide();
        $('.truncated-content').hide();
        $('.full-content').show();
        $('.read-less-btn').show();
    });

    $('.read-less-btn').click(function() {
        $(this).hide();
        $('.full-content').hide();
        $('.truncated-content').show();
        $('.read-more-btn').show();
    });
});
