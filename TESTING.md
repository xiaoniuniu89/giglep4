# Code Validation
- HTML
    - No errors were returned when passing through the official[W3C validator](https://validator.w3.org/nu/?doc=https%3A%2F%2Fp4gigle.herokuapp.com%2F)
        - To check any individual page, right click -> view source -> copy and paste the html [here](https://validator.w3.org/#validate_by_input)
   
- CSS 
     - No errors were found when passing through the official [(Jigsaw) validator](https://jigsaw.w3.org/css-validator/)(https://jigsaw.w3.org/css-validator/)
        - [social.css](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fres.cloudinary.com%2Fdaniel-callaghan%2Fraw%2Fupload%2Fv1648465339%2Fstatic%2Fsocial%2Fcss%2Fsocial.a93544dc56c0.css)
        - [organiser.css](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fres.cloudinary.com%2Fdaniel-callaghan%2Fraw%2Fupload%2Fv1648045081%2Fstatic%2Forganiser%2Fcss%2Forganiser.29dc225f0882.css)
        - [gig_calendar.css](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fres.cloudinary.com%2Fdaniel-callaghan%2Fraw%2Fupload%2Fv1648045082%2Fstatic%2Fgig_calendar%2Fcss%2Fcalendar.2e52ae3e2f90.css)


- JavaScript
    - No errors were found when passing through [Jshint](https://jshint.com/)

<img src='https://res.cloudinary.com/daniel-callaghan/image/upload/v1648730753/Screenshot_from_2022-03-31_13-45-03_zcmnzb.png'/>

- Python
    - No errors were found when passing through [PEP8](http://pep8online.com/)
# Automated Testing

* NB*  - To run the automated tets you must use the commented out SQL lite database in settings.py as the Postgres database on Heroku lacks the necessary permission to create database tables.

The app uses Djangos inbuilt test module to test the site's code

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
    - The notification bell in the navbar will turn red if you have any unread notifications.
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

## Browser Testing

The app was tested on the following browsers:

- [Google Chrome](https://www.google.com/chrome/?brand=FHFK&gclid=CjwKCAjw092IBhAwEiwAxR1lRnrDJkW2rc2m-_DsqG2ISAAChH0tbKgopfm-3BMuide3ikPssZgvWhoCsVUQAvD_BwE&gclsrc=aw.ds)

- [Firefox](https://www.mozilla.org/en-US/firefox/) 

- [Opera](www.opera.com) 

- [Safari](https://www.apple.com/uk/safari/)

<img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648720621/Screenshot_from_2022-03-31_10-56-11_joskcb.png"/>

### Chrome
- No issues on this browser, the app works as expected.

### Firefox
- Chatbox looks much nicer on this browser. No major issues on this browser, the app works as expected.

### Opera
- There are no major issues on the Opera browser and the app works as expected.

### Safari
- The padding on some elements, eg: name and profile pic, like and dislike on posts is much less on this browser. Especially noticable on Iphone.



# Bugs

## Solved Bugs
### No friends and Empty Friends object
- A lot of logic depends on whether the user has a friend or not, eg: feed posts, friend lists, share an event, etc
- Following someone, then unfollowing someone left a situation that the user would have a friend object that was empty as compared to having no friends. This broke a lot of the site at first.
- It was fixed by using try and except blocks in the views and handling a user having no friends and an empty friend objects as the same.



## Unsolved Bugs
### User passes test robustness on event share
- It is difficult to write a test robust enough to prevent a user from, for example, changing the URL when sharing an event on the event share confirm page. As long as the user is friends with the person's id used in the URL parameters and the user also wrote the event, the app will allow the user to do this. It's not great for the user experience and I will try to fix it in the future.

### Threads of the unfriended
- A thread is created as soon as one user follows another. This is necessary to create a chat button between those two people.
-After unfriending a person it is difficult to get rid of the thread. Also, I did not like the idea of following, chatting, unfollowing, following again, and not having access to the past DM's.
- So for now, when you unfriend someone, you can still have a conversation with them and the thread will still appear in your inbox.

### Static files
- The static files are served from Cloudinary and sometimes, but not often, there is a problem with Cloudinary. I have had 2 occasions in the past where the files were not serving and the site was without any styling for 5-10 minutes at a time.

### password reset
- Password reset only seems to work for users who are using a gmail address.


