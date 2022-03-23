## Table of contents
- <a href="#about">About</a> 
- <a href="#ux">UX Design</a>
  - <a a href="#user-stories">User Stories</a>
  - <a href="#typography">Typography</a>
  - <a href="#color">Color</a>
  - <a href="#wireframes">Wireframes</a>
- <a href="#features">Features</a>
  - <a href="#landing">Sign-Up/Login</a>
  - <a href="#feed">Social Feed</a>
  - <a href="#calendar">Calendar</a>
  - <a href="#msg">Messages</a>
  - <a href="#profile">User Profile</a>
  - <a href="#features-left">Features Left to Impliment</a>
- <a href="#tech">Technologies Used</a>
- <a href="#test">Testing</a>
- <a href="#deployment">Deployment</a>
- <a href="#credits">Credits</a>



<section id="about">

# About 

 Gigle is a social media app for working musicians. Users can connect with other musicians, send provate messages, book events on their own calendar, post what they are thinking in the social feed and like/comment other user posts. 


 <img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1643095598/Screenshot_from_2022-01-17_13-42-36_lz8lh0.png">
 
 
 The site is deployed here:
 
 - https://p4gigle.herokuapp.com/ 

</section>


<section id="ux">

# UX Design


## <p id="user-stories"> User Stories</p>

- As a user I can create an account to access the site.
- As a user I can reset my password incase I loose it or feel my current password is not secure.
- As a user I can update the information on my profile to reflect my current circumstances.
As a user I can post messages to let my followers know what I am thinking.
- As a user I can comment and like other users posts to show I agree or show I'm interested in what the say.
- As a user I can edit or delete my posts in case I change my mind about what I wanted to say.
- As a user I can follow other users so I can receive their posts in my feed.
- As a user I can DM other users to have a private conversation with them about work or other private matters.
- As a user I can unfollow a user to stop receiving their posts in my feed.
- As a user I can receive notifications when I'm followed, messaged, invited to events or post receives a comment or like so I can know who has tried to interact with me during the day.
- As a user I can add events to my calendar to avoid scheduling conflicts in my week to week work. 
- As a user I can send or recieve events to/from other users so I can send/receive relevant information for work or events.
- As a user I can search for other users so I can find musicians who I might want to work with.


## The Real Books

Gigle is designed to look like a set of musical manuscripts that working musicians are very familiar with called Real Books and Fake Books. Real Books are manuscripts that contain hundreds of popular pop and jazz songs that musicians may need to reference on any show. They are published by [hal leonard](https://www.halleonard.com/feature/490/real-books). The term Fake Book are older versions of these books, usually collections of songs that are incomplete and are just an outline of a piece.

 ## <p id="typography">Typography</p> 

- [Special Elite](https://fonts.google.com/specimen/Special+Elite) is used extensively in the site which is inspired by older style of Real Book, especially in the index and notes.

<img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1648067774/special_elite_f5chka.jpg"/>

- [Luckiest Guy](https://fonts.google.com/specimen/Luckiest+Guy) is used in the site and best reflects real books headings, titles and notation slashes.

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

Wireframes can be found [here]()

</section>

<section id="features">

# Features

 ## <p id="landing">Sign-up / Login</p> 

 The sign-up, login and password reset all use built-in features of the django webframework to handle authentication and form validation. 

 The styles of the forms are all custom styles.

- Sign up section


 <img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1643096835/Screenshot_from_2022-01-25_07-42-57_usmwqg.png">

 - login section

 <img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1643096835/Screenshot_from_2022-01-25_07-45-03_vosilr.png">

 - password reset system for forgotten passwords 

 <img src="https://res.cloudinary.com/daniel-callaghan/image/upload/v1643096835/Screenshot_from_2022-01-25_07-45-12_yzukof.png">


## <p id="feed">Social Feed </p> 



 <img src="">


 ## <p id="calendar">Calendar </p> 



 <img src="">

 ## <p id="msg">Messages </p> 


 <img src="">


## <p id="profile">User Profile </p> 



 <img src="">



## <p id="features-left">Features left to impliment</p> 



</section>

<section id="tech">

# Technologies Used 

[Gitpod](https://www.gitpod.io) 
- IDE (Intigrated Development Environment)

[Github](https://www.github.com)
- remote repository hosting platform

[HTML](https://developer.mozilla.org/en-US/docs/Web/HTML) | [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) | [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) | [Jquery](https://jquery.com/) | [python](https://www.python.org/) | [django](https://www.djangoproject.com/)

- Languages, libraries and framework
 Used to make the site

[Chrome Dev Tools](https://developer.chrome.com/docs/devtools/)
- Used to check site responsiveness

[Jigsaw](https://jigsaw.w3.org/css-validator/)
- Check for CSS errors

[HTML Validator](https://validator.w3.org/)
- Check for HTML errors

[jshint](https://jshint.com/)
- check for JavaScript errors

[Font Awesome](https://fontawesome.com/)
- for Icons 

[Balsamiq](https://balsamiq.com/)
- to make wireframes

[Website Responsive Test](http://responsivetesttool.com/)
- to check responsivness on different devices

# Testing <p id="test"></p>

Testing can be found in this file: [Testing](TESTING.md)

</section>

# Deployment <p id="deployment"></p>

The site is deployed on git hub pages. The link is here:

https://xiaoniuniu89.github.io/santa-letters/

Steps to deploy the site:


How to fork the repository
- Go to [github.com](https://www.github.com) and login.
- Click santa-letters
- in the top right of the page click the "fork" button
- you will now have a copy of the repository in your github account.

How to clone the repository
- Go to [github.com](https://www.github.com)
- Log in to account
- Click repositories
- Click santa-letters fork
- Click the green code button that says Clone or download 
- to copy from HTTPS copy URL link "HTTPS". 
- open terminal
- go to directory where you want to save the files
- type git clone and paste the link
- press enter and the clone will be created


More detailed instructions can be found [here](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository#cloning-a-repository-to-github-desktop)


# Credits <p id="credits"></p>

## Content

### Media
<br>

#### Images



<br>



#### Videos


<br>

### Text

- text written by