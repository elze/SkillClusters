# This also works on Python Anywhere

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config.from_pyfile('settings.cfg')

from wtforms import validators

from flask.ext import admin
from flask.ext.admin.contrib import sqla
from flask.ext.admin.contrib.sqla import filters, ModelView

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

import pprint

db = SQLAlchemy(app)

class SkillPostCounter(db.Model):
    __tablename__ = 'skill_post_counters'
    id = db.Column(db.Integer, primary_key=True)
    skill_term = db.Column(db.String(140))
    number_of_postings = db.Column(db.Float)

    def __unicode__(self):
        return self.skill_term

class SkillPair(db.Model):
    __tablename__ = 'skill_pairs'
    id = db.Column(db.Integer, primary_key=True)
    primary_term = db.Column(db.String(140))
    secondary_term = db.Column(db.String(140))
    number_of_times = db.Column(db.Integer)

    ratio = db.column_property(
        #db.select([Decimal(number_of_times) / Decimal(SkillPostCounter.number_of_postings)]).\
	#db.select([SkillPostCounter.number_of_postings / number_of_times]).\
	db.select([number_of_times / SkillPostCounter.number_of_postings]).\
            where(SkillPostCounter.skill_term==primary_term).\
            correlate_except(SkillPostCounter)
    )

    def __unicode__(self):
        return self.primary_term



class SkillView(ModelView):
    #column_select_related_list = ('primary_term', 'secondary_term', 'ratio')
    list_template = 'listCustom.html'
    column_searchable_list = ("primary_term",)
    column_filters = ('primary_term',)

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(SkillView, self).__init__(SkillPair, session, **kwargs)


@app.route('/')
def hello_world():
    return '<a href="/admin/">Click me to get to Admin!</a>'

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

# Create admin
admin = admin.Admin(app, 'SkillCluster')

# Add views
admin.add_view(SkillView(db.session))
#admin.add_view(PercentagesView(db.session))

if __name__ == '__main__':
    # Build a sample db on the fly, if one does not exist yet.
    #app_dir = op.realpath(os.path.dirname(__file__))
    #database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    #if not os.path.exists(database_path):
    #    build_db()

    # Start app
    app.run(debug=True)

