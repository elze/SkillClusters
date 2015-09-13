# This also works on Python Anywhere


from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

import logging
from logging import FileHandler

file_handler = FileHandler("skillClustersLog20150909.txt")
file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)

def skill_pair_default(o):
    if isinstance(o, SkillPair):
        return dict(secondary_term=o.secondary_term,
                    number_of_times=o.number_of_times,
                    ratio=str(o.ratio))


app.config.from_pyfile('settings.cfg')


from flask.ext import admin
# from flask.ext.admin.contrib import sqla
from flask.ext.admin.contrib.sqla import filters, ModelView

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Float, Numeric
from sqlalchemy.sql.expression import cast

from datetime import datetime
import json

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
        # db.select([Decimal(number_of_times) / Decimal(SkillPostCounter.number_of_postings)]).\
        # db.select([SkillPostCounter.number_of_postings / number_of_times]).\
        db.select(
            [cast(cast(number_of_times, Float) / cast(SkillPostCounter.number_of_postings, Float), Numeric(7, 3))]). \
            where(SkillPostCounter.skill_term == primary_term). \
            correlate_except(SkillPostCounter)
    )

    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)

    def __unicode__(self):
        return self.primary_term


class SkillView(ModelView):
    # column_select_related_list = ('primary_term', 'secondary_term', 'ratio')
    list_template = 'listCustom.html'
    column_labels = dict(primary_term='Primary Term', secondary_term='Associated Term',
                         number_of_times='Number of times', ratio='Ratio')
    column_descriptions = dict(
        number_of_times='Number of times associated term appears in a job listing with the primary term',
        ratio='Fraction of Primary Term job listings that have Associated Term in them')
    column_searchable_list = ("primary_term",)
    column_filters = ('primary_term',)

    can_create = False
    can_edit = False
    can_delete = False

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(SkillView, self).__init__(SkillPair, session, **kwargs)


def buildSkillsDictionaries(skillPairs):
    primary_to_secondary = {}
    skills_dictionaries = []

    for s in skillPairs:
        primaryTerm = s.primary_term
        if primaryTerm not in primary_to_secondary:
            primary_to_secondary[primaryTerm] = []
            associatedTerms = []
            this_skill_dictionary = dict(primary_term=primaryTerm, associated_terms=associatedTerms)
            skills_dictionaries.append(this_skill_dictionary)
        this_skill_dictionary["associated_terms"].append(s)

        # app.logger.debug(primaryTerm)
        primary_to_secondary[primaryTerm].append(s)

    return skills_dictionaries

@app.route('/skills')
def skills():
    engine = db.engine

    Session = sessionmaker(bind=engine)
    session = Session()
    q = session.query(SkillPair)
    # skillPairs = q.limit(100).all()
    skillPairs = q.order_by(SkillPair.primary_term.asc(), SkillPair.ratio.asc()).all()

    skills_dictionaries = buildSkillsDictionaries(skillPairs)

    skillsJsonString = json.dumps(skills_dictionaries, sort_keys=True, default=skill_pair_default)
    return skillsJsonString

@app.route('/skills/<primaryTerm>')
def skillsByTerm(primaryTerm):
    # This is not implemented yet: this is the same code as non-paginated skills

    engine = db.engine

    Session = sessionmaker(bind=engine)
    session = Session()
    q = session.query(SkillPair).filter(SkillPair.primary_term.like("%" + primaryTerm + "%"))
    skillPairs = q.order_by(SkillPair.primary_term.asc(), SkillPair.ratio.asc()).all()

    skills_dictionaries = buildSkillsDictionaries(skillPairs)


    skillsJsonString = json.dumps(skills_dictionaries, sort_keys=True, default=skill_pair_default)
    return skillsJsonString

	
@app.route('/skills/<int:pageNum>/<int:itemsPerPage>')
def skillsPage(pageNum, itemsPerPage):
    # In this method we are not using "range" function to get a range of skills_dictionaries
    # between certain indices, because I tried that and range function makes the
    # method impossibly slow. So we are building skills_dictionaries to contain
    # just those primary_terms that fall between certain indices.

    engine = db.engine

    Session = sessionmaker(bind=engine)
    session = Session()
    q = session.query(SkillPair)
    # skillPairs = q.limit(100).all()
    skillPairs = q.order_by(SkillPair.primary_term.asc(), SkillPair.ratio.asc()).all()

    primary_to_secondary = {}

    skills_dictionaries = []
    primary_skill_index = -1
    current_primary_term = ''
	
    for s in skillPairs:
        primaryTerm = s.primary_term
        if primaryTerm != current_primary_term:
	    current_primary_term = primaryTerm
	    primary_skill_index = primary_skill_index + 1

	    if (primary_skill_index >= (pageNum-1)*itemsPerPage) and (primary_skill_index < pageNum*itemsPerPage): 
		associatedTerms = []
		this_skill_dictionary = dict(primary_term=primaryTerm, associated_terms=associatedTerms)
		skills_dictionaries.append(this_skill_dictionary)

	if (primary_skill_index >= (pageNum-1)*itemsPerPage) and (primary_skill_index < pageNum*itemsPerPage): 
	    this_skill_dictionary["associated_terms"].append(s)

        # app.logger.debug(primaryTerm)
        #primary_to_secondary[primaryTerm].append(s)

    # app.logger.debug('primary_terms = \n')
    # app.logger.debug(primary_terms)

    skillsJsonString = json.dumps(skills_dictionaries, sort_keys=True, default=skill_pair_default)
    return skillsJsonString

