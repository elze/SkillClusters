# This also works on Python Anywhere

import json

from flask import Flask
app = Flask(__name__)


@app.route('/skills')
def skills_mock():
    skillsJsonString = json.dumps([{"primary_term":"Java", "associated_terms": [{"secondary_term":"Hibernate","fraction":0.75},{"secondary_term":"Oracle","fraction":0.6},{"secondary_term":"Spring","fraction":0.5},{"secondary_term":"JMS","fraction":0.4},{"secondary_term":"JBOSS","fraction":0.7},{"secondary_term":"JSP","fraction":0.3},{"secondary_term":"HTML","fraction":0.7},{"secondary_term":"CSS","fraction":0.6},{"secondary_term":"Eclipse","fraction":0.9},{"secondary_term":"Maven","fraction":0.8}]},
				   {"primary_term":"C#", "associated_terms":[{"secondary_term":".NET","fraction":0.9},{"secondary_term":"NHibernate","fraction":0.4},{"secondary_term":"SQL Server","fraction":0.8},{"secondary_term":"Entity Framework","fraction":0.7},{"secondary_term":"ASP.NET","fraction":0.6},{"secondary_term":"NUnit","fraction":0.5},{"secondary_term":"Team Foundation Server","fraction":0.4},{"secondary_term":"HTML","fraction":0.7},{"secondary_term":"CSS","fraction":0.6},{"secondary_term":"Visual Studio","fraction":0.9},{"secondary_term":"Javascript","fraction":0.6},{"secondary_term":"Powershell","fraction":0.1}]},
				   {"primary_term":"Python", "associated_terms":[{"secondary_term":"Django","fraction":0.7},{"secondary_term":"Flask","fraction":0.4},{"secondary_term":"Bottle","fraction":0.1},{"secondary_term":"SQLAlchemy","fraction":0.2},{"secondary_term":"GIS","fraction":0.5},{"secondary_term":"Postgres","fraction":0.4},{"secondary_term":"Git","fraction":0.6},{"secondary_term":"HTML","fraction":0.4},{"secondary_term":"CSS","fraction":0.3},{"secondary_term":"Javascript","fraction":0.4}]},
				   {"primary_term":"Ruby", "associated_terms":[{"secondary_term":"Ruby on Rails","fraction":0.8},{"secondary_term":"Sinatra","fraction":0.3},{"secondary_term":"Elixir","fraction":0.1},{"secondary_term":"ActiveRecord","fraction":0.2},{"secondary_term":"Postgres","fraction":0.2},{"secondary_term":"Git","fraction":0.6},{"secondary_term":"HTML","fraction":0.6},{"secondary_term":"CSS","fraction":0.6},{"secondary_term":"Javascript","fraction":0.5},{"secondary_term":"Mocha","fraction":0.1},{"secondary_term":"Cucumber","fraction":0.4}]},
				   {"primary_term":"Javascript", "associated_terms":[{"secondary_term":"Angular","fraction":0.6},{"secondary_term":"React","fraction":0.4},{"secondary_term":"Backbone","fraction":0.5},{"secondary_term":"Knockout","fraction":0.3},{"secondary_term":"Node","fraction":0.6},{"secondary_term":"Express","fraction":0.2},{"secondary_term":"Git","fraction":0.9},{"secondary_term":"HTML","fraction":0.9},{"secondary_term":"CSS","fraction":0.9},{"secondary_term":"Mocha","fraction":0.1},{"secondary_term":"Chai","fraction":0.1}]}
				   ],
				  indent=4
				   )
    return skillsJsonString

if __name__ == '__main__':
    # Start app
    app.run(debug=True)

