## Table of contents
- <a href="#about">About</a> 
- <a href="#ux">UX Design</a>
  - <a a href="#user-stories">User Stories</a>
  - <a href="#typography">Typography</a>
  - <a href="#color">Color</a>
  - <a href="#wireframes">Wireframes</a>
- <a href="#features">Features</a>
  - <a href="#nav">Nav/Footer</a>
  - <a href="#landing">Sign-Up/Login</a>
  - <a href="#feed">Social Feed</a>
  - <a href="#profile">User Profile</a>
  - <a href="#msg">Messages</a>
  - <a href="#calendar">Calendar</a>
  - <a href="#error">Error Pages</a>
  - <a href="#features-left">Features Left to Impliment</a>
- <a href="#tech">Technologies Used</a>
- <a href="#test">Testing</a>
- <a href="#deployment">Deployment</a>
- <a href="#credits">Credits</a>



<section id="about">

# About 

Gigle is a social media app for working musicians. Users can connect with other musicians, send private messages, book events on their own calendar, post what they are thinking in the social feed, and like/comment on other user posts. 


 <img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1643095598/Screenshot_from_2022-01-17_13-42-36_lz8lh0.png">
 
 
 The site is deployed here:
 
 - https://p4gigle.herokuapp.com/ 

</section>


<section id="ux">

# UX Design


## <p id="user-stories"> User Stories</p>

- As a user, I can create an account to access the site.
- As a user, I can reset my password in case I lose it or feel my current password is not secure.
- As a user, I can update the information on my profile to reflect my current circumstances.
As a user, I can post messages to let my followers know what I am thinking.
- As a user, I can comment and like other users' posts to show I agree or show I'm interested in what they say.
- As a user, I can edit or delete my posts in case I change my mind about what I wanted to say.
- As a user, I can follow other users so I can receive their posts in my feed.
- As a user, I can DM other users to have a private conversation with them about work or other private matters.
- As a user, I can unfollow a user to stop receiving their posts in my feed.
- As a user, I can receive notifications when I'm followed, messaged, invited to events or post receives a comment or like so I can know who has tried to interact with me during the day.
- As a user, I can add events to my calendar to avoid scheduling conflicts in my week-to-week work. 
- As a user, I can send or receive events to/from other users so I can send/receive relevant information for work or events.
- As a user, I can search for other users so I can find musicians who I might want to work with.


## The Real Books

