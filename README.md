# SkillClusters

This application parses software developer job ads and determines, for each technical skill keyword (e.g. Python, Java, C#, Javascript, etc) what other skills are most likely to go with it (e.g. for Python it would be Django, Flask, etc.) So when one is preparing for a software development interview, one could know what other areas they need to study to answer the most likely interview questions.

This application is currently deployed at http://skillclusters.com/sc

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

Or if you are using MySQL database, to install a Python module for it, use

sudo apt-get install python-mysqldb

3. You can connect your local instance of the app to a database on your machine, if you have one installed, or the one used by the app deployed at elze.pythonanywhere.com. (If the latter, ask one of the contributors of this project for these configuration parameters).

In the file settings.cfg file replace the placeholders:

username should be the database username,

password should be the database password,

hostname should be the database's host name (most likely localhost, if you are running it on your machine),

port should be the port the database runs at, if not default (if it is the default, as is most likely the case, remove the [:port] part)

database_name should be the database name


4. Start the app: from a command prompt, run:

cd <path_to_SkillClusters>/web

flask_app.py

The app should start a local web server, and tell you its URL. You can then go to that URL in the browser.


Getting the parsing program to run
===================================

1. On command prompt, cd into the SkillClusters directory

2. Install Postgres database locally on your machine.

3. Run the queries in the create_tables_postgres.sql file to create the tables sc1_skill_post_counters and sc1_skill_pairs. 

4. In the file db_postgres_settings.cfg replace the placeholders: 

username should be your database username,

password should be your database password,

hostname should be your database's host name (most likely localhost, if you are running it on your machine),

port should be the port your database runs at, if not default (if it is the default, as is most likely the case, remove the [:port] part)

database_name should be your database name

5. In the import_settings.cfg file, replace the "path/to/" placeholder with the path to your SkillClusters directory.

6. From SkillClusters directory run the program like this:

python -m parsing.parseJobs



