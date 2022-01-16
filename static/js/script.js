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
    $('.notification-dropdown').toggleClass('notification-nav--open', 500)
    $('.bell').toggleClass('hide')
    $('.cover-bell').toggleClass('hide')
})



// open and close modal 

$('#edit-profile').on('click', function(){
    $('#profile-update-modal').css('display', 'block')
})

$('#close-modal').on('click', function(){
    $('#profile-update-modal').css('display', 'none')
})
