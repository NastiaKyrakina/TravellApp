$(document).ready(function () {

    $(".note").on('click', 'button[id^=edit-element-]',
        function () {
            var post_primary_key = $(this).attr('id').split('-')[2];
            $('#note_element-' + post_primary_key + ' .note-text').load('/user/note/edit/' + post_primary_key)
            return false;

        });

    $('note-form').submit(
        function () {

            $('this').AjaxForm()

            console.log("post successful");

            return false;
        });


    function edit_post_send() {
        text = $('note-text-data').first().val();
        $.ajax({
            url: "/user/note/edit/" + post_primary_key, // the endpoint
            type: "POST", // http method
            data: {
                csrfmiddlewaretoken: Cookies.get('csrftoken'),
                text_note: text
            }, // data sent with the delete request
            success: function (json) {
                console.log("post successful");
            },

            error: function (xhr, errmsg, err) {
                // Show an error
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });

    }


    $(".note").on('click', 'button[id^=delete-element-]',
        function () {
            var post_primary_key = $(this).attr('id').split('-')[2];
            delete_post(post_primary_key);
        });

    function delete_post(post_primary_key) {
        if (confirm('are you sure you want to remove this post?') == true) {

            $.ajax({
                url: "/user/note/delete/", // the endpoint
                type: "POST", // http method
                data: {
                    csrfmiddlewaretoken: Cookies.get('csrftoken'),
                    notepk: post_primary_key
                }, // data sent with the delete request
                success: function (json) {
                    // hide the post
                    $('#note_element-' + post_primary_key).hide(); // hide the post on success
                    console.log(json.toString());
                    console.log("post deletion successful");
                },

                error: function (xhr, errmsg, err) {
                    // Show an error
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
            });
        } else {
            return false;
        }
    }


    $(".load_href_1").click(function () {

        var qr = $(".user-posts >:last-child .note_date small").text();

        $.ajax({
            type: 'GET',
            async: true,
            url: 'load_notes/',
            data: "since=" + qr,
            success: function (data) {
                $(".user-posts").append(data['html'])
            },
            dataType: 'json',
        });

    });


});

