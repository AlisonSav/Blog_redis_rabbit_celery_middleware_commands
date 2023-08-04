# Practic
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>
<h3 align="center">This is Study project</h3>
Overview
This web application when Authors can create Posts and any users can comment its
Any Users can see Popular posts with Comments, Authors list and Author detail.
Any Users can write comments under the Post, but cant create Posts.
Any Users can send contact form for admin.
All Posts and Comments waiting for Admin moderation. Only Admin can publish created Posts and Comments
Logged Users can create Posts and Comments, can delete Posts. Can see list with his Published and Draft Posts.
Logged Users can update his Profile information.

The main features that have currently been implemented are:

There are models for Authors, Posts and Comments.
Users can view list and detail information for models.
Admin users can create and manage models. The admin has been optimised (the basic registration is present in admin.py, but commented out).

Quick Start
To get this project up and running locally on your computer:

Set up the Python development environment. We recommend using a Python virtual environment.
Assuming you have Python setup, run the following commands (if you're on Windows you may use py or py -3 instead of python to start Python):
pip3 install -r requirements.txt
py manage.py makemigrations
py manage.py migrate
py manage.py collectstatic
py manage.py test # Run the standard tests. These should all pass.
py manage.py createsuperuser # Create a superuser
py manage.py runserver
to run tests:
tox run all tests (flake8, black, unittests)
tox -epep8 run flake8 tests
tox -eblack run black diff tests
tox -etest run only unittests
Open a browser to http://127.0.0.1:8000/admin/ to open the admin site
Create a few test objects of each type.
Open tab to http://127.0.0.1:5000 to see the main site, with your new objects.
If you to create some objects - you need
- first create Users -py manage.py create_users <int>
- after create Posts -py manage.py create_posts <int>
- create Comments -py manage.py create_comments <int>
