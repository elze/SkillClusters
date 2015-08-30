# This also works on Python Anywhere

import json

from flask import Flask
app = Flask(__name__)


@app.route('/skills_mock/')
def skills_mock():
    skillsJsonString = json.dumps([{"primary_term":"Java", "associated_terms": [{"skill_term":"Hibernate","fraction":0.75},{"skill_term":"Oracle","fraction":0.6},{"skill_term":"Spring","fraction":0.5},{"skill_term":"JMS","fraction":0.4},{"skill_term":"JBOSS","fraction":0.7},{"skill_term":"JSP","fraction":0.3},{"skill_term":"HTML","fraction":0.7},{"skill_term":"CSS","fraction":0.6},{"skill_term":"Eclipse","fraction":0.9},{"skill_term":"Maven","fraction":0.8}]},
				   {"primary_term":"C#", "associated_terms":[{"skill_term":".NET","fraction":0.9},{"skill_term":"NHibernate","fraction":0.4},{"skill_term":"SQL Server","fraction":0.8},{"skill_term":"Entity Framework","fraction":0.7},{"skill_term":"ASP.NET","fraction":0.6},{"skill_term":"NUnit","fraction":0.5},{"skill_term":"Team Foundation Server","fraction":0.4},{"skill_term":"HTML","fraction":0.7},{"skill_term":"CSS","fraction":0.6},{"skill_term":"Visual Studio","fraction":0.9},{"skill_term":"Javascript","fraction":0.6},{"skill_term":"Powershell","fraction":0.1}]},
				   {"primary_term":"Python", "associated_terms":[{"skill_term":"Django","fraction":0.7},{"skill_term":"Flask","fraction":0.4},{"skill_term":"Bottle","fraction":0.1},{"skill_term":"SQLAlchemy","fraction":0.2},{"skill_term":"GIS","fraction":0.5},{"skill_term":"Postgres","fraction":0.4},{"skill_term":"Git","fraction":0.6},{"skill_term":"HTML","fraction":0.4},{"skill_term":"CSS","fraction":0.3},{"skill_term":"Javascript","fraction":0.4}]},
				   {"primary_term":"Ruby", "associated_terms":[{"skill_term":"Ruby on Rails","fraction":0.8},{"skill_term":"Sinatra","fraction":0.3},{"skill_term":"Elixir","fraction":0.1},{"skill_term":"ActiveRecord","fraction":0.2},{"skill_term":"Postgres","fraction":0.2},{"skill_term":"Git","fraction":0.6},{"skill_term":"HTML","fraction":0.6},{"skill_term":"CSS","fraction":0.6},{"skill_term":"Javascript","fraction":0.5},{"skill_term":"Mocha","fraction":0.1},{"skill_term":"Cucumber","fraction":0.4}]},
				   {"primary_term":"Javascript", "associated_terms":[{"skill_term":"Angular","fraction":0.6},{"skill_term":"React","fraction":0.4},{"skill_term":"Backbone","fraction":0.5},{"skill_term":"Knockout","fraction":0.3},{"skill_term":"Node","fraction":0.6},{"skill_term":"Express","fraction":0.2},{"skill_term":"Git","fraction":0.9},{"skill_term":"HTML","fraction":0.9},{"skill_term":"CSS","fraction":0.9},{"skill_term":"Mocha","fraction":0.1},{"skill_term":"Chai","fraction":0.1}]}
				   ],
				  indent=4
				   )
    return skillsJsonString

if __name__ == '__main__':
    # Start app
    app.run(debug=True)

