# Automated Testing

* NB*  - To run the automated steps you must use the commented out SQL lite database in settings.py as the Postgres database on Heroku lacks the necessary permission to create database tables.

The app useses Djangos inuilt test module to test the sites code

To run tests, in command line type:
- python3 manage.py test

To run tests on individual apps include the app name at the end
- social app
    - python3 manage.py test social
- organiser app
    - python3 manage.py test organiser
- gig_calendar app
    - python3 manage.py test gig_calendar

The social app has a total of 25 tests
The organiser app has a total of 59 tests
The gig_calendar app has a total of 22 tests

To generate a coverage report of the app follow these steps in the command line:
- type: coverage run --source='.' manage.py test
- type: coverage report

A coverage report shows a total of 1461 statements tested with 87 untested, a 94% coverage rate.

<img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648208438/Screenshot_from_2022-03-25_11-39-41_oaq2is.png"/>


# Manual Testing

## Testing user stories

- As a user, I can create an account to access the site.
    - From the landing page, click the sign-up button on the page or in the navbar.
    - Fill in username, email, and confirm password.
    - you will be automatically redirected to the login page and can now use your username and password to log in.

- As a user, I can reset my password in case I lose it or feel my current password is not secure.
    - From the Login page, click forgot password under the login button.
    - Enter an email address.
    - Check mail and follow the link
    - reset password.
    - log in with the new password.

- As a user, I can update the information on my profile to reflect my current circumstances.
    - Click the icon for your profile page in the navbar.
    - On the profile card there is an edit button in the top right corner.
    - A modal form will pop up and you can change any details you wish.
    - On submission, your profile information will be updated across the app.
- As a user, I can post messages to let my followers know what I am thinking.
    - On the feed page click the post button at the top of the page.
    - Fill in the message you would like to post and click submit.
    - Your post is now live in the feed.
- As a user, I can comment and like other users' posts to show I agree or show I'm interested in what they say.
    - To like:
        - On the Feed page click the thumb up or thumb down button on the post in question.
        - Your like/dislike will be added to the post.
    - To Comment:
        - On the feed page, find the post you would like to comment on and click the speech bubble icon next to the dislike icon.
        - You will be redirected to the post detail page which has a comment box directly under the post.
        - Fill in your comment and submit.
        - Your comment has now been added to the post detail page.
- As a user, I can edit or delete my posts in case I change my mind about what I wanted to say.
    - To edit:
        - Find your post and click edit.
        - You will be redirected to a page where you can update your post, edit your post and submit it.
        - Your post has been updated in the feed.
    - To Delete:
        - Find your post and click delete.
        - When redirected and prompted to confirm click the confirm button.
        - Your post has now been deleted.
- As a user, I can follow other users so I can receive their posts in my feed.
    - Search for the user and navigate to their profile, or on the feed page directly click follow if they appear in your friend suggestions.
    - When you click follow, the user is immediately added to your friends and their posts will appear in your feed.
- As a user, I can DM other users to have a private conversation with them about work or other private matters.
    - From Profile:
        - On the users' profile, if you are friends, click the chat button available to you.
    - From Inbox:
        - Find the user with whom you would like to DM and click the thread to open the DM
    - In the message box input your message and submit it.
    - The message will be added to the chatbox.
- As a user, I can unfollow a user to stop receiving their posts in my feed.
    - On the users' profile page click the unfollow button.
    - You will no longer see their posts in your feed.
- As a user, I can receive notifications when I'm followed, messaged, invited to events or post receives a comment or like so I can know who has tried to interact with me during the day.
    - If you receive a like or comment on your post, someone follows you, you receive a DM, are invited to an invent - you will receive a notification.
    - The notification bell in the navbar will turn read if you have any unread notifications.
    - Click the bell and a notifications dropdown will appear under the navbar.
    - Click on the notification you want and you will be redirected to the page concerning that notification.
- As a user, I can add events to my calendar to avoid scheduling conflicts in my week-to-week work. 
    - On the calendar page, next to the right arrow button click the add event to calendar button.
    - Fill in the details for the event - title, date, and description and then submit.
    - The event has been added to your calendar.
- As a user, I can send or receive events to/from other users so I can send/receive relevant information for work or events.
    - On the event detail page, on the event card in the top right there is a share icon. Click it.
    - Select which friend you would like to send to or add a friend if you have no friends.
    - confirm you would like to send the event and submit it.
    - Your event has been shared with that user.
- As a user, I can search for other users so I can find musicians who I might want to work with.
    - In the search bar type the name, first or last, or the username of the user you would like to search for.
    - You will be redirected to a results page with any users matching your query.

