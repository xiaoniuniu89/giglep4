// to open profile dropdown menu
// organiser.css line 33 
$('.profile-dropdown-icon').on('click', function() {
    $('.profile-dropdown').toggleClass('profile-nav--open', 500);
    $('.close-dropdown').toggleClass('hide');
    $('.close-dropdown').toggleClass('move-forward');
    $('.nav-list li:nth-child(2)').toggleClass('hide');
    // if notifications are open, close them 
    if($('.notification-dropdown').hasClass('notification-nav--open')){
        $('.notification-dropdown').toggleClass('notification-nav--open', 300)
        $('.bell').toggleClass('hide');
    }

});

// to open and close the notification menu
$('.notifications-dropdown-icon').on('click', function() {
    $('.notification-dropdown').toggleClass('notification-nav--open', 500);
    $('.bell').toggleClass('hide');
});

// open and close modal to edit profile 

$('#edit-profile').on('click', function(){
    $('#profile-update-modal').css('display', 'block');
});

$('#close-modal').on('click', function(){
    $('#profile-update-modal').css('display', 'none');
});

// for removing notifications 
// Help from this tutorial
// https://www.youtube.com/watch?v=_JKWYkz597c&t=4s

// django documentation includes the following function to get csrf token 
// https://docs.djangoproject.com/en/3.1/ref/csrf/ 

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Help from this tutorial
// https://www.youtube.com/watch?v=_JKWYkz597c&t=4s

function removeNotification(removeNotificationURL, redirectURL) {
    // from onclick in remove notification in show_notifications.html
    // get csrf token 
    const csrftoken = getCookie('csrftoken');
    // make a new xml request 
    let xmlhttp = new XMLHttpRequest();
    // if request is ready 
    xmlhttp.onreadystatechange = function() {
        // if 200 response go ahead and redirect 
        if (xmlhttp.readyState == XMLHttpRequest.DONE) {
            if (xmlhttp.status == 200) {
                window.location.replace(redirectURL);
            } else return ('There was an error');
        }
    };
    xmlhttp.open("DELETE", removeNotificationURL, true);
    xmlhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xmlhttp.send();
}
