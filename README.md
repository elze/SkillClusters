# SkillClusters

This application parses software developer job ads and determines, for each technical skill keyword (e.g. Python, Java, C#, Javascript, etc) what other skills are most likely to go with it (e.g. for Python it would be Django, Flask, etc.) So when one is preparing for a software development interview, one could know what other areas they need to study to answer the most likely interview questions.

This application is currently deployed at http://elze.pythonanywhere.com/static/index.html

Getting the Flask app to run
============================

To get it to run on your local machine, you should do this: 

1. Install Python and its tools

1.1. Install any version of Python 2.7 or higher.

1.2. Install pip following these instructions: https://pip.pypa.io/en/latest/installing.html

2. Using pip, install Python modules this application needs. From a command prompt, run: 

pip install Flask

pip install sqlalchemy

pip install flask-sqlalchemy

pip install flask-admin

pip install psycopg2


3. Get the web_settings.cfg file from one of the contributors to this project, and place it in the SkillClusters top level directory . This configuration file will contain the configuration options for the Flask app, including the connection string the app needs for connecting to the database.

4. Start the app: from a command prompt, run:

cd <path_to_SkillClusters>/web

flask_app.py

The app should start a local web server, and tell you its URL. You can then go to that URL in the browser.


Getting the parsing program to run
===================================

1. On command prompt, cd into the SkillClusters directory

3. Get the files db_postgres_settings.cfg and import_settings.cfg file from one of the contributors to this project, and place it in the SkillClusters top level directory . Thes configuration files will contain the configuration options for the parsing program, including the connection string it needs for connecting to the database.

3. From SkillClusters directory run the program like this:

python -m parsing.parseJobs



