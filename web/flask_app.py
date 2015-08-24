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

