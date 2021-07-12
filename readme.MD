# Get movie recommendations based on your taste
Users rate movies that they've seen, and get recommendations from other users who rate movies similarly.

The problem that is tackled here is that in other services like imdb and rotten tomatoes,
a high rating from any other user always brings up the average score on the movie.
The idea here is that ratings from users who do not share our taste should be ignored.

## The idea
Every user has a position in the space formed by all the movies in the database, see the illustration below with  2 movies:

![concept](concept_pic.png "concept drawing")

Sid and Andy will be recommended each other's favorite movies. The same goes for Hanna and Molly. Mac has seen the Lion King but not Toy Story and is automatically placed on the Toy Story scale at the middle score 3 and ends up closest to Sid.

## Goal of the project
After involving 50 users with 50 movies each, start getting recommendations that beats those you get from IMDB, Netflix or even friends that thought they knew you.


## Get started
* Make a virtual environment `python -m venv env`
* Activate the virtual environment with CMD `env\Scripts\activate` (Deactivate with `deactivate`)
* Install requirements `pip install -r requirements.txt`

* Add the following to a file called `.env`


    SECRET_KEY=rqr_cjv4igscyu8&&(0ce(=sy=f2)p=f_wn&@0xsp7m$@!kp=d
    DEBUG=True
    ALLOWED_HOSTS=.localhost,127.0.0.1
    DATABASE_URL=sqlite:///db.sqlite3
    EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

* Run `python manage.py migrate`
* Run `python manage.py runserver`
* Play around at http://127.0.0.1:8000/ or http://127.0.0.1:8000/admin/ (admin page is slow, shouldn't have added that many movies to the sqlite db)


Get started with the admin user "ben" with password "ben". The other users also has the same password as their name, e.g. "mac, mac".


## Contributing
This project needs lots of help in its current state and contributing in any way is welcome. Here are some recommended topics for inspiration:
* Search
* Domain name
    * The site needs a domain name to be hosted at. filmtips.xyz was used in the poc-state and might work for the next phase, filmtips.com demands too much money.
* Associate images with movie titles
* Filter irrelevant irrelevant movies
* Automatic database upgrades
* User interface
  * All improvements welcome
* Page scaling for devices with different screen sizes
* Front end

Possible improvements of the algorithm:
* Place users at the average score of an unseen movie instead of at the middle score 3?


#

Reference material for setting up this project
https://simpleisbetterthancomplex.com/series/beginners-guide/1.11/