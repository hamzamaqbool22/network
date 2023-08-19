console.log('working checking');

$(document).ready(function() {
    // Function to get CSRF token from cookies
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            var cookies = document.cookie.split(";");
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Set up CSRF token for AJAX requests
    const csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Function to update like buttons based on local storage
    function updateLikes() {
        $(".like-button").each(function() {
            var button = $(this);
            var postId = button.data("post-id");
            var likeCountElement = $(".like-count[data-post-id='" + postId + "']");

            var isLiked = localStorage.getItem("liked_" + postId);
            if (isLiked === "true") {
                button.find("i").removeClass("far").addClass("fas text-danger");
            } else {
                button.find("i").removeClass("fas text-danger").addClass("far");
            }
        });
    }

    // Call the function to update like buttons when the page loads
    updateLikes();

    // Handle like button clicks
    $(".like-button").click(function() {
        var button = $(this);
        var postId = button.data("post-id");
        var likeCountElement = $(".like-count[data-post-id='" + postId + "']");

        $.ajax({
            type: "POST",
            url: "/like_toggle/",
            data: {
                post_id: postId,
                csrfmiddlewaretoken: csrftoken,
            },
            success: function(response) {
                if (response.action === "liked") {
                    localStorage.setItem("liked_" + postId, "true");
                } else {
                    localStorage.removeItem("liked_" + postId);
                }
                updateLikes();
                likeCountElement.text(response.like_count);
            },
            error: function(xhr, status, error) {
                console.error("Error:", error);
            }
        });
    });
});
