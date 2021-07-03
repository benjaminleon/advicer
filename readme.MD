## Get movie recommendations based on your taste 
Users make ratings between 1 - 5 on movies that they've seen. 

You get recommendations from other users who rate movies similar to you.

The problem that is tackled here is that in other services like imdb and rotten tomatoes,
a high rating from another user always brings up the average score on the movie. The idea here is that we should ignore votes from users who do not share our taste in general. 


### Getting started with a local environment
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
* Play around at http://127.0.0.1:8000/ or http://127.0.0.1:8000/admin/

#

Reference material for setting up this project
https://simpleisbetterthancomplex.com/series/beginners-guide/1.11/