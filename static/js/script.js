// to open profile dropdown menu
// organiser.css line 33 
$('.profile-dropdown-icon').on('click', function() {
    $('.profile-dropdown').toggleClass('profile-nav--open', 500),
    $('.close-dropdown').toggleClass('hide')
    $('.close-dropdown').toggleClass('move-forward')
    $('.nav-list li:nth-child(2)').toggleClass('hide')

})


// to open and close the notification menu
$('.notifications-dropdown-icon').on('click', function() {
    console.log('clicked')
    $('.notification-dropdown').toggleClass('notification-nav--open', 500)
    $('.bell').toggleClass('hide')
    $('.cover-bell').toggleClass('hide')
})



// open and close modal to edit profile 

$('#edit-profile').on('click', function(){
    $('#profile-update-modal').css('display', 'block')
})

$('#close-modal').on('click', function(){
    $('#profile-update-modal').css('display', 'none')
})

// for notifications 

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


function removeNotification(removeNotificationURL, redirectURL) {
    const csrftoken = getCookie('csrftoken');
    let xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == XMLHttpRequest.DONE) {
            if (xmlhttp.status == 200) {
                window.location.replace(redirectURL)
            } else('There was an error');
        }
    } 
    xmlhttp.open("DELETE", removeNotificationURL, true);
    xmlhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xmlhttp.send();
}