Gigle is designed to look like a set of musical manuscripts that working musicians are very familiar with called Real Books and Fake Books. Real Books are manuscripts that contain hundreds of popular pop and jazz songs that musicians may need to reference on any show. They are published by [hal leonard](https://www.halleonard.com/feature/490/real-books). The term Fake Book is for older versions of these books, usually collections of songs that are incomplete and are just an outline of a piece.

 ## <p id="typography">Typography</p> 

- [Special Elite](https://fonts.google.com/specimen/Special+Elite) is used extensively in the site which is inspired by older style of Real Book, especially in the index and notes.

<img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648067774/special_elite_f5chka.jpg"/>

- [Luckiest Guy](https://fonts.google.com/specimen/Luckiest+Guy) is used in the site and best reflects real books headings, titles, and notation slashes.

<img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648067770/luckiest_guy_yg9lcp.jpg"/>


## <p id="color">Color</p>

The color scheme is influenced a lot by the bright neon colors of the various iterations of real books over time.

-  main-dark: #202020; 
- off-white: #faf9f6;
- off-grey: #615766;
- urgent: #D22730;
- yellow: #E0E722;
- orange: #FFAD00;
- red: #D22730;
- green: #44D62C;

<img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648068040/Screenshot_from_2022-03-23_20-26-34_1_ktaj8q.png"/>


## <p id="wireframes">Wireframes</p> 

Wireframes can be found <a href="p4-wireframes.pdf">here</a>

</section>

<section id="features">

# Features

This is an app I would have liked to use when I was working as a musician in my 20s. A lot of the functionality comes from problems I encountered often. The project is very big, however. In some areas, I don't have time to implement a feature, in others I don't have the skills yet. Here is a breakdown of how I decided on the minimal viable product for the first release.

<img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648111832/Screenshot_from_2022-03-24_08-49-35_vzrkna.png"/>

 ## <p id="nav">Nav / Footer</p> 
The navbar features a logo to the feed page, font awesome icons for all of the different pages a user can visit, a search bar, and a notification bell. Any flash messages will also be displayed under the navbar. The footer again provides links to any useful pages and links to social media sites.

- navbar

<img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648109810/Screenshot_from_2022-03-24_08-15-47_qhaaoe.png"/>

- notifications

<img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648110091/Screenshot_from_2022-03-24_08-20-54_age9z0.png"/>

- Flash messages

<img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648110229/Screenshot_from_2022-03-24_08-23-16_rrtyzw.png"/>

- Footer

<img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648110277/Screenshot_from_2022-03-24_08-15-55_f8fgfv.png"/>

 ## <p id="landing">Sign-up / Login</p> 

 The sign-up, login, and password reset all use built-in features of the Django web framework to handle authentication and form validation. 

 The styles of the forms are all custom styles.

- Sign up section


 <img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1643096835/Screenshot_from_2022-01-25_07-42-57_usmwqg.png">

 - login section

 <img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1643096835/Screenshot_from_2022-01-25_07-45-03_vosilr.png">

 - password reset system for forgotten passwords 

 <img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1643096835/Screenshot_from_2022-01-25_07-45-12_yzukof.png">


## <p id="feed">Social Feed </p> 

The social page is the page the user sees when they log into the site. From here users can create posts, get friend suggestions, and see posts of other users in their feed that they can like/dislike.

- feed page

 <img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648068983/Screenshot_from_2022-03-23_20-55-33_wons39.png"/>

 - create/edit post page 

 <img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648069465/Screenshot_from_2022-03-23_21-03-58_y4albw.png"/>
 - post detail/comment page

 <img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648069391/Screenshot_from_2022-03-23_21-02-35_v4iaev.png"/>



 ## <p id="profile">User Profile </p> 

- user profile page with update profile modal

 <img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648070761/Screenshot_from_2022-03-23_21-24-51_fhxulv.png"/>

 <img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648070791/Screenshot_from_2022-03-23_21-25-00_zjxger.png"/>

 - This is the profile of any user who is not the logged in user

 <img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648070944/Screenshot_from_2022-03-23_21-28-38_kjksja.png"/>

 - This is the users' friend list. The design of this page is very similar to the inbox displaying conversations between the user and friends and also the search results page.

- user list display 

 <img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648071093/Screenshot_from_2022-03-23_21-30-46_u2cwzf.png"/>

 ## <p id="msg">Messages </p>
 Users who are friends can have private conversations. The logged-in user is displayed on the right in green text.

 - DM page

 <img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648071262/Screenshot_from_2022-03-23_21-33-58_cyauze.png"/>


 ## <p id="calendar">Calendar </p>
 The calendar acts as a schedular. Users can add events, multiple events in a single day create a list view of the events. Users can share events with other users also.


- calendar

 <img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648071559/Screenshot_from_2022-03-23_21-38-49_h9ipne.png">

 - add/edit event

 <img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648071675/Screenshot_from_2022-03-23_21-40-38_gixpxm.png"/>

 - event detail
 <img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648071831/Screenshot_from_2022-03-23_21-43-18_zihi6q.png"/>

  - accept event invite

 <img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648071916/Screenshot_from_2022-03-23_21-44-45_iwl6ov.png"/>


 ## <p id="error">Error Pages </p>
There are 4 custom error pages. I think these are important as the inbuilt error pages are not tonally consistent with the design of the site.

- 404 (also very similar to 400 bad request)

 <img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648110517/Screenshot_from_2022-03-24_08-27-59_riziey.png">

 - 403 

<img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648110676/Screenshot_from_2022-03-24_08-30-51_l4qgxc.png">

 - 500

 <img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648110743/Screenshot_from_2022-03-23_16-32-08_1_fv8dbb.png">


## <p id="features-left">Features left to impliment</p>

- ability to send and display pdfs of music charts.
- setlist maker with PDFs, optimized for tablet view.
- band manager page where pdfs can be updated in real-time and added to the users' setlist.
- Kanban board for every event should the user need to organize their practice.
- group chats for bands.
- the ability to store press materials such as pdf of bio and photos that can be shared with agents.
- application to issue statements and bills
- geo locations and google maps to link events to venue


</section>

<section id="tech">

# Technologies Used 

[Gitpod](https://www.gitpod.io) 
- IDE (Intigrated Development Environment)

[Github](https://www.github.com)
- remote repository hosting platform

[HTML](https://developer.mozilla.org/en-US/docs/Web/HTML) | [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) | [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) |  [python](https://www.python.org/) 

- Languages Used to make the site

[Jquery](https://jquery.com/) | [JqueryUI](https://jqueryui.com/) | [django](https://www.djangoproject.com/) | [coverage](https://coverage.readthedocs.io/en/6.3.2/) 

- libraries and framework used to make the site

[Chrome Dev Tools](https://developer.chrome.com/docs/devtools/)
- Used to check site responsiveness

[HTML Validator](https://validator.w3.org/)
- Check for HTML errors

[Jigsaw](https://jigsaw.w3.org/css-validator/)
- Check for CSS errors

[PEP8](http://pep8online.com/)
- Check for python errors

[jshint](https://jshint.com/)
- check for JavaScript errors

[Font Awesome](https://fontawesome.com/)
- for Icons

[Balsamiq](https://balsamiq.com/)
- to make wireframes


# Testing <p id="test"></p>

Testing can be found in this file: [Testing](TESTING.md)

</section>

# Deployment <p id="deployment"></p>

The site is deployed on [Heroku](https://www.heroku.com/). The link is here:

https://p4gigle.herokuapp.com/

Steps to deploy the site on Heroku:

- in code editor add requirements for Heroku to install by typing the following commands into the terminal:
  - pip3 freeze > requirements.txt

- create a Procfile in the same directory as manage.py and paste in the following:
  - web: gunicorn gigle.wsgi

- in settings.py add Heroku to allowed hosts
  
- commit and push changes

- log in to Heroku or make an account
- click create a new app in the top right corner
- name your app and choose the region you live in
- in the resources tab of your app dashboard add the Postgres database resource
- in the settings tab click reveal config vars and add the following
  - CLOUDINARY_URL - get from [cloudinary](https://cloudinary.com/)
  - DATABASE_URL (added automatically)
  - EMAIL_PASS - the app uses google, steps to set up app passwords found [here](https://support.google.com/accounts/answer/185833?hl=en)
  - EMAIL_USER - Email account address
  - SECRET_KEY - can be anything

- go to the deploy tab and choose GitHub as deploy method
- search for the repo and connect
- click deploy branch
- if the build fails in the top right corner click the 'more' button and check logs to get an indication of the problem
- Click the view app button to see the app


How to fork the repository
- Go to [github.com](https://www.github.com) and log in.
- Click giglep4
- in the top right of the page click the "fork" button
- you will now have a copy of the repository in your GitHub account.

How to clone the repository
- Go to [github.com](https://www.github.com)
- Log in to account
- Click repositories
- Click giglep4
- Click the green code button that says Clone or download 
- to copy from HTTPS copy URL link "HTTPS". 
- open terminal
- go to the directory where you want to save the files
- type git clone and paste the link
- Press enter and the clone will be created


More detailed instructions can be found [here](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository#cloning-a-repository-to-github-desktop)


# Credits <p id="credits"></p>

## Media

#### Images
I found the black silhouettes of different musicians on [pixabay](https://pixabay.com/) and were mostly taken from a user called [Mohoamed Hassan](https://pixabay.com/users/mohamed_hassan-5229782/)

- landing page
    - [desktop](https://pixabay.com/vectors/jazz-silhouette-musician-trumpet-3662296/)
    - [mobile](https://pixabay.com/vectors/saxophone-saxophonist-silhouette-4455933/)

- 404 and 400
  - https://pngset.com/download-free-png-evwwm
- 403 page
  - https://pixabay.com/vectors/hand-print-grey-fingers-thumbs-307728/
- 500
  - https://pixabay.com/vectors/breaking-guitar-music-musician-2858673/

<br>

## Code and Tutorials

- [Corey Schafer blog series](https://www.youtube.com/watch?v=-s7e_Fy6NRU&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=10)

  - This series was great for how to use Django's built-in views and authentication especially CRUD functionality.


- [Legion Script](https://www.youtube.com/watch?v=_JKWYkz597c)
  - This series helped a lot to get the DM and notifications functionality working. 


- [Hui Wen](https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html)
  - This tutorial was very useful and I don't think the calendar app would not have worked without it. It describes how to make a calendar in a utils.py file and render it to the template.
  