@app.route('/primary_skills_count')
def primary_skills_count():
    engine = db.engine

    Session = sessionmaker(bind=engine)
    session = Session()
    q = session.query(SkillPostCounter)
    primarySkillsCount = len(q.all())
    countJsonString = json.dumps({"Count": primarySkillsCount})
    return countJsonString

@app.route('/')
def hello_world():
    return '<a href="/admin/">Click me to get to Admin!</a>'


@app.route('/skills_mock/')
def skills_mock():
    skillsJsonString = json.dumps([
        {"primary_term": "C#",
         "associated_terms": [{"skill_term": ".NET", "fraction": 0.9}, {"skill_term": "NHibernate", "fraction": 0.4},
                              {"skill_term": "SQL Server", "fraction": 0.8},
                              {"skill_term": "Entity Framework", "fraction": 0.7},
                              {"skill_term": "ASP.NET", "fraction": 0.6}, {"skill_term": "NUnit", "fraction": 0.5},
                              {"skill_term": "Team Foundation Server", "fraction": 0.4},
                              {"skill_term": "HTML", "fraction": 0.7}, {"skill_term": "CSS", "fraction": 0.6},
                              {"skill_term": "Visual Studio", "fraction": 0.9},
                              {"skill_term": "Javascript", "fraction": 0.6},
                              {"skill_term": "Powershell", "fraction": 0.1}]},
        {"primary_term": "Java",
         "associated_terms": [{"skill_term": "Hibernate", "fraction": 0.75}, {"skill_term": "Oracle", "fraction": 0.6},
                              {"skill_term": "Spring", "fraction": 0.5}, {"skill_term": "JMS", "fraction": 0.4},
                              {"skill_term": "JBOSS", "fraction": 0.7}, {"skill_term": "JSP", "fraction": 0.3},
                              {"skill_term": "HTML", "fraction": 0.7}, {"skill_term": "CSS", "fraction": 0.6},
                              {"skill_term": "Eclipse", "fraction": 0.9}, {"skill_term": "Maven", "fraction": 0.8}]},
        {"primary_term": "Javascript",
         "associated_terms": [{"skill_term": "Angular", "fraction": 0.6}, {"skill_term": "React", "fraction": 0.4},
                              {"skill_term": "Backbone", "fraction": 0.5}, {"skill_term": "Knockout", "fraction": 0.3},
                              {"skill_term": "Node", "fraction": 0.6}, {"skill_term": "Express", "fraction": 0.2},
                              {"skill_term": "Git", "fraction": 0.9}, {"skill_term": "HTML", "fraction": 0.9},
                              {"skill_term": "CSS", "fraction": 0.9}, {"skill_term": "Mocha", "fraction": 0.1},
                              {"skill_term": "Chai", "fraction": 0.1}]},
        {"primary_term": "PHP",
         "associated_terms": [{"skill_term": "Angular", "fraction": 0.3}, {"skill_term": "Ember", "fraction": 0.6},
                              {"skill_term": "Git", "fraction": 0.3}, {"skill_term": "LAMP", "fraction": 0.9},
                              {"skill_term": "Linux", "fraction": 0.6}, {"skill_term": "MVC", "fraction": 0.6},
                              {"skill_term": "Oracle", "fraction": 0.4}, {"skill_term": "REST", "fraction": 0.7},
                              {"skill_term": "MySQL", "fraction": 0.8}, {"skill_term": "HTML", "fraction": 0.4},
                              {"skill_term": "CSS", "fraction": 0.3}, {"skill_term": "Javascript", "fraction": 0.4},
                              {"skill_term": "Symfony", "fraction": 0.4}, {"skill_term": "Zend", "fraction": 0.2}]},
        {"primary_term": "Python",
         "associated_terms": [{"skill_term": "Django", "fraction": 0.7}, {"skill_term": "Flask", "fraction": 0.4},
                              {"skill_term": "Bottle", "fraction": 0.1}, {"skill_term": "SQLAlchemy", "fraction": 0.2},
                              {"skill_term": "GIS", "fraction": 0.5}, {"skill_term": "Postgres", "fraction": 0.4},
                              {"skill_term": "Git", "fraction": 0.6}, {"skill_term": "HTML", "fraction": 0.4},
                              {"skill_term": "CSS", "fraction": 0.3}, {"skill_term": "Javascript", "fraction": 0.4}]},
        {"primary_term": "Ruby", "associated_terms": [{"skill_term": "Ruby on Rails", "fraction": 0.8},
                                                      {"skill_term": "Sinatra", "fraction": 0.3},
                                                      {"skill_term": "Elixir", "fraction": 0.1},
                                                      {"skill_term": "ActiveRecord", "fraction": 0.2},
                                                      {"skill_term": "Postgres", "fraction": 0.2},
                                                      {"skill_term": "Git", "fraction": 0.6},
                                                      {"skill_term": "HTML", "fraction": 0.6},
                                                      {"skill_term": "CSS", "fraction": 0.6},
                                                      {"skill_term": "Javascript", "fraction": 0.5},
                                                      {"skill_term": "Mocha", "fraction": 0.1},
                                                      {"skill_term": "Cucumber", "fraction": 0.4}]}
    ],
        indent=4
    )
    return skillsJsonString

# Create admin
admin = admin.Admin(app, 'SkillCluster')

# Add views
admin.add_view(SkillView(db.session))
# admin.add_view(PercentagesView(db.session))

if __name__ == '__main__':
    # Build a sample db on the fly, if one does not exist yet.
    # app_dir = op.realpath(os.path.dirname(__file__))
    # database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    # if not os.path.exists(database_path):
    #    build_db()

    # Start app
    app.run(debug=True)
