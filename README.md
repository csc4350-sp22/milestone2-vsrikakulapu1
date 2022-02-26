This README allows you to run my cloned repository on your local.

Heroku URL for my deployed app is : http://afternoon-taiga-38593.herokuapp.com/

To run the project locally, follow the steps below: 
Installation requirements (if you haven't installed them): 
(Also, Check the versions that are suitable for your system) 
python3 -m ensurepip --upgrade 
pip3 install python-dotenv 
pip3 install requests 
pip3 install Flask
pip3 install flask-login
brew install postgresql
brew services start postgresql
psql -h localhost  # this is just to test out that postgresql is installed okay - type "\q" to quit
pip3 install psycopg2-binary
pip3 install Flask-SQLAlchemy==2.1

Plugins to check for pylint errors:
pip3 install pylint-flask
pip3 install pylint-flask-sqlalchemy

Setup(what files to add):
Create .env file in your main directory to store your API Key and Database Url.
You can add your database url in .env file as - 
export DATABASE_URL = “your_url_goes_here”
Be sure to change “postgres” in url to “postgresql” for the SQLAlchemy to recognize. 
Create an account at https://www.themoviedb.org/?language=en-US and get your own TMDB key which should then be added to the .env file as: API_KEY="YOUR_KEY" Create a .gitignore file and add .env so that it remains hidden from being accessed by git.

Run Application: Run command in terminal: python3 app.py
To allow pylint to recognize SQLAlchemy: run the command to check for pylint errors:
$ pylint --load-plugins pylint_flask_sqlalchemy app.py
 Where app.py is the file name you want to run.

Preview web page in browser '/'
Brief overview of the app: The app takes you to a web page asking you to sign up to move further in the app. Once you enter your name and username you would like to use, the forms take these data and checks database if the username is unique. If unique, it takes you to the login page, else lets you know that username already exists, so you have to use a different one. Once you reach the login page, enter your details to move further inside the app. After logging in, you reach the final page in the app. This page is called Movie Hub which shows random movie details including : movie title, tagline, genres, movie poster along with the wikipedia link that provides more information about the movie. The background image gives a movie feel and to the right side of the screen is a random movie with the name, tagline and genres. Below the info is the movie poster and once you hover over the poster, you could see a link saying "Click here to Know more". This link click takes you to the wikipedia page relating to that movie name. Below the movie details, you can enter your rating and/or review to the displayed movies multiple times to multiple movies. You can also find the movie reviews given by other users below that. 
Detailed description of how implementing your project differed from your expectations during project planning.
Overall, I imagined that this milestone would be doable like the first one in the given amount of time. But, being the midpoint of semester, I had to take care of other midterms too. So, my time management and the planning help from class made it possible to finish this milestone. I got extensive help from Discord and I'm grateful for that. I started late so most of the errors I'm facing had solutions in discord chat already. This made my task easier.

Detailed description of 2+ technical issues and how you solved them (your process, what you searched, what resources you used)
I had errors saying my values in database for username was null which shouldn't be. So I fixed it by changing my code with online resources and the links given in Milestone 2 spec. 
I had this error H10 where it says APP CRASHED when trying to deploy on Heroku. I made the correction of adding an if condition to replace postgres with postgresql in DATABASE_URL. That fix from Discord saved my app from crashing.
All the help from Stackoverflow, Discord, online websites with documentation helped me in successfully building this app.

Detailed description of 2+ known problems and how you would address them if you had more time. If none exist, what additional features might you implement, and how?
I don't have any problems or errors as of now. But if some errors arise I would try to solve using the vast knowledge and experience of my peers from the online websites like Google, reddit, quora ...
I wanted to add additional functionality to my app so that it can display multiple movies at a time and allows us to hover over the movie posters to get the link that provides more information. I was able to add the hover functionality using CSS styling but couldn't expand my app to display multiple movies at a time on my screen. I tried to be creative by adding a background image which enhanced my UI and made it more user-friendly. However, more time would have allowed me to add extra features that would make the app more professional.
Detailed description of 2+ technical issues and how you solved it. (your process, what you searched, what resources you used)
I got application errors after deploying my app to Heroku.
Error 81 - at=info code=H81 desc="Blank app" method=GET path="/" host=agile-harbor-33804.herokuapp.com request_id=6f245cf9-e79b-4e28-9e9b-a9f24187dd48 fwd="99.104.37.93" dyno= connect= service= status=502 bytes= protocol=https I tried to google my error but I didn't find useful information that could solve my issue. So, I created a new app and tried to deploy again and it worked but then I got a different error next time (error H14).
Error H14 - at=error code=H14 desc=No web processes running" method=GET path="/" host=movie-hub-283.herokuapp.com request_id=a2fa4d4b-eb3e-4876-978b-9deca7bbb173 fwd="99.104.37.93" dyno= connect= service= status=503 bytes= protocol=https" I solved it using the stack overflow community response which used "heroku ps:scale web=1 " command to resolve it.
I faced Key Errors and Type Errors too while working with my app.py file. The errors looked like this "ValueError: Empty status argument", "TypeError: string indices must be integers". I used github solutions and other resources available on google to solve these errors. I handled the KeyError by having a return statement like this in my app.py file - return "Couldn't fetch movies!"

