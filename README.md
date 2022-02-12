 This README allows you to run my cloned repository on your local.

 Heroku URL for my deployed app "movie-hub-283" is :
 https://movie-hub-283.herokuapp.com/

To run the project locally, follow the steps below:
Installation requirements (if you haven't installed them):
(Also, Check the versions that are suitable for your system)
	python3 -m ensurepip --upgrade
	pip install python-dotenv
	pip install requests
	pip install Flask

Setup(what files to add)
	Create .env file in your main directory to store your API Key
	Create an account at https://www.themoviedb.org/?language=en-US and get your own TMDB key which 
	should then be added to the .env file as: API_KEY="YOUR_KEY"
	Create a .gitignore file and add .env so that it remains hidden from being accessed by git.

Run Application:
	Run command in terminal: python3 app.py
	Preview web page in browser '/'

Brief overview of the app:
My app is called Movie Hub which shows random movie details including : movie title, tagline, genres, movie poster along with the wikipedia link that provides more information about the movie. The background image gives a movie feel and to the right side of the screen is a random movie with the name, tagline and genres. Below the info is the movie poster and once you hover over the poster, you could see a link saying "Click here to Know more". This link click takes you to the wikipedia page relating to that movie name.


Detailed description of 2+ known problems and how you would address them if you had more time. If none exist, what additional features might you implement, and how?

I don't have any problems or errors as of now. But if some errors arise I would try to solve using the vast knowledge and experience of my peers from the online websites like Google, reddit, quora ...
 
I wanted to add additional functionality to my app so that it can display multiple movies at a time and allows us to hover over the movie posters to get the link that provides more information. I was able to add the hover functionality using CSS styling but couldn't expand my app to display multiple movies at a time on my screen. I tried to be creative by adding a background image which enhanced my UI and made it more user-friendly. However, more time would have allowed me to add extra features that would make the app more professional.

Detailed description of 2+ technical issues and how you solved it. (your process, what you searched, what resources you used)

I got application errors after deploying my app to Heroku.

Error 81 - at=info code=H81 desc="Blank app" method=GET path="/" host=agile-harbor-33804.herokuapp.com request_id=6f245cf9-e79b-4e28-9e9b-a9f24187dd48 fwd="99.104.37.93" dyno= connect= service= status=502 bytes= protocol=https
I tried to google my error but I didn't find useful information that could solve my issue. So, I created a new app and tried to deploy again and it worked but then I got a different error next time (error H14). 

Error H14 - at=error code=H14 desc=No web processes running" method=GET path="/" host=movie-hub-283.herokuapp.com request_id=a2fa4d4b-eb3e-4876-978b-9deca7bbb173 fwd="99.104.37.93" dyno= connect= service= status=503 bytes= protocol=https"
I solved it using the stack overflow community response which used "heroku ps:scale web=1 " command to resolve it.

I faced Key Errors and Type Errors too while working with my app.py file. The errors looked like this "ValueError: Empty status argument", "TypeError: string indices must be integers". I used github solutions and other resources available on google to solve these errors. I handled the KeyError by having a return statement like this in my app.py file - return "Couldn't fetch movies!"


